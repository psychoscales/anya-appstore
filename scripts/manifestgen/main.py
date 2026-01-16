from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import re
import shutil
import tarfile
import tempfile
from pathlib import Path
from typing import Any

import yaml


VERSION_DIR_RE = re.compile(r"^(?:v)?\d[\w.\-]*$")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(Path("../..")), help="path to appstore repo root")
    ap.add_argument("--out", default=str(Path("../../dist")), help="output directory")
    ap.add_argument(
        "--url-prefix",
        default="",
        help="prefix for url fields (default: empty, urls are relative like apps/<appId>/<version>.tar.gz)",
    )
    args = ap.parse_args()

    repo_root = Path(args.repo).resolve()
    out_dir = Path(args.out).resolve()
    url_prefix = str(args.url_prefix).strip()

    apps_dir = repo_root / "apps"
    if not apps_dir.is_dir():
        raise SystemExit(f"invalid repo: missing apps dir at {apps_dir}")

    out_dir.mkdir(parents=True, exist_ok=True)

    errors: list[str] = []

    store_meta: dict[str, Any] = {}
    store_data = repo_root / "data.yaml"
    if store_data.exists():
        try:
            store_meta = yaml.safe_load(store_data.read_text(encoding="utf-8")) or {}
        except Exception as e:  # noqa: BLE001
            errors.append(f"read/parse data.yaml failed: {e}")

    apps: list[dict[str, Any]] = []
    for ent in sorted(apps_dir.iterdir(), key=lambda p: p.name):
        if not ent.is_dir():
            continue

        app_slug = ent.name
        app_data_path = ent / "data.yml"
        if not app_data_path.exists():
            errors.append(f"skip {app_slug}: missing data.yml")
            continue

        try:
            raw = yaml.safe_load(app_data_path.read_text(encoding="utf-8")) or {}
        except Exception as e:  # noqa: BLE001
            errors.append(f"skip {app_slug}: parse data.yml failed: {e}")
            continue

        addl = (raw.get("additionalProperties") or {}) if isinstance(raw, dict) else {}
        anya = (addl.get("anya") or {}) if isinstance(addl, dict) else {}

        app_id = (addl.get("key") or "").strip() if isinstance(addl, dict) else ""
        if not app_id:
            app_id = app_slug

        name = raw.get("name") or addl.get("name") or ""
        tags = raw.get("tags") or addl.get("tags") or []
        typ = addl.get("type") or "unknown"

        app: dict[str, Any] = {
            "appId": app_id,
            "name": name,
            "title": raw.get("title") or "",
            "description": raw.get("description") or "",
            "tags": tags if isinstance(tags, list) else [],
            "type": typ,
            "defaultPort": addl.get("defaultPort") or 0,
            "website": addl.get("website") or "",
            "github": addl.get("github") or "",
            "anya": {
                "installType": anya.get("installType") or "",
                "cliBinary": anya.get("cliBinary") or "",
                "baseURL": anya.get("baseURL") or "",
                "removable": anya.get("removable"),
                "hidden": anya.get("hidden"),
            },
        }

        versions, verrs = build_versions(repo_root, out_dir, url_prefix, app_id, ent)
        errors.extend(verrs)
        if versions:
            app["versions"] = versions

        apps.append(app)

    manifest: dict[str, Any] = {
        "schemaVersion": 1,
        "generatedAt": _utc_rfc3339(),
        "store": store_meta,
        "apps": apps,
    }
    if errors:
        manifest["errors"] = errors

    manifest_path = out_dir / "manifest.json"
    write_json_atomic(manifest_path, manifest)


def build_versions(
    repo_root: Path, out_dir: Path, url_prefix: str, app_id: str, app_path: Path
) -> tuple[list[dict[str, Any]], list[str]]:
    out: list[dict[str, Any]] = []
    errs: list[str] = []

    for ent in sorted(app_path.iterdir(), key=lambda p: p.name):
        if not ent.is_dir():
            continue
        version = ent.name
        if not VERSION_DIR_RE.match(version):
            continue

        version_data_path = ent / "data.yml"
        if not version_data_path.exists():
            errs.append(f"skip {app_id}/{version}: missing version data.yml")
            continue

        try:
            version_data = yaml.safe_load(version_data_path.read_text(encoding="utf-8")) or {}
        except Exception as e:  # noqa: BLE001
            errs.append(f"skip {app_id}/{version}: parse version data.yml failed: {e}")
            continue

        tgz_out = out_dir / "apps" / app_id / f"{version}.tar.gz"
        tgz_out.parent.mkdir(parents=True, exist_ok=True)

        try:
            write_app_tar_gz(tgz_out, app_id, app_path, version)
        except Exception as e:  # noqa: BLE001
            errs.append(f"pack {app_id}/{version}: {e}")
            continue

        md5hex = md5_file(tgz_out)
        rel_url = f"apps/{app_id}/{version}.tar.gz"
        if url_prefix:
            rel_url = url_prefix.rstrip("/") + "/" + rel_url

        out.append(
            {
                "version": version,
                "url": rel_url,
                "md5": md5hex,
                "bytes": tgz_out.stat().st_size,
                "data": version_data,
            }
        )

    out.sort(key=lambda v: _version_key(v["version"]))
    return out, errs


def write_app_tar_gz(out_path: Path, app_id: str, app_path: Path, version: str) -> None:
    # Pack:
    # - app-level files (data.yml, README.md, logo.png if exists)
    # - the entire version directory (e.g. 1.2.3/**)
    #
    # Tar entry names are <appId>/<relativePathFromAppDir>.
    tmp_dir = Path(tempfile.mkdtemp(prefix="anya-appstore-pack-"))
    try:
        tmp_path = tmp_dir / (out_path.name + ".tmp")

        def _filter(ti: tarfile.TarInfo) -> tarfile.TarInfo:
            # Make the archive deterministic across checkouts/runs so package md5 is stable.
            ti.uid = 0
            ti.gid = 0
            ti.uname = ""
            ti.gname = ""
            ti.mtime = 0
            return ti

        with tmp_path.open("wb") as f:
            with gzip.GzipFile(filename="", mode="wb", fileobj=f, mtime=0) as gz:
                with tarfile.open(fileobj=gz, mode="w") as tf:
                    for fn in ("data.yml", "README.md", "logo.png"):
                        src = app_path / fn
                        if src.exists() and src.is_file():
                            tf.add(src, arcname=f"{app_id}/{fn}", recursive=False, filter=_filter)

                    version_dir = app_path / version
                    if not version_dir.is_dir():
                        raise FileNotFoundError(str(version_dir))

                    for root, dirs, files in os.walk(version_dir):
                        dirs.sort()
                        files.sort()
                        root_p = Path(root)
                        for f in files:
                            src = root_p / f
                            rel = src.relative_to(app_path).as_posix()
                            tf.add(src, arcname=f"{app_id}/{rel}", recursive=False, filter=_filter)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        os.replace(tmp_path, out_path)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def md5_file(path: Path) -> str:
    h = hashlib.md5()  # noqa: S324 - used for integrity check, not security
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json_atomic(path: Path, v: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    b = json.dumps(v, ensure_ascii=False, indent=2) + "\n"
    tmp.write_text(b, encoding="utf-8")
    os.replace(tmp, path)


def _utc_rfc3339() -> str:
    # Avoid importing datetime for this tiny tool; time in UTC is enough.
    import time

    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _version_key(v: str) -> tuple[list[int], str]:
    # Best-effort semver-ish ordering; falls back to lexicographic.
    s = v.lstrip("v")
    parts = s.split(".")
    nums: list[int] = []
    for p in parts:
        try:
            nums.append(int(p))
        except ValueError:
            break
    return nums, v


if __name__ == "__main__":
    main()
