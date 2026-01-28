# Demo Migrate

用于验证“按版本号升级 + 迁移 + 回滚 + 安装后动作”的示例应用。

- `0.0.1`：返回文本 `demo-migrate v0.0.1`
- `0.0.2`：返回文本 `demo-migrate v0.0.2`，并提供 `upgrade.yml` 在升级时写入 `data/migrated_to_0.0.2.txt`
- `actions.yml`：安装时触发 `ollama pull qwen2.5:0.5b`
