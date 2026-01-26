# Continue 配置示例（连接远端 Ollama）

Continue 默认会尝试连接本机 `http://127.0.0.1:11434`。如果你的模型在 DGX Spark（或另一台机器）上，按下面方式配置：

1. 打开 VS Code -> Continue
2. 点击右上角齿轮（设置）
3. 左侧选择 **Models**
4. 打开 `config.yaml`，替换为示例（把 `YOUR_SPARK_IP` 改成实际 IP）

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
    model: gpt-oss:120b
    apiBase: http://YOUR_SPARK_IP:11434
    title: gpt-oss:120b
    roles:
      - chat
      - edit
      - autocomplete
```

验证连通性：

```bash
curl -v http://YOUR_SPARK_IP:11434/api/version
```

