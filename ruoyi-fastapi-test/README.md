# ruoyi-fastapi-test（测试说明）

本目录是项目的自动化测试套件，包含：

- API 测试（`requests`）
- UI / E2E 测试（Playwright）

---

## 1. 依赖安装

建议使用 Python 3.10+。

```bash
cd ruoyi-fastapi-test
pip install -r requirements.txt
playwright install
```

---

## 2. 测试依赖的服务

默认测试配置在：

- `common/config.py`

当前默认地址：

| 服务 | 默认地址 |
|------|----------|
| 管理后台 | `http://localhost:80` |
| 后端 | `http://localhost:9099` |

如果你的端口变了，请先修改：

- `common/config.py`

---

## 3. 推荐启动顺序

### 只跑 API 测试

只需要后端：

```bash
cd ../ruoyi-fastapi-backend
python app.py --env dev
```

### 跑管理后台 UI 测试

```bash
cd ../ruoyi-fastapi-frontend
npm install
npm run dev
```

### 跑 Portal Web / App UI 测试

Portal Web：

```bash
cd ../ruoyi-fastapi-desktop-web
npm install
npm run dev
```

App H5：

```bash
cd ../ruoyi-fastapi-app
pnpm install
pnpm dev:h5
```

---

## 4. 运行测试

回到测试目录：

```bash
cd ../ruoyi-fastapi-test
python -m pytest -v
```

### 按文件运行

```bash
python -m pytest test_login.py -v
python -m pytest test_pages.py -v
python -m pytest tool -v
python -m pytest system -v
python -m pytest monitor -v
```

---

## 5. Docker 方式

测试目录也提供了独立 compose：

| 文件 | 说明 |
|------|------|
| `docker-compose.test.my.yml` | MySQL 测试环境 |
| `docker-compose.test.pg.yml` | PostgreSQL 测试环境 |

### 启动

```bash
cd ruoyi-fastapi-test
docker compose -f docker-compose.test.my.yml up -d --build
# 或
docker compose -f docker-compose.test.pg.yml up -d --build
```

### 执行测试

```bash
pip install -r requirements.txt
python -m pytest -v
```

---

## 6. 测试数据说明

- 默认管理员账号：`admin / admin123`
- 软件库相关测试依赖初始化 SQL 和种子数据
- 部分文章 / 软件测试依赖 KB 和 Software SQL 已导入

如果你的库不是完整初始化状态，部分测试会失败。

---

## 7. UI 测试说明

部分 UI 测试在目标端口未启动时会自动 `skip`，避免误报。

常见依赖端口：

- 管理后台：`localhost:80`
- Portal Web：`localhost:5175`
- Portal H5：`localhost:9090`

---

## 8. 常见问题

### 登录测试失败

优先检查：

1. 后端是否启动
2. 数据库中是否有默认管理员
3. 是否被验证码或锁定策略影响

### UI 测试全部被跳过

说明通常不是测试坏了，而是对应服务没有启动。

### 端口和我本机不一致

请修改：

- `common/config.py`

再运行测试。
