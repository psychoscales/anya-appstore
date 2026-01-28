# 应用开发指南（anya-appstore）

本指南用于帮助开发者向 `anya-appstore` 提交应用版本，目标是：结构统一、可升级、可回滚、易维护。

## 1. 开发原则

- 结构固定：遵循 `apps/<appId>/<version>/` 的版本目录规范。
- 可升级：升级只切换 compose 与 `.version`，迁移仅允许写入 `data/`。
- 可回滚：保留旧版本目录，升级失败会自动回滚。
- 可移植：所有持久化数据写入 `./data`（相对路径）。
- 可配置：通过 `data.yml` 的 `formFields` 暴露必要参数。
- 版本清晰：推荐使用语义化版本（如 `0.1.0`），避免随意跳号。

## 2. 目录结构

```
anya-appstore/
  apps/
    <appId>/
      data.yml               # 应用级元信息（列表展示）
      README.md              # 应用说明（可选）
      <version>/
        docker-compose.yml   # 版本级部署文件（必需）
        data.yml             # 版本级配置字段（可选）
        README.md            # 版本级说明（推荐）
        docs.yml             # 文档导航（可选）
        upgrade.yml          # 升级迁移脚本（可选）
```

## 3. 应用级 data.yml（必需）

路径：`apps/<appId>/data.yml`

最小示例：

```yaml
name: Demo App
tags:
  - Demo
title: 示例应用（Compose）
description: 简要描述应用功能。
additionalProperties:
  key: demo-app
  name: Demo App
  tags:
    - Demo
  type: website
  website: https://example.com
  github: https://github.com/example/demo
  defaultPort: 8080
  anya:
    installType: compose
    removable: true
    hidden: false
```

说明：

- `name/title/description/tags` 会用于列表展示。
- `additionalProperties.key` 缺省时使用目录名作为 appId。
- `anya.installType` 当前使用 `compose`。
- `anya.removable` 控制是否允许卸载。
- `anya.hidden` 控制是否在列表中隐藏（系统能力类可设为 true）。

## 4. 版本级 data.yml（可选）

路径：`apps/<appId>/<version>/data.yml`

用于定义安装时可配置的环境变量（表单字段）：

```yaml
additionalProperties:
  formFields:
    - envKey: PANEL_APP_PORT_HTTP
      labelZh: HTTP端口
      labelEn: HTTP Port
      type: number
      default: 8080
      required: true
    - envKey: OLLAMA_BASE_URL
      labelZh: Ollama 地址
      labelEn: Ollama Base URL
      type: text
      default: http://host.docker.internal:11434
      required: true
```

说明：

- `envKey` 必填，对应 `docker-compose.yml` 中的环境变量。
- `default` 作为默认值展示与回填。
- `labelZh/labelEn` 用于 UI 展示。
- `type` 可写 `text/number`（当前 UI 统一为文本输入，但建议规范填写）。

## 5. docker-compose.yml 编写规范

路径：`apps/<appId>/<version>/docker-compose.yml`

推荐规范：

- 使用 Compose v2 语法（不需要 `version:`）。
- 服务名称稳定且简单（如 `web`、`app`）。
- 镜像使用明确版本标签，不要直接用 `latest`。
- 持久化目录统一挂载到 `./data`。
- 端口映射使用表单变量，如 `${PANEL_APP_PORT_HTTP:-8080}`。
- 建议设置 `restart: unless-stopped`。

示例：

```yaml
services:
  web:
    image: myrepo/demo:1.2.3
    restart: unless-stopped
    ports:
      - "${PANEL_APP_PORT_HTTP:-8080}:8080"
    environment:
      - DEMO_MODE=${DEMO_MODE:-false}
    volumes:
      - ./data:/app/data
```

## 6. 文档（README / docs.yml）

版本目录内推荐提供 `README.md` 作为默认文档。

可选：`docs.yml` 定义文档导航（多个 Markdown 页面）：

```yaml
default: README.md
pages:
  - title: 快速开始
    file: README.md
  - title: 高级配置
    file: advanced.md
```

要求：

- `file` 必须是版本目录内的 Markdown 文件。
- 未提供 `docs.yml` 时会自动使用 `README.md`，或读取目录内其他 `.md`。

## 7. upgrade.yml（升级/迁移，可选）

路径：`apps/<appId>/<version>/upgrade.yml`

当前仅支持 `file.write`，且 **只允许写入 `data/` 目录**：

```yaml
schemaVersion: 1
paths:
  - from: "0.0.1"
    to: "0.0.2"
    steps:
      - type: file.write
        args:
          path: data/migrated_to_0.0.2.txt
          content: migrated OK (0.0.1 -> 0.0.2)
```

说明：

- `paths` 可以包含多个升级路径。
- `from/to` 使用版本字符串匹配。
- 迁移脚本失败会触发自动回滚。

## 8. 更新/发布流程

1. 新增版本目录：`apps/<appId>/<newVersion>/`。
2. 更新 `docker-compose.yml`（镜像版本、配置变更等）。
3. 如需新参数，更新版本级 `data.yml`。
4. 如需数据迁移，新增或更新 `upgrade.yml`。
5. 更新版本级 `README.md` 或文档页面。
6. （可选）调整应用级 `apps/<appId>/data.yml` 元信息。
7. 生成分发产物：

```bash
cd /home/xy3/proj/anya/anya-appstore/scripts/manifestgen
uv run python main.py --repo ../.. --out ../../dist
```

8. 本地安装/升级验证通过后提交 PR。

## 9. 提交前自检清单

- [ ] `apps/<appId>/data.yml` 存在且字段完整
- [ ] `apps/<appId>/<version>/docker-compose.yml` 可直接运行
- [ ] 所有持久化数据使用 `./data`
- [ ] 表单字段与 compose 环境变量一致
- [ ] 升级路径（如有）仅写入 `data/`
- [ ] 生成并更新 `dist/manifest.json`

