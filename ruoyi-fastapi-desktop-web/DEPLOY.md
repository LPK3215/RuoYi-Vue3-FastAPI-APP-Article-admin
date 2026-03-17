# ruoyi-fastapi-desktop-web（Portal Web 部署说明）

本文件聚焦 Portal Web 的构建与静态部署。

---

## 1. 构建前准备

### 安装依赖

```bash
cd ruoyi-fastapi-desktop-web
npm ci
```

### 确认生产环境变量

默认使用：

- `.env.production`

当前生产默认：

```ini
VITE_APP_TITLE=DeskOps 数据控制台
VITE_API_BASE=/prod-api
```

说明：

- Portal Web 生产环境通常不再使用 `VITE_API_TARGET`
- 生产请求会直接打到 `/prod-api/*`

---

## 2. 构建

```bash
npm run build
```

产物目录：

- `dist/`

如果只是本机验证构建结果：

```bash
npm run preview
```

---

## 3. 与后端配套

Portal Web 最常见的部署方式是：

1. `dist/` 由 Nginx 托管
2. `/prod-api/` 转发给后端
3. 后端 `.env.prod` 中 `APP_ROOT_PATH='/prod-api'`

如果你不是生产，而是预发布，也可以改成：

- Portal：`VITE_API_BASE=/stage-api`
- 后端：`APP_ROOT_PATH=/stage-api`
- Nginx：转发 `/stage-api/`

---

## 4. Nginx 示例

### 正式环境

```nginx
server {
  listen 80;
  server_name your-domain.com;

  root /var/www/deskops-portal;
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

### 预发布环境

```nginx
server {
  listen 80;
  server_name stage.your-domain.com;

  root /var/www/deskops-portal-stage;
  index index.html;

  location / {
    try_files $uri $uri/ /index.html;
  }

  location /stage-api/ {
    proxy_pass http://127.0.0.1:9099/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

---

## 5. 部署后验证

上线后建议验证：

1. 首页是否能正常打开
2. 软件列表接口是否正常
3. 软件详情页和文章详情页是否能打开
4. 刷新任意路由是否正常

---

## 6. 常见问题

### 刷新二级路由 404

这是 SPA 场景，必须配置：

```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

### 页面打开了，但接口 404

先检查三者是否一致：

1. Portal 的 `VITE_API_BASE`
2. 后端的 `APP_ROOT_PATH`
3. Nginx 的 `location /xxx-api/`

### 想部署额外环境

可以自行新增 `.env.<mode>`，然后：

```bash
npx vite build --mode <mode>
```

需要同时补齐后端环境和 Nginx 配置。
