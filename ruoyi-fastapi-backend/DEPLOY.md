# ruoyi-fastapi-backend（部署说明）

本文件聚焦后端部署，覆盖：

- 本机部署
- 生产部署
- Docker 部署
- 环境切换
- 反向代理

更详细的开发说明见：[README.md](./README.md)

---

## 1. 部署前检查清单

### 依赖

- Python 3.10+
- Redis 6+
- MySQL 5.7+ / MariaDB 或 PostgreSQL 13+

补充：

- 本机 Redis 辅助脚本默认配置集中在 `../scripts/dev/redis-version.json`
- 当前固定镜像为 `redis:7.4.8`

### 必做项

1. 准备数据库
2. 准备 Redis
3. 准备对应的 `.env.*`
4. 初始化 SQL
5. 启动后端
6. 配置 Nginx 或其他反向代理

---

## 2. 环境文件选择

后端统一按下面优先级加载环境：

1. `--env`
2. `APP_ENV`
3. 默认 `dev`

并且 `.env.<env>` 缺失时会直接报错退出，避免“明明改了 A，实际却跑了 B”。

### 内置环境

| 环境 | 配置文件 | 说明 |
|------|----------|------|
| `dev` | `.env.dev` | 本机开发 |
| `prod` | `.env.prod` | 正式环境 / 本机模拟生产 |
| `dockermy` | `.env.dockermy` | Docker + MySQL |
| `dockerpg` | `.env.dockerpg` | Docker + PostgreSQL |

### 自定义环境

如果要部署预发布环境，建议新增：

- `.env.stage`

并至少调整：

```ini
APP_ENV = 'stage'
APP_ROOT_PATH = '/stage-api'
APP_RELOAD = false
APP_DISABLE_SWAGGER = true
APP_DISABLE_REDOC = true
```

启动：

```bash
python app.py --env stage
```

---

## 3. 数据库初始化

### MySQL / MariaDB

这里不是“3 个数据库”，而是“同一个数据库的 3 段初始化 SQL”。

推荐直接使用汇总入口：

1. `sql/ruoyi-fastapi-all.sql`

如果你想按模块拆开执行，也可以继续沿用：

1. `sql/ruoyi-fastapi.sql`
2. `sql/ruoyi-fastapi-software.sql`
3. `sql/ruoyi-fastapi-kb.sql`

MySQL 命令行一键导入示例（从仓库根目录执行）：

```bash
mysql -h 127.0.0.1 -u root -p ruoyi-fastapi < ruoyi-fastapi-backend/sql/ruoyi-fastapi-all.sql
```

### PostgreSQL

推荐直接使用汇总入口：

1. `sql/ruoyi-fastapi-pg-all.sql`

如果你想按模块拆开执行，也可以继续沿用：

1. `sql/ruoyi-fastapi-pg.sql`
2. `sql/ruoyi-fastapi-pg-software.sql`
3. `sql/ruoyi-fastapi-pg-kb.sql`

PostgreSQL 命令行一键导入示例（从仓库根目录执行）：

```bash
psql -h 127.0.0.1 -U postgres -d ruoyi-fastapi -f ruoyi-fastapi-backend/sql/ruoyi-fastapi-pg-all.sql
```

### 增量迁移

按需执行：

- `sql/ruoyi-fastapi-software-menu-migrate.sql`
- `sql/ruoyi-fastapi-kb-menu-migrate.sql`
- `sql/ruoyi-fastapi-kb-db-migrate.sql`
- `sql/ruoyi-fastapi-kb-category-migrate.sql`

---

## 4. 本机部署

### 推荐原则

- 日常本机使用，固定优先走 `.env.dev`
- 本地把验证码、文档、接口、管理端链路全部确认正常后，再切到 `prod` 或部署环境
- 不建议把“日常开发启动”和“部署启动”混在一起
- 本地默认建议开启验证码；如果只是为了临时调试才关闭，请显式执行 `sql/ruoyi-fastapi-dev-disable-captcha.sql`
- 需要恢复时执行 `sql/ruoyi-fastapi-dev-enable-captcha.sql`

### MySQL / MariaDB

```powershell
cd ruoyi-fastapi-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
.\run.bat
```

仓库根目录也可以直接：

```powershell
.\ruoyi-fastapi-backend\run.bat
```

### PostgreSQL

```powershell
cd ruoyi-fastapi-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-pg.txt
.\run.bat pgprod
```

说明：

- `pgprod` 只是示例名，对应你自己准备的 `.env.pgprod`
- 只要文件名和 `--env` 一致即可

---

### 本机模拟生产

只有在你明确要验证生产配置时，再运行：

```powershell
cd ruoyi-fastapi-backend
.\run.bat prod
```

## 5. 使用 uvicorn / 多 worker

如果你希望自己控制 worker 数量，使用：

- Windows PowerShell

```powershell
$env:APP_ENV="prod"
uvicorn server:create_app --factory --host 0.0.0.0 --port 9099 --workers 2
```

- Linux / macOS

```bash
export APP_ENV=prod
uvicorn server:create_app --factory --host 0.0.0.0 --port 9099 --workers 2
```

注意：

- `uvicorn` 模式下不再使用 `--env`
- `APP_ENV` 必须提前设置

---

## 6. Docker 部署

### MySQL 版本

仓库根目录执行：

```bash
docker compose -f docker-compose.my.yml up -d --build
```

端口：

- 管理后台：`12580`
- 后端：`19099`
- MySQL：`13306`
- Redis：`16379`

说明：

- `docker-compose.my.yml` 现在会自动导入基础 + software + kb 三段 MySQL SQL
- 不需要再额外手工补执行软件库和 KB 初始化脚本

### PostgreSQL 版本

```bash
docker compose -f docker-compose.pg.yml up -d --build
```

端口：

- 管理后台：`12580`
- 后端：`19099`
- PostgreSQL：`15432`
- Redis：`16379`

### Windows 辅助脚本

MySQL Docker 方案可以直接用：

```powershell
.\scripts\dev\start-dockermy-and-check.ps1
```

它会自动：

1. 启动 compose
2. 等待 MySQL / Redis 健康
3. 校验数据库中的业务表和菜单
4. 校验 Portal 接口

说明：

- Docker 场景本质上仍然是同一个后端入口，只是换成 `.env.dockermy` / `.env.dockerpg`
- 本机开发没问题后，再切到 Docker / 生产环境，排障会简单很多
- 两套 compose 现在都会自动导入基础 + software + kb 业务 SQL

---

## 7. Nginx 反向代理

### 生产环境 `/prod-api`

```nginx
server {
  listen 80;
  server_name your-domain.com;

  location /prod-api/ {
    proxy_pass http://127.0.0.1:9099/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

### 预发布 `/stage-api`

```nginx
server {
  listen 80;
  server_name stage.your-domain.com;

  location /stage-api/ {
    proxy_pass http://127.0.0.1:9099/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

### Docker `/docker-api`

项目里现成配置在：

- `ruoyi-fastapi-frontend/bin/nginx.dockermy.conf`
- `ruoyi-fastapi-frontend/bin/nginx.dockerpg.conf`

---

## 8. 与前端配套关系

| 场景 | 后端前缀 | 管理后台 | Portal Web |
|------|----------|----------|------------|
| 本机开发 | `/dev-api` | `npm run dev` | `.env.development` |
| 预发布 | `/stage-api` | `npm run build:stage` | 自定义 mode |
| 生产 | `/prod-api` | `npm run build:prod` | `.env.production` |
| Docker | `/docker-api` | `npm run build:docker` | 通常不单独部署 |

部署时最容易出错的地方，就是前端 API 前缀和后端 `APP_ROOT_PATH` 不一致。

---

## 9. 部署后验证

建议至少验证以下内容：

1. 后端进程是否正常启动
2. `http://host:9099/docs` 是否可访问（如果未禁用 Swagger）
3. 登录接口是否返回正常
4. 后台前端能否登录
5. Portal 接口如 `/portal/article/list` 是否正常

---

## 10. 常见部署问题

### Swagger 访问不了

检查 `.env.prod`：

- `APP_DISABLE_SWAGGER`
- `APP_DISABLE_REDOC`

### 前端 404 / 502

优先检查：

- 前端请求前缀是否和 `APP_ROOT_PATH` 一致
- Nginx 的 `proxy_pass` 是否以 `/` 结尾
- 后端端口是否真的在监听 `9099`

### 数据库连不上

检查：

- `DB_TYPE`
- `DB_HOST`
- `DB_PORT`
- 是否导入了正确 SQL
- PostgreSQL 场景是否安装了 `requirements-pg.txt`

### AI 模块页面是空的

后端现在会在 `ai_models` 为空时自动初始化默认模型模板。

如果你仍然看到空列表，请检查：

- 数据库用户是否有写入 `ai_models` 权限
- 启动时日志里是否出现 “AI 默认模型初始化完成”
