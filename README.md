# anya-appstore

一个极简的应用商店仓库（参考 1Panel appstore 的目录结构），用于被 `anya-backend` 读取并展示应用列表。

当前仅包含一个应用：`ollama`（宿主机安装/运行，非 Docker 安装）。

## 目录结构

- `data.yaml`：商店元信息（可选，当前仅做占位）
- `apps/<app>/data.yml`：应用元信息（用于列表展示）
- `apps/<app>/README.md`：应用说明

## 说明

- 该仓库的 `apps/*/data.yml` 尽量兼容 1Panel 的字段命名（如 `additionalProperties.key`）。
- `anya-backend` 会优先读取 `ANYA_APPSTORE_DIR` 指定的路径；未设置时会自动在上级目录中查找 `anya-appstore/apps`。
