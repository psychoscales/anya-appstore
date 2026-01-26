# Continue 配置（连接 Anya 的 Ollama）

在 Anya Client 中，Ollama 通常由 Anya 在本机启动，因此 Continue 最简单的配置就是连接本机：

- `apiBase: http://127.0.0.1:11434`

如果你在 Anya 的 `Ollama` 应用配置里改了端口，请把 `11434` 替换为实际值。

## 配置步骤

1) 打开 VS Code -> Continue
2) 点击右上角齿轮（Settings）
3) 左侧选择 **Models**
4) 打开 `config.yaml`，替换为示例

```yaml
name: Config
version: 1.0.0
schema: v1

assistants:
  - name: default
    model: OllamaSpark

models:
  - name: OllamaSpark
    provider: ollama
    model: qwen2.5:7b
    apiBase: http://127.0.0.1:11434
    title: qwen2.5:7b
    roles:
      - chat
      - edit
      - autocomplete
```

注意：
- `model:` 需要填写你已经在 Anya 的 `/models` 页面里 **拉取完成** 的模型名称。

## 连通性验证

验证 Ollama API（本机）：

```bash
curl -v http://127.0.0.1:11434/api/version
```

如果你要让 Continue 连接远端（例如 Anya 跑在 DGX Spark，你在工作站用 VS Code）：
- 需要确保工作站能访问到远端的 Ollama `http://<spark-ip>:11434`
- 然后把 `apiBase` 改成 `http://<spark-ip>:11434`
