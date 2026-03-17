# ruoyi-fastapi-desktop-web（Portal Web 使用说明）

本目录是独立的使用端 Web 前端，面向普通用户展示：

- 软件列表 / 搜索 / 筛选
- 软件详情 / 下载
- 教程文章列表 / 详情

---

## 1. 环境要求

- Node.js 18+，推荐 20+
- npm 为默认包管理器

---

## 2. 环境切换

项目当前内置：

| 模式 | 配置文件 | 说明 |
|------|----------|------|
| 开发 | `.env.development` | 本机开发，走 Vite 代理 |
| 生产 | `.env.production` | 构建静态文件，通常配合 Nginx |

### 当前关键变量

| 变量 | 作用 |
|------|------|
| `VITE_APP_TITLE` | 页面标题 |
| `VITE_API_BASE` | 前端请求前缀 |
| `VITE_API_TARGET` | 开发模式代理目标地址 |

### 默认值

- 开发：`VITE_API_BASE=/dev-api`
- 开发：`VITE_API_TARGET=http://127.0.0.1:9099`
- 生产：`VITE_API_BASE=/prod-api`

如果需要额外环境，例如 `stage`，可以新增 `.env.stage`，然后使用 Vite mode：

```bash
npx vite --mode stage
npx vite build --mode stage
```

---

## 3. 本机开发启动

```bash
cd ruoyi-fastapi-desktop-web
npm install
npm run dev
```

默认地址：

- `http://localhost:5175`

开发环境会把：

- `/dev-api/*` 代理到 `http://127.0.0.1:9099`

---

## 4. 与后端的关系

Portal Web 不直接写死完整后端地址，而是通过前缀配套。

| 场景 | Portal 前缀 | 后端前缀 |
|------|-------------|----------|
| 本机开发 | `/dev-api` | `/dev-api` |
| 生产部署 | `/prod-api` | `/prod-api` |
| 自定义环境 | 例如 `/stage-api` | 例如 `/stage-api` |

如果你改了 Portal Web 的 `VITE_API_BASE`，记得同步后端 `APP_ROOT_PATH` 和 Nginx 转发规则。

---

## 5. 常用命令

```bash
npm run dev
npm run build
npm run preview
npm run typecheck
npm run lint
```

---

## 6. 构建产物

```bash
npm run build
```

输出目录：

- `dist/`

构建命令会先执行 TypeScript 构建检查，再执行 Vite 打包。

---

## 7. 你最常会改的目录

- `src/api/`：接口封装
- `src/pages/`：页面
- `src/layout/`：布局
- `src/ui/`：通用 UI 组件

---

## 8. 常见问题

### 页面能打开，但数据请求失败

先检查：

1. 后端是否启动
2. `.env.development` 的 `VITE_API_TARGET` 是否正确
3. 后端是否允许对应接口访问

### 构建后刷新路由 404

部署时需要 Nginx 做 SPA 回退到 `index.html`。

### 需要第三套环境

新增 `.env.<name>` 后，用 Vite 的 `--mode` 启动或构建即可。

---

## 9. 进一步阅读

- [部署说明](./DEPLOY.md)
- [仓库总说明](../README.md)
