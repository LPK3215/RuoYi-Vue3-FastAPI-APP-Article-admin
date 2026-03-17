# DeskOps 软件库管理后台（ruoyi-fastapi-frontend）部署文档

本目录为 **后台管理系统 Web**（Vue3 + Vite + Element Plus）。

> 配套后端：`ruoyi-fastapi-backend`（默认 `http://127.0.0.1:9099`）。

---

## 环境要求

- Node.js 18+（推荐 20+）
- npm / pnpm / yarn 任一（本项目自带 `package-lock.json`，默认按 npm 使用）

---

## 本机开发

### 1) 安装依赖

```bash
cd ruoyi-fastapi-frontend
npm install
```

### 2) 启动开发服务器

```bash
npm run dev
```

默认端口由 `vite.config.js` 指定为 `80`，访问：

- `http://localhost:80`

### 3) API 代理（重要）

开发环境 API 前缀在 `.env.development`：

```ini
VITE_APP_BASE_API = '/dev-api'
```

并且 `vite.config.js` 已配置代理：

- `/dev-api` → `http://127.0.0.1:9099`（自动去掉 `/dev-api` 前缀再转发）

如果后端端口不是 `9099`，请修改 `vite.config.js` 里的 `server.proxy['/dev-api'].target`。

### 4) 品牌配置（可选）

在 `.env.*` 中可自定义后台标题/Logo 文本/登录页底部文字：

- `VITE_APP_TITLE`：页面标题（浏览器 tab）与系统名称
- `VITE_APP_LOGO_TEXT`：侧边栏 Logo 文本（为空时回退为 `VITE_APP_TITLE`）
- `VITE_APP_FOOTER`：登录页底部文字（可留空）

---

## 生产构建

### 1) 选择环境

常用构建命令（见 `package.json`）：

```bash
npm run build:prod    # 生产
npm run build:stage   # 预发布/测试
npm run build:docker  # Docker 环境
```

构建产物输出到：

- `ruoyi-fastapi-frontend/dist/`

### 2) 与后端的路径约定（重要）

生产环境前端默认（见 `.env.production`）：

```ini
VITE_APP_BASE_API = '/prod-api'
```

后端生产环境建议（见 `ruoyi-fastapi-backend/.env.prod`）：

```ini
APP_ROOT_PATH = '/prod-api'
```

建议使用 Nginx：

- 静态资源托管在 `/`
- `/prod-api/` 反向代理到后端 `9099`，并去掉 `/prod-api` 前缀再转发

---

## Nginx 部署示例

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

## 主题说明（UI）

- 主题模式（暗黑/亮色）切换会同步影响侧边栏风格，避免“页面亮色但菜单固定黑色”的割裂感。
- 下拉类组件（Select/Dropdown/Autocomplete/Cascader 等）已统一为更一致的暗黑/亮色外观。

---

## 常见问题

### 1) 端口 80 被占用

修改 `vite.config.js`：

- `server.port: 80` → 改为可用端口（如 `5173`）

### 2) 刷新页面 404

这是 SPA 路由问题，需要 Nginx 的 `try_files`：

```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

### 3) 默认登录信息

初始化 SQL 自带默认管理员账号：

- 用户名：`admin`
- 密码：`admin123`
