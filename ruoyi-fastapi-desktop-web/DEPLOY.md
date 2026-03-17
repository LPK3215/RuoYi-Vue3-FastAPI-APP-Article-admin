# DeskOps 使用端 Web（ruoyi-fastapi-desktop-web）部署文档

本目录为 **独立的使用端 Web（Portal）前端**（React + TypeScript + Vite），用于对接 `ruoyi-fastapi-backend` 的 `/portal/**` 接口并渲染：

- 软件库（列表/筛选/详情/下载）
- 教程/博客（文章列表/详情，Markdown 渲染 + 关联软件跳转）

---

## 环境要求

- Node.js 18+（推荐 20+）
- npm / pnpm / yarn 任一（本项目自带 `package-lock.json`，默认按 npm 使用）

---

## 本机开发

### 1) 安装依赖

```bash
cd ruoyi-fastapi-desktop-web
npm install
```

### 2) 配置环境变量

项目提供 `.env.example`，也可直接使用默认的 `.env.development` / `.env.production`。

关键变量（与 `vite.config.ts` 一致）：

```ini
VITE_APP_TITLE=DeskOps Portal
VITE_API_BASE=/dev-api
VITE_API_TARGET=http://127.0.0.1:9099
```

说明：

- `VITE_API_BASE`：前端请求前缀（开发环境走 Vite 代理）
- `VITE_API_TARGET`：代理目标后端地址（仅开发环境需要）

### 3) 启动

```bash
npm run dev
```

默认端口为 `5175`（见 `vite.config.ts`），访问：

- `http://localhost:5175`

---

## 生产构建 & 静态部署

### 1) 构建

```bash
cd ruoyi-fastapi-desktop-web
npm ci
npm run build
```

产物目录：

- `ruoyi-fastapi-desktop-web/dist/`

### 2) Nginx 示例（静态资源 + API 反代）

生产环境建议让前端直接请求 `/prod-api/**`，由 Nginx 反代到后端：

- 前端 `.env.production`：`VITE_API_BASE=/prod-api`
- 后端 `.env.prod`：`APP_ROOT_PATH='/prod-api'`

```nginx
server {
  listen 80;
  server_name your-domain.com;

  root /var/www/deskops;
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

## 代码检查

```bash
npm run typecheck
npm run lint
```

---

## UI 说明（下拉框）

为避免浏览器原生 `<select>` 在不同主题/平台下样式不一致，系统内下拉框采用自绘 Select（Portal + Popover），并已修复「筛选-许可证」弹层被裁切的问题。
