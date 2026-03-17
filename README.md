# DeskOps（SoftwareHub 软件库管理）

这是一个围绕“软件库 + 教程文章 + 多端展示”搭建的业务项目，当前仓库包含：

- 后端 API：`ruoyi-fastapi-backend`
- 管理后台：`ruoyi-fastapi-frontend`
- Portal Web：`ruoyi-fastapi-desktop-web`
- uni-app 客户端：`ruoyi-fastapi-app`
- 自动化测试：`ruoyi-fastapi-test`

---

## 项目结构

| 目录 | 作用 | 默认本机地址 |
|------|------|--------------|
| `ruoyi-fastapi-backend/` | FastAPI 后端，负责管理端和 Portal API | `http://127.0.0.1:9099` |
| `ruoyi-fastapi-frontend/` | 管理后台（Vue3 + Element Plus） | `http://localhost:80` |
| `ruoyi-fastapi-desktop-web/` | Portal Web（React + TypeScript） | `http://localhost:5175` |
| `ruoyi-fastapi-app/` | uni-app（H5 / 小程序 / APP） | H5 默认 `http://localhost:9090` |
| `ruoyi-fastapi-test/` | pytest + Playwright 测试套件 | 依赖上面服务 |

---

## 启动顺序

推荐按下面顺序启动本机开发环境：

1. 初始化数据库
2. 启动 Redis
3. 启动后端 `ruoyi-fastapi-backend`
4. 启动管理后台 `ruoyi-fastapi-frontend`
5. 按需启动 Portal Web / App / 测试

最常用的本机开发组合：

```bash
# 1) 后端（推荐：直接用统一脚本，默认 dev）
.\2-backend-start.bat

# 2) 管理后台
cd ../ruoyi-fastapi-frontend
npm install
npm run dev

# 3) Portal Web（可选）
cd ../ruoyi-fastapi-desktop-web
npm install
npm run dev

# 4) App H5（可选）
cd ../ruoyi-fastapi-app
pnpm install
pnpm dev:h5
```

---

## 初始化数据

首次运行至少需要执行以下 SQL：

1. `ruoyi-fastapi-backend/sql/ruoyi-fastapi.sql`
2. `ruoyi-fastapi-backend/sql/ruoyi-fastapi-software.sql`
3. `ruoyi-fastapi-backend/sql/ruoyi-fastapi-kb.sql`

默认管理员账号：

- 用户名：`admin`
- 密码：`admin123`

---

## 环境切换总览

### 后端

后端统一优先走本地 `dev`，并按 `--env > APP_ENV > dev` 选择 `ruoyi-fastapi-backend/.env.<name>`：

| 环境 | 配置文件 | 典型用途 |
|------|----------|----------|
| `dev` | `.env.dev` | 本机开发 |
| `prod` | `.env.prod` | 本机模拟生产 / 正式部署 |
| `dockermy` | `.env.dockermy` | Docker + MySQL |
| `dockerpg` | `.env.dockerpg` | Docker + PostgreSQL |
| 自定义 | `.env.<custom>` | 例如 `stage`、`test` |

示例：

```bash
.\2-backend-start.bat
.\2-backend-start.bat prod
.\2-backend-start.bat dockermy
.\2-backend-start.bat dockerpg
```

说明：

- 日常开发优先使用 `.env.dev`
- 本地开发确认没问题后，再切换到 `prod` / Docker / 其他部署环境
- 如果指定环境文件不存在，后端会直接报错退出，避免走错线路

### 管理后台

`ruoyi-fastapi-frontend` 当前内置 4 套模式：

| 模式 | 配置文件 | 命令 | API 前缀 |
|------|----------|------|----------|
| 开发 | `.env.development` | `npm run dev` | `/dev-api` |
| 预发布 | `.env.staging` | `npm run build:stage` | `/stage-api` |
| 生产 | `.env.production` | `npm run build:prod` | `/prod-api` |
| Docker | `.env.docker` | `npm run build:docker` | `/docker-api` |

### Portal Web

`ruoyi-fastapi-desktop-web` 当前内置：

| 模式 | 配置文件 | 用途 |
|------|----------|------|
| 开发 | `.env.development` | 本机代理到后端 |
| 生产 | `.env.production` | 静态部署，通常走 `/prod-api` |

如需额外模式，可新增 `.env.<mode>` 并用 Vite 的 `--mode` 机制启动或构建。

### App

`ruoyi-fastapi-app` 没有独立 `.env.*`，当前通过 `src/config.js` 切换后端地址：

- 本机开发：`baseUrl = "http://localhost:9099"`
- 生产部署：`baseUrl = "https://your-domain.com/prod-api"`

---

## Docker 快速启动

仓库根目录已经提供两套 compose：

| 文件 | 说明 | 暴露地址 |
|------|------|----------|
| `docker-compose.my.yml` | MySQL + Redis + 后端 + 管理后台 | 后端 `19099`，后台 `12580` |
| `docker-compose.pg.yml` | PostgreSQL + Redis + 后端 + 管理后台 | 后端 `19099`，后台 `12580` |

MySQL 版本示例：

```bash
docker compose -f docker-compose.my.yml up -d --build
```

Windows 下也可以使用辅助脚本：

```powershell
.\scripts\dev\start-dockermy-and-check.ps1
```

---

## 典型使用流程

1. 用管理后台维护分类、软件、文章等业务数据
2. 用 Portal Web 或 App 验证对外展示效果
3. 用 `ruoyi-fastapi-test` 运行接口和 UI 回归
4. 根据部署目标选择本机部署或 Docker 部署

---

## 文档导航

- [后端使用说明](./ruoyi-fastapi-backend/README.md)
- [后端部署说明](./ruoyi-fastapi-backend/DEPLOY.md)
- [管理后台使用说明](./ruoyi-fastapi-frontend/README.md)
- [管理后台部署说明](./ruoyi-fastapi-frontend/DEPLOY.md)
- [Portal Web 使用说明](./ruoyi-fastapi-desktop-web/README.md)
- [Portal Web 部署说明](./ruoyi-fastapi-desktop-web/DEPLOY.md)
- [App 使用说明](./ruoyi-fastapi-app/README.md)
- [App 部署说明](./ruoyi-fastapi-app/DEPLOY.md)
- [测试说明](./ruoyi-fastapi-test/README.md)

---

## 技术栈

- 后端：FastAPI + SQLAlchemy + Redis + MySQL / PostgreSQL
- 管理后台：Vue 3 + Element Plus + Vite
- Portal Web：React 19 + TypeScript + Vite
- App：uni-app + Vue 3 + Tailwind CSS
- 测试：pytest + requests + Playwright

---

## 版权说明

本项目基于 MIT 协议开源，允许商业使用，但请保留原作者版权信息。
