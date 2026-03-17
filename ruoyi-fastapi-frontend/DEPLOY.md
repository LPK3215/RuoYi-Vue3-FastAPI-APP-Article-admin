# ruoyi-fastapi-frontend（管理后台部署说明）

本文件聚焦管理后台的构建和部署。

---

## 1. 构建模式

当前 `package.json` 已提供：

| 命令 | 配置文件 | 适用场景 | API 前缀 |
|------|----------|----------|----------|
| `npm run build:prod` | `.env.production` | 正式环境 | `/prod-api` |
| `npm run build:stage` | `.env.staging` | 预发布环境 | `/stage-api` |
| `npm run build:docker` | `.env.docker` | Docker 环境 | `/docker-api` |

如果只是本机调试，不需要构建，直接：

```bash
npm run dev
```

---

## 2. 安装与构建

```bash
cd ruoyi-fastapi-frontend
npm ci
npm run build:prod
```

构建产物：

- `dist/`

---

## 3. 部署前对齐项

### 前端

确认当前构建模式对应的 API 前缀：

- `.env.production` -> `/prod-api`
- `.env.staging` -> `/stage-api`
- `.env.docker` -> `/docker-api`

### 后端

确认后端对应环境中的：

- `APP_ROOT_PATH`

必须和前端前缀一致。

例如：

| 前端构建 | 后端环境 |
|----------|----------|
| `build:prod` | `.env.prod` 中 `/prod-api` |
| `build:stage` | 你自建 `.env.stage` 中 `/stage-api` |
| `build:docker` | `.env.dockermy` / `.env.dockerpg` 中 `/docker-api` |

---

## 4. Nginx 部署示例

### 正式环境 `/prod-api`

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

### 预发布 `/stage-api`

```nginx
server {
  listen 80;
  server_name stage.your-domain.com;

  root /var/www/softwarehub-admin-stage;
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

### Docker `/docker-api`

Docker 场景已经内置在：

- `bin/nginx.dockermy.conf`
- `bin/nginx.dockerpg.conf`

如果使用根目录 compose，无需再手工写一份。

---

## 5. Docker 构建

当前 Dockerfile 会执行：

```bash
npm run build:docker
```

然后把 `dist/` 拷贝到 Nginx 镜像中。

如果要手工构建：

```bash
docker build -t deskops-admin ./ruoyi-fastapi-frontend
```

---

## 6. 部署后验证

建议依次检查：

1. 首页是否能打开
2. 登录接口是否成功
3. 刷新任意内部路由是否正常
4. 上传、下载、导出是否正常

---

## 7. 常见问题

### 构建后接口 404 / 502

通常是这三类问题：

1. 前端 API 前缀和后端 `APP_ROOT_PATH` 不一致
2. Nginx 没有转发对应前缀
3. `proxy_pass` 结尾缺少 `/`

### 页面打开正常，刷新子路由 404

确保启用了：

```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

### Docker 环境接口不通

确认使用的是：

- `.env.docker`
- 后端 `.env.dockermy` 或 `.env.dockerpg`
- 对应的 Nginx 配置也是 `/docker-api`
