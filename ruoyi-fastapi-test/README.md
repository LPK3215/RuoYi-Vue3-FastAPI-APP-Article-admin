# SoftwareHub 测试套件（ruoyi-fastapi-test）

本目录为 **自动化测试套件**，包含：

- API 测试（`requests`）
- UI/E2E 测试（Playwright）

> 部分 UI 测试会在端口未启动时自动 `skip`，避免在未启动服务的情况下误报失败。

---

## 依赖安装

建议使用 Python 3.10+。

```bash
cd ruoyi-fastapi-test
pip install -r requirements.txt
playwright install
```

---

## 本机运行（推荐）

### 1) 启动后端

按后端说明启动：`../ruoyi-fastapi-backend/README.md`

默认：

- API：`http://127.0.0.1:9099`

> 如需禁用验证码，可参考 `disable_captcha.sql` 或按你的测试环境配置处理。

### 2) 启动管理端（可选：用于 UI 测试）

```bash
cd ../ruoyi-fastapi-frontend
npm install
npm run dev
```

默认：

- 管理端：`http://localhost:80`

### 3) 启动使用端 Web（Portal，可选：用于 UI 测试）

```bash
cd ../ruoyi-fastapi-desktop-web
npm install
npm run dev
```

默认：

- Portal Web：`http://localhost:5175`

### 3.1) 启动使用端 H5（可选：用于 UI 测试）

```bash
cd ../ruoyi-fastapi-app
pnpm install
pnpm dev:h5
```

默认：

- H5：`http://localhost:9090`

### 4) 运行测试

```bash
cd ../ruoyi-fastapi-test
python -m pytest -v
```

---

## Docker 方式（可选）

进入测试目录：

```bash
cd ruoyi-fastapi-test
```

启动服务（MySQL / PostgreSQL 二选一）：

```bash
docker compose -f docker-compose.test.my.yml up -d --build
# 或
docker compose -f docker-compose.test.pg.yml up -d --build
```

运行测试：

```bash
pip install -r requirements.txt
python -m pytest -v
```

---

## 测试说明

- 默认管理员账号：`admin / admin123`（由初始化 SQL 提供）
- 软件库相关测试依赖“种子数据”（例如 `softwareId=20001` 的 Python 条目）
- UI 测试会检查端口是否可访问，不满足条件会 `skip`：
  - 管理端 UI：`localhost:80`
  - Portal Web：`localhost:5175`
  - Portal H5：`localhost:9090`
