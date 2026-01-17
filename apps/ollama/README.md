# Ollama

该应用用于给 Anya 提供 Ollama（本地推理服务），并通过 Docker Compose 管理。

Ollama 模型等持久化数据会挂载到 `./data`（宿主机目录，路径相对于 `docker-compose.yml` 所在目录）。

## 启动（本地 / 手工）

```bash
cd anya-appstore/apps/ollama/0.0.1
PANEL_APP_PORT_HTTP=11434 docker compose up -d
```

停止：

```bash
cd anya-appstore/apps/ollama/0.0.1
docker compose stop
```

## GPU（可选）

- NVIDIA：安装 NVIDIA Container Toolkit；本应用的 `docker-compose.yml` 已默认包含 `gpus: all`（以及 `deploy.resources.reservations.devices`）。如需纯 CPU 运行可移除这些字段。
- AMD：把镜像改为 `ollama/ollama:rocm`，并按需添加 `devices: ["/dev/kfd", "/dev/dri"]`。

## Anya Backend 配置

- `ANYA_APPSTORE_DIR`：指向本仓库根目录（例如：`/proj/anya/anya-appstore`）
- `ANYA_OLLAMA_BASE_URL`：Ollama HTTP API（默认：`http://127.0.0.1:11434`）
- `ANYA_OLLAMA_CLI`：Ollama CLI 路径（默认：`ollama`；未安装 CLI 时也可仅通过 HTTP 工作）

## 目标能力（由 anya-backend 提供）

- 展示模型：列出本机已安装的模型
- 下载模型：拉取指定模型
- 对话模型：基于 HTTP API 进行对话
