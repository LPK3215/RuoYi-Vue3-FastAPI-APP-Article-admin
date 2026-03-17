# DeskOps（SoftwareHub 软件库管理）

本仓库是一个面向业务的“软件资源管理平台”，包含：

- **后台管理**：分类/软件/上架下架/内容维护（`ruoyi-fastapi-frontend`）
- **使用端 Web（Portal）**：软件库浏览/搜索/筛选/详情（`ruoyi-fastapi-desktop-web`）
- **教程/博客（Portal）**：文章列表/详情（Markdown 渲染）+ 关联软件跳转（`ruoyi-fastapi-desktop-web`）
- **使用端 App（可选）**：uni-app（H5/小程序/APP）（`ruoyi-fastapi-app`）

### 功能模块

#### 后台管理（管理员）

| 功能 | 说明 |
|------|------|
| 分类管理 | 软件分类的增删改查 |
| 软件管理 | 软件基础信息、富文本说明（Markdown）、多平台下载地址管理 |
| 上架/下架 | 控制软件资源的展示状态 |
| 批量治理 | 批量移动分类、批量标签治理（追加/移除/覆盖） |
| 数据质量中心 | 缺项统计 + 一键定位（缺下载/缺许可证/缺图标等） |
| 软件详情页 | 独立详情页（Markdown 预览 + 下载/资源表格） |
| 教程管理 | 教程/博客文章（Markdown）+ 关联软件（顺序可调） |
| 软件导出 | 按当前筛选条件导出 Excel |
| 展示模式 | 支持表格/卡片两种视图切换 |

#### 用户端（普通用户）

| 功能 | 说明 |
|------|------|
| 软件浏览 | 查看已上架的软件资源 |
| 搜索筛选 | 按分类、名称等条件筛选软件 |
| 软件详情 | 查看软件完整信息和下载链接 |
| 教程文章 | 浏览已发布教程文章（Markdown 渲染，底部关联软件跳转下载） |

### 项目结构

| 目录 | 说明 |
|------|------|
| `ruoyi-fastapi-backend/` | FastAPI 后端（后台管理 API + 用户端 API） |
| `ruoyi-fastapi-frontend/` | 后台管理系统（Vue3 + Element Plus + Vite） |
| `ruoyi-fastapi-desktop-web/` | 使用端 Web（Portal，React + TypeScript + Vite + 自定义 UI） |
| `ruoyi-fastapi-app/` | 使用端 App（可选，uni-app，支持 H5/小程序/APP） |
| `ruoyi-fastapi-test/` | 自动化测试（pytest + requests + Playwright） |

---

## 快速启动

### 环境要求

- **Python**: 3.10+
- **Node.js**: 18+
- **MySQL**: 5.7+ 或 PostgreSQL 13+
- **Redis**: 6.0+

### 启动步骤

```bash
# 1. 克隆项目
# git clone <your-repo-url>
cd RuoYi-Vue3-FastAPI

# 2. 初始化数据库（首次必须）
# - ruoyi-fastapi-backend/sql/ruoyi-fastapi.sql
# - ruoyi-fastapi-backend/sql/ruoyi-fastapi-software.sql
# - ruoyi-fastapi-backend/sql/ruoyi-fastapi-kb.sql

# 3. 启动后端
cd ruoyi-fastapi-backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
# 配置 .env.dev 文件（数据库、Redis）
python app.py --env dev

# 4. 启动后台管理（管理员端）
cd ruoyi-fastapi-frontend
npm install
npm run dev

# 5. 启动使用端 Web（Portal，可选）
cd ruoyi-fastapi-desktop-web
npm install
npm run dev

# 6. 启动使用端 App H5（可选）
cd ruoyi-fastapi-app
pnpm install
pnpm dev:h5
```

### 默认登录信息

- **地址**: http://localhost:80
- **账号**: admin
- **密码**: admin123

---

## 部署文档

各子项目的详细部署文档：

- [后端部署](./ruoyi-fastapi-backend/DEPLOY.md)
- [前端部署](./ruoyi-fastapi-frontend/DEPLOY.md)
- [桌面端部署](./ruoyi-fastapi-desktop-web/DEPLOY.md)
- [测试说明](./ruoyi-fastapi-test/README.md)

---

## 技术栈

**后端**
- FastAPI + SQLAlchemy + MySQL/PostgreSQL + Redis + OAuth2 & JWT

**前端**
- Vue3 + Element Plus + Vite + Pinia + Vue Router

**桌面端**
- React 19 + TypeScript + Vite + TanStack Query + TanStack Table + 自定义 UI

**测试**
- pytest + requests + Playwright

---

## 版权说明

本项目基于 MIT 协议开源，允许商业使用，但请保留原作者版权信息。
