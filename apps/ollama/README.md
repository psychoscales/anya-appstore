# Ollama（宿主机安装）

该应用用于在 Anya 的面板中“接管/对接”宿主机已经安装的 Ollama（不通过 Docker 安装）。

## 前置条件

- 宿主机已安装 `ollama`，并能在 PATH 中找到命令：`ollama version`
- Ollama API 默认监听 `127.0.0.1:11434`（或你自行配置的地址）

## Anya Backend 配置

- `ANYA_APPSTORE_DIR`：指向本仓库根目录（例如：`/proj/anya/anya-appstore`）
- `ANYA_OLLAMA_BASE_URL`：Ollama HTTP API（默认：`http://127.0.0.1:11434`）
- `ANYA_OLLAMA_CLI`：Ollama CLI 路径（默认：`ollama`）

## 目标能力（由 anya-backend 提供）

- 展示模型：列出本机已安装的模型
- 下载模型：拉取指定模型
- 对话模型：基于 HTTP API 进行对话
