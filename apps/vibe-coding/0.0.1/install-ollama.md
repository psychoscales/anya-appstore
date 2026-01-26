# 安装 Ollama

安装最新版本：

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

拉取一个模型（示例）：

```bash
ollama pull gpt-oss:120b
```

（可选）开启远程访问（局域网工作站连接）：

```bash
sudo systemctl edit ollama
```

添加：

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_ORIGINS=*"
```

然后：

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

