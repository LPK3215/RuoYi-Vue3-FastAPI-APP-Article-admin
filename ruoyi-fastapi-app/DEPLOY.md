# ruoyi-fastapi-app（App / H5 部署说明）

本文件聚焦 `ruoyi-fastapi-app` 的部署与发布。

---

## 1. 部署前必须确认

### 后端地址

发布前先检查：

- `src/config.js`

把 `baseUrl` 改成目标环境可访问的地址。

常见示例：

| 环境 | `baseUrl` |
|------|-----------|
| 本机开发 | `http://localhost:9099` |
| 预发布 | `https://stage.your-domain.com/stage-api` |
| 生产 | `https://your-domain.com/prod-api` |

### 平台配置

如果要发布小程序或 APP，还要检查：

- `src/manifest.json`

重点包括：

- App 名称
- 各平台 `appid`
- 打包配置

---

## 2. H5 部署

### 构建

```bash
cd ruoyi-fastapi-app
pnpm install
pnpm build:h5
```

产物目录：

- `dist/build/h5/`

### 部署方式

把 `dist/build/h5/` 部署到任意静态服务器即可，例如：

- Nginx
- OSS / COS / CDN
- Netlify

### Nginx 示例

```nginx
server {
  listen 80;
  server_name app.your-domain.com;

  root /var/www/deskops-app-h5;
  index index.html;

  location / {
    try_files $uri $uri/ /index.html;
  }
}
```

说明：

- App 自己是静态页面
- 实际 API 走 `src/config.js` 中配置的后端地址

---

## 3. 微信小程序发布

### 开发构建

```bash
pnpm build:mp-weixin
```

产物目录：

- `dist/build/mp-weixin/`

### 打开开发者工具

```bash
pnpm open:build
```

### 上传

```bash
pnpm upload:build
```

发布前请确认：

1. 微信开发者工具已登录
2. `manifest.json` 中的小程序 `appid` 正确
3. 服务器域名已在小程序后台配置

---

## 4. APP 发布

### 构建

```bash
pnpm build:app
```

如果需要其他平台，可用：

```bash
pnpm build:custom
```

发布前请确认：

1. `manifest.json` 中应用标识正确
2. 图标、启动页、包名等信息已配置
3. `src/config.js` 的 `baseUrl` 指向可被真机访问的服务

---

## 5. 多环境发布建议

由于当前 App 没有独立 `.env.*`，建议采用下面方式管理环境：

### 方案 A：手工切换 `src/config.js`

适合项目当前结构，最直接。

### 方案 B：自己扩展一套环境文件

如果后续你希望和 Web 一样管理多环境，可以继续演进为：

- `config.dev.js`
- `config.stage.js`
- `config.prod.js`

再在构建前按脚本拷贝或注入。

---

## 6. 部署后验证

无论是 H5、小程序还是 APP，建议至少验证：

1. 登录是否正常
2. 软件列表是否能拉到数据
3. 软件详情和文章详情是否能打开
4. 下载 / 外链跳转是否正常

---

## 7. 常见问题

### 改目录名后无法构建

重新执行：

```bash
pnpm install
```

### 真机能打开页面但接口失败

不要再用：

- `http://localhost:9099`

真机需要改成：

- `http://你的电脑局域网IP:9099`
- 或线上域名

### H5 刷新 404

部署在 Nginx 时需要：

```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```
