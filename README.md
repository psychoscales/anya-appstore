# anya-appstore

一个极简的应用商店仓库（参考 1Panel appstore 的目录结构），用于被 `anya-backend` 读取并展示应用列表。

当前包含：
- `ollama`：本地推理服务（Docker Compose，数据挂载到 `./data`）
- `open-webui`：基于 Ollama 的聊天 Web UI（Docker Compose）
- `live-vlm-webui`：基于 DGX Spark playbook 的 VLM WebUI（分发/元信息）

## 目录结构

- `data.yaml`：商店元信息（可选，当前仅做占位）
- `apps/<app>/data.yml`：应用元信息（用于列表展示）
- `apps/<app>/README.md`：应用说明
- `apps/<app>/<version>/...`：版本目录（参考 1Panel；包含 `docker-compose.yml`、版本级 `data.yml` 等）

## 说明

- 该仓库的 `apps/*/data.yml` 尽量兼容 1Panel 的字段命名（如 `additionalProperties.key`）。
- `anya-backend` 会优先读取 `ANYA_APPSTORE_DIR` 指定的路径；未设置时会自动在上级目录中查找 `anya-appstore/apps`。

## 产物（manifest + 压缩包）

CI 会从 `apps/**` 生成静态分发产物：

- `dist/manifest.json`：应用索引（包含版本的 `md5` + `url`）
- `dist/apps/<appId>/<version>.tar.gz`：版本包（含 app-level 文件 + 版本目录）

本仓库提供一个生成器：`scripts/manifestgen`（Python + uv）

```bash
cd scripts/manifestgen
uv run python main.py --repo ../.. --out ../../dist
```

## 启动http server

```
cd dist
python3 -m http.server 18080 --bind 127.0.0.1
```
