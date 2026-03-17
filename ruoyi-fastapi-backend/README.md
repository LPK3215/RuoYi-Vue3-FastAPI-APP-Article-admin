# ruoyi-fastapi-backend（后端使用说明）

本目录是项目的 FastAPI 后端，统一提供：

- 管理端 API
- Portal Web / App API
- Swagger / ReDoc 文档

---

## 1. 环境与依赖

### 基础依赖

- Python 3.10+
- Redis 6+
- MySQL 5.7+ / MariaDB
- 或 PostgreSQL 13+

### Python 依赖文件

| 文件 | 用途 |
|------|------|
| `requirements.txt` | MySQL / MariaDB 场景 |
| `requirements-pg.txt` | PostgreSQL 场景 |

---

## 2. 环境切换规则

后端现在统一按下面的优先级选择环境：

1. 显式传入的 `--env`
2. 已设置的 `APP_ENV`
3. 默认回退到 `dev`

并且如果 `.env.<env>` 不存在，会直接报错退出，不再悄悄用默认值启动。

### 当前已提供的环境文件

| 环境名 | 配置文件 | 典型用途 |
|--------|----------|----------|
| `dev` | `.env.dev` | 本机开发 |
| `prod` | `.env.prod` | 本机模拟生产 / 正式部署 |
| `dockermy` | `.env.dockermy` | Docker + MySQL |
| `dockerpg` | `.env.dockerpg` | Docker + PostgreSQL |

### 推荐启动方式

日常本机开发，优先直接运行脚本，不需要自己记很多参数：

```powershell
# 仓库根目录，默认 dev
.\2-backend-start.bat

# 或者在后端目录中运行，默认 dev
.\run.bat

# 只有在明确切环境时才传参
.\run.bat prod
.\run.bat dockermy
.\run.bat dockerpg
```

如果你不用脚本，也可以直接：

```bash
python app.py
python app.py --env prod
```

### 自定义环境

如果你需要 `stage`、`test` 之类的环境，可以直接新增：

- `.env.stage`
- `.env.test`

然后运行：

```bash
python app.py --env stage
python app.py --env test
```

---

## 3. 数据库初始化

首次部署或首次本机启动，至少需要导入以下 SQL：

1. 基础表 / 权限 / 字典：`sql/ruoyi-fastapi.sql`
2. 软件库业务表 + 菜单：`sql/ruoyi-fastapi-software.sql`
3. 教程 / 知识库：`sql/ruoyi-fastapi-kb.sql`

### 增量 SQL

已有数据库升级时按需执行：

- 软件菜单顺序 / 授权同步：`sql/ruoyi-fastapi-software-menu-migrate.sql`
- 教程菜单迁移：`sql/ruoyi-fastapi-kb-menu-migrate.sql`
- KB 表结构补充：`sql/ruoyi-fastapi-kb-db-migrate.sql`
- KB 分类修复：`sql/ruoyi-fastapi-kb-category-migrate.sql`

### PostgreSQL

如果本机或 Docker 使用 PostgreSQL，请导入：

- `sql/ruoyi-fastapi-pg.sql`

---

## 4. Redis 准备

后端依赖 Redis，默认数据库编号是 `2`。

Windows 下仓库内提供了辅助脚本：

```powershell
..\scripts\dev\setup-redis.ps1
..\scripts\dev\start-redis.ps1
```

---

## 5. 本机开发启动

### MySQL / MariaDB

```powershell
cd ruoyi-fastapi-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
.\run.bat
```

### PostgreSQL

建议做一份专用环境文件，例如 `.env.pgdev`，把 `DB_TYPE` 改成 `postgresql` 并配置 PostgreSQL 连接信息，然后：

```powershell
cd ruoyi-fastapi-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-pg.txt
python app.py --env pgdev
```

### 启动后默认地址

- API：`http://127.0.0.1:9099`
- Swagger：`http://127.0.0.1:9099/docs`
- ReDoc：`http://127.0.0.1:9099/redoc`

说明：

- 本机日常开发应优先走 `.env.dev`
- 验证码、Swagger、本地调试链路都先在 `dev` 里确认
- 本地默认建议保持验证码开启；如需临时关闭，可手动执行 `sql/ruoyi-fastapi-dev-disable-captcha.sql`
- 如果之前关闭过验证码，可用 `sql/ruoyi-fastapi-dev-enable-captcha.sql` 恢复
- 只有当本机开发确认无误后，再切到 `prod` / Docker / 自定义部署环境

---

## 6. 生产 / 预发布启动

### 统一入口

```bash
python app.py --env prod
```

Windows 下也可以继续沿用统一脚本：

```powershell
.\run.bat prod
```

### 使用 uvicorn

使用 `uvicorn` 时不能再带 `--env`，需要先设置环境变量：

- Windows PowerShell

```powershell
$env:APP_ENV="prod"
uvicorn server:create_app --factory --host 0.0.0.0 --port 9099 --workers 2
```

- macOS / Linux

```bash
export APP_ENV=prod
uvicorn server:create_app --factory --host 0.0.0.0 --port 9099 --workers 2
```

### 关键生产项

重点检查：

- `APP_ROOT_PATH`
- `APP_RELOAD=false`
- `APP_DISABLE_SWAGGER=true`
- `APP_DISABLE_REDOC=true`
- 数据库和 Redis 凭据

---

## 7. Docker 启动

### MySQL 版本

仓库根目录：

```bash
docker compose -f docker-compose.my.yml up -d --build
```

默认地址：

- 管理后台：`http://127.0.0.1:12580`
- 后端：`http://127.0.0.1:19099`

Windows 也可使用：

```powershell
.\scripts\dev\start-dockermy-and-check.ps1
```

### PostgreSQL 版本

```bash
docker compose -f docker-compose.pg.yml up -d --build
```

默认地址同样是：

- 管理后台：`http://127.0.0.1:12580`
- 后端：`http://127.0.0.1:19099`

---

## 8. 与前端的前缀约定

后端常见前缀与前端构建模式要配套：

| 场景 | 后端 `APP_ROOT_PATH` | 前端 API 前缀 |
|------|----------------------|---------------|
| 本机开发 | `/dev-api` | `/dev-api` |
| 预发布 | `/stage-api` | `/stage-api` |
| 生产 | `/prod-api` | `/prod-api` |
| Docker | `/docker-api` | `/docker-api` |

说明：

- 管理后台会把 `/dev-api`、`/prod-api`、`/docker-api` 等前缀代理给后端
- 如果你新增 `stage`，请同时让前端构建和 Nginx 也使用 `/stage-api`

---

## 9. 常用验证

### 接口健康检查

启动后至少验证：

- `http://127.0.0.1:9099/docs`
- 登录接口是否可用
- Redis 是否能写入 token / 锁信息

### 默认管理员

- 用户名：`admin`
- 密码：`admin123`

---

## 10. 常见问题

### 改了 `.env.*` 但行为没变化

后端不会自动热加载配置，改完后需要重启进程。

### 本机开发改代码后接口没变化

`.env.dev` 当前默认：

- `APP_RELOAD = false`

如果希望开发期热重载，可以临时改成 `true`。

### 登录被锁

Redis 中删除这些 Key 即可：

- `account_lock:admin`
- `password_error_count:admin`

### 本机切换到 PostgreSQL 启动失败

通常是以下原因之一：

- 还在安装 `requirements.txt`，没有安装 `requirements-pg.txt`
- 还在使用 MySQL 的 SQL，而不是 `sql/ruoyi-fastapi-pg.sql`
- `.env.<env>` 里 `DB_TYPE` 不是 `postgresql`

---

## 11. 进一步阅读

- [部署说明](./DEPLOY.md)
- [仓库总说明](../README.md)
