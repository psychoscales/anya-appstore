# 在 Anya 中启动 Ollama + 安装模型

## 1) 同步 AppStore

- 打开 Anya：`/apps`
- 点击“更新列表”（同步 AppStore）

## 2) 启动 Ollama

任选其一：

- 方式 A：在 `/apps` 找到 `Ollama` -> 点击“管理” -> 点击“启动”
- 方式 B：直接打开 `/models` -> 如果提示未运行，点击“启动”

提示：
- 默认 HTTP 端口为 `11434`（Anya 的 `Ollama` 应用配置里可调整）
- Ollama 的数据（模型等）会落盘在 Anya 的缓存目录下 `compose/ollama/data/`（用于验证“数据不丢”）

## 3) 安装/拉取模型

- 打开 `/models`
- 在 “Library / 搜索” 中选择一个模型（例如：`qwen2.5:7b`、`llama3.1:8b` 等）
- 点击 “Pull / 下载”
- 下载完成后会出现在 “已安装模型” 列表里

完成后进入下一页：配置 VS Code Continue 连接到 Anya 的 Ollama。

