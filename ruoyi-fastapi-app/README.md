# ruoyi-fastapi-app（App / H5 使用说明）

本目录是基于 uni-app 的客户端工程，支持：

- H5
- 微信小程序
- 原生 APP
- 其他 uni-app 支持的平台

---

## 1. 环境要求

- Node.js：建议 `^20.19.0 || >=22.12.0`
- pnpm：项目默认使用 `pnpm@10`

---

## 2. 环境切换方式

当前 App 没有独立的 `.env.*`，而是通过：

- `src/config.js`

来切换后端请求地址。

### 当前关键配置

```js
export default {
  baseUrl: "http://localhost:9099",
}
```

### 常见场景

| 场景 | `baseUrl` 示例 |
|------|----------------|
| 本机开发 | `http://localhost:9099` |
| 本机同局域网真机调试 | `http://你的电脑IP:9099` |
| 生产部署 | `https://your-domain.com/prod-api` |
| 预发布 | `https://stage.your-domain.com/stage-api` |

原则：

- `baseUrl + 接口路径` 必须能直接请求到后端

---

## 3. 首次安装

```bash
cd ruoyi-fastapi-app
pnpm install
```

如果你刚刚重命名、移动过这个项目目录，建议重新执行一次：

```bash
pnpm install
```

原因是 `pnpm` 生成的 `.bin` 启动脚本在 Windows 下可能会缓存旧路径。

---

## 4. 常用启动命令

### H5

```bash
pnpm dev:h5
```

通常访问：

- `http://localhost:9090`

如果端口占用，uni-app 会自动尝试其他端口，以终端输出为准。

### 微信小程序

```bash
pnpm dev:mp-weixin
```

### APP

```bash
pnpm dev:app
```

### 其他平台

```bash
pnpm dev:mp-qq
pnpm dev:mp-alipay
pnpm dev:quickapp-webview
```

---

## 5. 常用构建命令

### H5

```bash
pnpm build:h5
```

### 微信小程序

```bash
pnpm build:mp-weixin
```

### APP

```bash
pnpm build:app
```

### 其他平台

```bash
pnpm build:mp-qq
pnpm build:mp-alipay
pnpm build:quickapp-webview
```

---

## 6. 构建产物

常见输出目录：

| 平台 | 输出目录 |
|------|----------|
| H5 | `dist/build/h5/` |
| 微信小程序（生产） | `dist/build/mp-weixin/` |
| 微信小程序（开发） | `dist/dev/mp-weixin/` |

---

## 7. 微信开发者工具辅助命令

项目已经集成 `weapp-ide-cli`：

```bash
pnpm open:dev
pnpm open:build
pnpm weapp:login
```

如需上传：

```bash
pnpm upload:dev
pnpm upload:build
```

---

## 8. 其他关键配置

### App 名称 / 标题 / AppID

重点文件：

- `src/manifest.json`
- `src/pages.json`

常见需要改的内容：

- App 名称
- 页面标题
- 各平台 `appid`

### 应用信息

可在 `src/config.js` 中修改：

- `appInfo.name`
- `appInfo.version`
- `appInfo.logo`
- `appInfo.site_url`
- 协议链接

---

## 9. 常见问题

### 改了目录名后 `uni` 命令报错

请重新运行：

```bash
pnpm install
```

### H5 能打开但请求失败

通常是 `src/config.js` 里的 `baseUrl` 没改对：

- 本机浏览器开发用 `http://localhost:9099`
- 真机联调用你电脑的局域网 IP

### 小程序无法打开

确认：

1. `src/manifest.json` 的 `appid` 已配置
2. 微信开发者工具已登录
3. 目标目录是正确的 `dist/dev/mp-weixin` 或 `dist/build/mp-weixin`

---

## 10. 进一步阅读

- [部署说明](./DEPLOY.md)
- [仓库总说明](../README.md)
