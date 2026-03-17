# ruoyi-fastapi-desktop-web（独立电脑端 Web 前端）

这是一个**新的、独立的桌面端网页前端项目**（Vite + React + TypeScript），核心目标只有一件事：

> **调用你的 FastAPI 后端接口拿到数据，然后把数据渲染成可用的桌面端 UI。**

已内置示例：

- 登录：`/captchaImage` + `/login`
- 用户信息：`/getInfo`
- 列表渲染：`GET /system/user/list` → `rows/total` → 表格 + 分页 + 行详情(JSON)

---

## 1) 启动后端（本机 dev）

按照后端说明启动：`../ruoyi-fastapi-backend/README.md`

默认：`http://127.0.0.1:9099`

---

## 2) 启动前端

```bash
cd ruoyi-fastapi-desktop-web
npm install
npm run dev
```

浏览器打开：`http://localhost:5175`

---

## 3) 接口代理与环境变量

开发环境默认：

- `VITE_API_BASE=/dev-api`
- `VITE_API_TARGET=http://127.0.0.1:9099`

前端发起的请求会走：`/dev-api/**`，由 Vite 代理到后端并去掉前缀（见 `vite.config.ts`）。

---

## 4) 你真正要改/扩展的地方（渲染逻辑）

- 请求封装：`src/api/http.ts`
- 新增业务接口：`src/api/*.ts`
- “拿数据 → 渲染”的示例页：`src/pages/UsersPage.tsx`
- 通用表格组件：`src/ui/DataTable.tsx`
