# SoftwareHub 后端（ruoyi-fastapi-backend）部署文档

本目录为 **FastAPI 后端服务**，同时提供：

- 后台管理 API（管理端登录后使用）
- Portal API（用户端/公开展示使用）

> 更完整的本机开发说明见：`ruoyi-fastapi-backend/README.md`。本文件侧重“部署与环境配置”。

---

## 环境要求

- Python 3.10+
- MySQL 5.7+（或 PostgreSQL 13+）
- Redis 6.0+

---

## 环境文件与配置

后端会按 `APP_ENV` 加载对应的 `.env.*` 文件：

- 默认：`.env.dev`
- 生产：`.env.prod`
- Docker（MySQL / PG）：`.env.dockermy` / `.env.dockerpg`

关键配置（示例）：

```ini
APP_ENV = 'prod'
APP_HOST = '0.0.0.0'
APP_PORT = 9099
APP_RELOAD = false
APP_ROOT_PATH = '/prod-api'

DB_TYPE = 'mysql'
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_DATABASE = 'ruoyi-fastapi'

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = ''
REDIS_DATABASE = 2
```

---

## 初始化数据库（首次部署必须）

本项目的菜单/权限/字典/种子数据依赖 SQL 初始化，首次部署请执行：

1. 基础表/权限/字典：`sql/ruoyi-fastapi.sql`
2. 软件库业务表 + 菜单：`sql/ruoyi-fastapi-software.sql`
3. 教程/知识库（文章 + 关联软件 + 菜单）：`sql/ruoyi-fastapi-kb.sql`

> 如果是“已有库升级”，且只想同步软件菜单顺序/授权，可执行：`sql/ruoyi-fastapi-software-menu-migrate.sql`。

> 如果是“已有库升级”，且教程菜单仍挂在「软件管理」下，可执行：`sql/ruoyi-fastapi-kb-menu-migrate.sql`。

> 如果是“已有库升级”，且缺少教程分类表或 `tool_kb_article.category_id`，可执行：`sql/ruoyi-fastapi-kb-db-migrate.sql`。

---

## 启动方式

推荐先用统一入口（支持 `--env`）跑通：

```bash
cd ruoyi-fastapi-backend
python app.py --env prod
```

如果使用 `uvicorn`（需要通过环境变量指定环境）：

- Windows PowerShell：

```powershell
$env:APP_ENV="prod"
uvicorn server:create_app --factory --host 0.0.0.0 --port 9099 --workers 2
```

- macOS/Linux：

```bash
export APP_ENV=prod
uvicorn server:create_app --factory --host 0.0.0.0 --port 9099 --workers 2
```

---

## 与前端的路径约定（反向代理）

典型部署建议：

- 管理端静态资源：`/`（来自 `ruoyi-fastapi-frontend/dist`）
- API：`/prod-api/` 代理到后端 `9099`，并去掉 `/prod-api` 前缀再转发

Nginx 示例见：`ruoyi-fastapi-backend/README.md`。

---

## 验证部署

- API：`http://127.0.0.1:9099`
- Swagger：`http://127.0.0.1:9099/docs`（可通过 `.env.prod` 关闭）
