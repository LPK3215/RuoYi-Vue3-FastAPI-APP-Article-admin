# ruoyi-fastapi-backend（后端）

本目录是 **FastAPI 后端**，同时提供：

- 后台管理 API（管理端登录后使用）
- Portal API（用户端/公开展示使用）

> 本项目优先按 **本机方式**运行（不依赖 Docker）。

---

## 开发启动（本机）

### 1) 环境依赖

- Python ≥ 3.10
- MySQL ≥ 5.7（或 MariaDB）
- Redis ≥ 6.2

### 2) 初始化数据库（必须）

1. 创建数据库（默认名见 `.env.dev`：`DB_DATABASE = 'ruoyi-fastapi'`）
2. 依次导入 SQL：
   - 基础表/权限/字典：`sql/ruoyi-fastapi.sql`
   - 软件库业务表 + 菜单：`sql/ruoyi-fastapi-software.sql`
   - 教程/知识库（文章 + 关联软件 + 菜单）：`sql/ruoyi-fastapi-kb.sql`

> 如果你是“已有库升级”，并且只想同步软件菜单顺序/授权，可单独执行：`sql/ruoyi-fastapi-software-menu-migrate.sql`。

### 3) Redis（必须）

确保 Redis 可用，且数据库编号与 `.env.dev` 一致（默认：`REDIS_DATABASE = 2`）。

Windows 可选脚本：

- 下载/准备：`../scripts/dev/setup-redis.ps1`
- 启动：`../scripts/dev/start-redis.ps1`

### 4) 安装依赖 & 启动

进入目录：

```bash
cd ruoyi-fastapi-backend
```

创建虚拟环境（示例）：

```bash
python -m venv .venv
```

- Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py --env dev
```

- macOS/Linux：

```bash
source .venv/bin/activate
pip install -r requirements.txt
python app.py --env dev
```

启动成功后默认：

- API：`http://127.0.0.1:9099`
- Swagger：`http://127.0.0.1:9099/docs`

---

## SoftwareHub（软件库）接口增强（后台）

### 1) 首页看板（聚合接口）

用于后台首页展示 KPI/维度分布/数据质量/最近更新/草稿待处理：

- `GET /tool/software/item/overview?limit=12&recentLimit=6`

### 1.1) 筛选项聚合（facets）

用于构建后台筛选 UI（标签/许可证/作者/平台等）：

- `GET /tool/software/item/facets?limit=50`

### 2) 软件列表排序（list 接口）

`/tool/software/item/list` 支持排序参数：

- `orderByColumn`：例如 `updateTime`
- `isAsc`：`ascending` / `descending`

示例：

- `GET /tool/software/item/list?pageNum=1&pageSize=10&orderByColumn=updateTime&isAsc=descending`

### 3) 数据质量筛选（list 接口）

`/tool/software/item/list` 支持“缺字段/缺配置”的快速筛选（1=有，0=无）：

- `hasDownloads` / `hasLicense` / `hasIcon` / `hasOfficialUrl` / `hasShortDesc` / `hasTags` / `hasResources`

示例：

- 缺下载：`hasDownloads=0`
- 缺许可证：`hasLicense=0`

---

### 3.1) URL 精准筛选（list 接口）

`/tool/software/item/list` 支持按 URL 过滤（便于重复治理/快速定位）：

- `officialUrl`：官网地址（模糊匹配）
- `repoUrl`：仓库地址（模糊匹配）

---

### 4) 导出软件列表（Excel）

用于按当前筛选条件导出软件列表（Excel）：

- `POST /tool/software/item/export`

说明：

- 请求体为 `application/x-www-form-urlencoded`（与前端通用 `proxy.download` 保持一致）
- 可传入与 `/tool/software/item/list` 相同的筛选参数（含数据质量筛选）
- 响应为 `application/octet-stream` 的流式 Excel 文件

---

### 5) 批量上架/下架（发布状态）

- `PUT /tool/software/item/batchChangePublishStatus`

请求示例（JSON）：

```json
{
  "softwareIds": [1, 2, 3],
  "publishStatus": "1"
}
```

其中 `publishStatus`：`0` 草稿 / `1` 上架 / `2` 下架。

---

### 6) 批量移动分类

- `PUT /tool/software/item/batchMoveCategory`

请求示例（JSON）：

```json
{
  "softwareIds": [1, 2, 3],
  "categoryId": 100
}
```

---

### 7) 批量标签治理（追加/移除/覆盖）

- `PUT /tool/software/item/batchManageTags`

请求示例（JSON）：

```json
{
  "softwareIds": [1, 2, 3],
  "action": "append",
  "tags": "cli,dev\nops"
}
```

其中 `action`：

- `append`：追加（去重）
- `remove`：移除
- `replace`：覆盖（允许 tags 为空表示清空）

---

### 8) 导入软件（Excel）

用于批量导入软件基础信息（不含下载/资源明细）：

- `POST /tool/software/item/importTemplate`：下载导入模板
- `POST /tool/software/item/importData?updateSupport=0|1`：上传 Excel 批量导入

说明：

- 若填写“软件ID”，则按软件ID更新（需要 `updateSupport=1`）
- 未填写“软件ID”，按新增处理

---

## 教程/知识库（KB）模块

> 用于“对外展示”的教程/博客文章：文章内容为 Markdown，并可关联多个软件（Portal 详情页会展示关联软件并跳转到软件下载页）。
>
> Portal 展示侧当前由 `ruoyi-fastapi-desktop-web` 通过 `/portal/article/**` 接口拉取数据并渲染（无需登录）。

### 1) 管理端接口（需要登录）

- `GET /tool/kb/article/list`：分页列表（支持 keyword/tag/publishStatus/status）
- `GET /tool/kb/article/{articleId}`：详情（含 `softwareIds`）
- `POST /tool/kb/article`：新增
- `PUT /tool/kb/article`：更新
- `PUT /tool/kb/article/changePublishStatus`：发布/下线/草稿
- `DELETE /tool/kb/article/{articleIds}`：删除（软删，逗号分隔）

### 2) Portal 接口（公开）

- `GET /portal/article/list`：分页列表（仅返回“已发布/正常/未删除”）
- `GET /portal/article/{articleId}`：详情（仅返回“已发布/正常/未删除”，并包含“已上架”的关联软件列表）

## 部署（非 Docker）

### 1) 生产配置（必须）

修改：`.env.prod`

重点关注：

- `DB_HOST / DB_PORT / DB_USERNAME / DB_PASSWORD / DB_DATABASE`
- `REDIS_HOST / REDIS_PORT / REDIS_PASSWORD / REDIS_DATABASE`
- `APP_PORT`（默认 `9099`）
- `APP_ROOT_PATH`（默认 `/prod-api`，用于配合 Nginx 反代前缀）
- `APP_RELOAD=false`（生产环境不要开热重载）
- `APP_DISABLE_SWAGGER=true`（默认关闭 Swagger）

### 2) 初始化数据库（首次部署必须）

同开发启动：执行 `sql/ruoyi-fastapi.sql` + `sql/ruoyi-fastapi-software.sql`。

### 3) 启动方式

最简单（推荐先跑通）：

```bash
python app.py --env prod
```

如需 `uvicorn`（更可控）：

> 注意：直接运行 `uvicorn` 时无法使用 `--env` 这种自定义参数，需要用环境变量指定环境。

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

### 4) Nginx 反向代理（推荐）

典型部署建议：

- 管理端静态资源：`/`（来自 `ruoyi-fastapi-frontend/dist`）
- API：`/prod-api/` 代理到后端 `9099`，并 **去掉** `/prod-api` 前缀再转发

示例（注意 `proxy_pass` 结尾的 `/`）：

```nginx
server {
  listen 80;
  server_name your-domain.com;

  root /var/www/softwarehub-admin;
  index index.html;

  location / {
    try_files $uri $uri/ /index.html;
  }

  location /prod-api/ {
    proxy_pass http://127.0.0.1:9099/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

---

## 常见问题

### 1) 登录被锁定（密码输错太多次）

锁定信息在 Redis（db=2）里。可删除这些 Key 解锁：

- `account_lock:admin`
- `password_error_count:admin`

### 2) 改了代码但接口没变化

`.env.dev` 默认 `APP_RELOAD = false`，需要手动重启后端进程。
