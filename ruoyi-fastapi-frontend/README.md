# ruoyi-fastapi-frontend（管理后台使用说明）

本目录是管理后台前端，主要用于：

- 分类管理
- 软件管理
- 教程 / 文章管理
- 数据导入导出
- 管理端权限操作

---

## 1. 环境要求

- Node.js 18+，推荐 20+
- npm 为默认包管理器

---

## 2. 环境切换

当前已经内置 4 套环境：

| 模式 | 配置文件 | 命令 | API 前缀 |
|------|----------|------|----------|
| 开发 | `.env.development` | `npm run dev` | `/dev-api` |
| 预发布 | `.env.staging` | `npm run build:stage` | `/stage-api` |
| 生产 | `.env.production` | `npm run build:prod` | `/prod-api` |
| Docker | `.env.docker` | `npm run build:docker` | `/docker-api` |

说明：

- 开发模式通过 Vite 代理访问后端
- 其他模式都是构建静态资源，由 Nginx 或静态服务器提供

---

## 3. 本机开发启动

### 安装依赖

```bash
cd ruoyi-fastapi-frontend
npm install
```

### 启动开发服务器

```bash
npm run dev
```

默认访问：

- `http://localhost:5174`

默认会把：

- `/dev-api` 代理到 `http://127.0.0.1:9099`

如果后端端口或代理目标不是 `9099`，请修改：

- `.env.development` 中的 `VITE_DEV_PORT`
- `.env.development` 中的 `VITE_DEV_PROXY_TARGET`

---

## 4. 与后端如何配套

管理后台和后端的前缀必须一一对应：

| 前端模式 | 前端前缀 | 后端 `APP_ROOT_PATH` |
|----------|----------|----------------------|
| 开发 | `/dev-api` | `/dev-api` |
| 预发布 | `/stage-api` | `/stage-api` |
| 生产 | `/prod-api` | `/prod-api` |
| Docker | `/docker-api` | `/docker-api` |

如果你使用 `build:stage`，但后端没有 `stage` 环境，就需要：

1. 新建 `ruoyi-fastapi-backend/.env.stage`
2. 把 `APP_ROOT_PATH` 改成 `/stage-api`
3. 用 `python app.py --env stage` 启动

---

## 5. 常用命令

```bash
npm run dev
npm run build:prod
npm run build:stage
npm run build:docker
npm run preview
```

Windows 还提供了辅助脚本：

- `bin/package.bat`：安装依赖
- `bin/run-web.bat`：启动开发环境
- `bin/build.bat`：构建生产包

---

## 6. 构建产物

所有构建结果输出到：

- `ruoyi-fastapi-frontend/dist/`

生产部署一般把 `dist/` 交给 Nginx 托管。

---

## 7. 品牌与界面配置

可在 `.env.*` 中修改：

- `VITE_APP_TITLE`
- `VITE_APP_LOGO_TEXT`
- `VITE_APP_FOOTER`

适合用于：

- 更换系统标题
- 更换侧边栏 Logo 文案
- 更换登录页底部说明

---

## 8. 默认登录信息

- 用户名：`admin`
- 密码：`admin123`

---

## 9. 常见问题

### 开发端口被占用

修改 `.env.development` 中：

- `VITE_DEV_PORT`

### 登录 502 / 接口异常

先确认：

1. 后端是否已经启动
2. 后端端口是否还是 `9099`
3. `.env.development` 里的 `VITE_DEV_PROXY_TARGET` 是否正确

### 构建后刷新页面 404

这是 SPA 常见问题，部署时需要 Nginx 配置：

```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

---

## 10. 进一步阅读

- [部署说明](./DEPLOY.md)
- [仓库总说明](../README.md)
