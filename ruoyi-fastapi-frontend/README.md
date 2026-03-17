# ruoyi-fastapi-frontend（后台管理系统）

本目录是 **后台管理系统 Web**（Vue3 + ElementPlus + Vite）。

> 你当前的核心业务是「SoftwareHub：软件库管理系统」，后台管理主要在「软件管理」菜单下维护分类/软件/软件详情。

---

## 产品化增强（SoftwareHub）

- 首页看板：KPI + 发布状态图 + 最近更新 + 草稿待处理 + 维度分布（标签/许可证/平台）+ 数据质量（缺字段/缺配置）提示。
- 软件列表：新增“数据质量”快速筛选 + 质量中心抽屉，一键定位缺下载/缺许可证/缺图标等条目并快速修复。
- 筛选体验：许可证/标签支持 facets 下拉（带数量），并支持按官网/仓库 URL 模糊过滤。
- 批量操作：支持批量上架/下架/设为草稿（表格模式多选）。
- 批量治理：支持批量移动分类、批量标签治理（追加/移除/覆盖，自动去重与规范化）。
- 排序增强：列表支持按更新时间/ID/排序字段自定义排序。
- 软件详情页：独立详情页（Markdown 预览 + 下载/资源表格 + 数据质量提示）。
- 教程管理：教程/博客文章（Markdown）维护 + 关联软件（顺序可调），Portal 公开展示（`ruoyi-fastapi-desktop-web`）。
- Markdown 导入：介绍/使用说明支持从本地导入 `.md/.txt` 文件并填充到编辑框（前端读取，0 后端改动）。
- 软件导入：支持按模板批量导入软件基础信息（可选更新已存在记录）。
- 软件导出：支持按当前筛选条件导出 Excel，便于备份/审计/对外同步。

---

## 页面职责（建议约定）

- `软件列表（/software/item）`：查询/筛选/批量治理/导入导出/快速编辑（弹窗）。
- `软件详情（/software/detail）`：只读预览（从列表“详情/预览”进入）。
- `软件编辑（/software/edit）`：全屏编辑页（从详情页“编辑”进入，避免跳回列表弹窗造成割裂）。
- `教程管理（/kb/article）`：文章列表（搜索/发布下线/删除/详情）。
- `教程编辑（/kb/article/edit）`：全屏编辑页（Markdown 编辑/预览 + 关联软件排序）。

---

## 开发启动（本机）

### 1) 环境依赖

- Node.js ≥ 18（推荐 20+）
- npm / pnpm / yarn 任一（本项目带 `package-lock.json`，默认按 npm 使用）

### 2) 启动前置条件

请先确保后端已启动（默认）：

- 后端：`http://127.0.0.1:9099`

开发环境 API 前缀（见 `.env.development`）：

- `VITE_APP_BASE_API = '/dev-api'`

并且 `vite.config.js` 已配置代理：

- `/dev-api` → `http://127.0.0.1:9099`（会自动把 `/dev-api` 前缀去掉再转发）

如果后端端口不是 `9099`，请修改 `vite.config.js` 的 `server.proxy['/dev-api'].target`。

### 3) 安装依赖 & 启动

进入目录：

```bash
cd ruoyi-fastapi-frontend
```

安装依赖：

```bash
npm install
```

启动开发服务器（默认端口 `80`）：

```bash
npm run dev
```

访问：

- `http://localhost:80`

默认账号密码（初始化 SQL 自带）：

- 账号：`admin`
- 密码：`admin123`

### 4) 品牌配置（可选）

在 `.env.*` 中可自定义后台的标题/Logo 文本/登录页底部文字：

- `VITE_APP_TITLE`：页面标题（浏览器 tab）与系统名称
- `VITE_APP_LOGO_TEXT`：侧边栏 Logo 文本（为空时回退为 `VITE_APP_TITLE`）
- `VITE_APP_FOOTER`：登录页底部文字（可留空）

---

## 部署（静态资源 + 反向代理）

生产部署通常是：构建出静态文件 `dist/`，交给 Nginx（或任意静态服务器）托管，并将 `/prod-api` 反向代理到后端。

### 1) 构建

```bash
cd ruoyi-fastapi-frontend
npm ci
npm run build:prod
```

产物目录：

- `dist/`

### 2) 与后端的路径约定（重要）

前端生产环境默认（见 `.env.production`）：

- `VITE_APP_BASE_API = '/prod-api'`

后端生产环境默认（见 `ruoyi-fastapi-backend/.env.prod`）：

- `APP_ROOT_PATH = '/prod-api'`

因此建议使用 Nginx：

- 托管前端静态资源在 `/`
- 将 `/prod-api/` 代理到后端，并把 `/prod-api` 前缀去掉再转发

### 3) Nginx 示例

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

### 1) 端口 80 被占用

修改 `vite.config.js`：

- `server.port: 80` → 换成可用端口（如 `5173`）

### 2) 登录/接口 502

通常是本机代理/抓包软件影响请求链路。建议：

- 先确认后端 `http://127.0.0.1:9099` 可访问
- 再确认 `vite.config.js` 的代理目标端口与后端一致
