# Ollama

该应用用于给 Anya 提供 Ollama（本地推理服务）。

当前仓库同时提供两种交付方式：
- 宿主机安装（anya-backend 现阶段对接方式）
- Docker Compose（仅提供应用包模板；本 PR 暂不实现在面板里“管理/安装/升级”）

## 前置条件

### 方式 A：宿主机安装（当前 anya-backend 直接对接）

- 宿主机已安装 `ollama`，并能在 PATH 中找到命令：`ollama version`
- Ollama API 默认监听 `127.0.0.1:11434`（或你自行配置的地址）

### 方式 B：Docker Compose（仅模板）

CPU only：

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

NVIDIA GPU（需要安装 NVIDIA Container Toolkit，并在 Docker 上启用 GPU 支持）：

```bash
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

## Anya Backend 配置

- `ANYA_APPSTORE_DIR`：指向本仓库根目录（例如：`/proj/anya/anya-appstore`）
- `ANYA_OLLAMA_BASE_URL`：Ollama HTTP API（默认：`http://127.0.0.1:11434`）
- `ANYA_OLLAMA_CLI`：Ollama CLI 路径（默认：`ollama`）

## 目标能力（由 anya-backend 提供）

- 展示模型：列出本机已安装的模型
- 下载模型：拉取指定模型
- 对话模型：基于 HTTP API 进行对话
