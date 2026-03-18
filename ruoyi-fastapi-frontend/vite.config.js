import { defineConfig, loadEnv } from 'vite'
import path from 'path'
import createVitePlugins from './vite/plugins'

const UI_PACKAGES = new Set([
  'vue',
  'vue-router',
  'pinia',
  '@vueuse/core',
  'element-plus',
  '@element-plus/icons-vue',
  'ant-design-vue',
  '@ant-design/icons-vue'
])
const MARKDOWN_PACKAGES = new Set(['markstream-vue', 'stream-markdown', 'vue-i18n', 'katex'])
const MERMAID_PACKAGES = new Set(['mermaid', '@mermaid-js/parser'])
const QUILL_PACKAGES = new Set(['@vueup/vue-quill', 'quill'])
const CHART_PACKAGES = new Set(['echarts', '@antv/g2plot', '@antv/infographic'])
const UTILS_PACKAGES = new Set([
  'axios',
  'uuid',
  'js-cookie',
  'jsencrypt',
  'nprogress',
  'clipboard',
  'file-saver',
  'fuse.js',
  'splitpanes',
  'vuedraggable',
  'vue-cropper'
])

function getPackageName(normalizedId) {
  const nodeModulesIndex = normalizedId.lastIndexOf('/node_modules/')
  if (nodeModulesIndex < 0) {
    return null
  }
  const packagePath = normalizedId.slice(nodeModulesIndex + '/node_modules/'.length)
  const packageSegments = packagePath.split('/')
  if (packageSegments[0].startsWith('@')) {
    return `${packageSegments[0]}/${packageSegments[1]}`
  }
  return packageSegments[0]
}

function resolveManualChunk(id) {
  const normalizedId = id.replace(/\\/g, '/')
  if (!normalizedId.includes('/node_modules/')) {
    return undefined
  }
  const packageName = getPackageName(normalizedId)
  if (!packageName) {
    return undefined
  }
  if (UI_PACKAGES.has(packageName)) {
    return 'vendor-ui'
  }
  if (MARKDOWN_PACKAGES.has(packageName)) {
    return 'vendor-markdown'
  }
  if (MERMAID_PACKAGES.has(packageName)) {
    return 'vendor-mermaid'
  }
  if (QUILL_PACKAGES.has(packageName)) {
    return 'vendor-quill'
  }
  if (CHART_PACKAGES.has(packageName)) {
    return 'vendor-charts'
  }
  if (UTILS_PACKAGES.has(packageName)) {
    return 'vendor-utils'
  }
  return undefined
}

// https://vitejs.dev/config/
export default defineConfig(({ mode, command }) => {
  const env = loadEnv(mode, process.cwd())
  const { VITE_APP_ENV } = env
  const devPort = Number(env.VITE_DEV_PORT || 5174)
  const devProxyTarget = env.VITE_DEV_PROXY_TARGET || 'http://127.0.0.1:9099'
  return {
    // 部署生产环境和开发环境下的URL。
    // 默认情况下，vite 会假设你的应用是被部署在一个域名的根路径上
    // 例如 https://www.ruoyi.vip/。如果应用被部署在一个子路径上，你就需要用这个选项指定这个子路径。例如，如果你的应用被部署在 https://www.ruoyi.vip/admin/，则设置 baseUrl 为 /admin/。
    base: VITE_APP_ENV === 'production' ? '/' : '/',
    plugins: createVitePlugins(env, command === 'build'),
    resolve: {
      // https://cn.vitejs.dev/config/#resolve-alias
      alias: {
        // 设置路径
        '~': path.resolve(__dirname, './'),
        // 设置别名
        '@': path.resolve(__dirname, './src')
      },
      // https://cn.vitejs.dev/config/#resolve-extensions
      extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue']
    },
    // 打包配置
    build: {
      // https://vite.dev/config/build-options.html
      sourcemap: command === 'build' ? false : 'inline',
      outDir: 'dist',
      assetsDir: 'assets',
      chunkSizeWarningLimit: 2600,
      rollupOptions: {
        output: {
          manualChunks: resolveManualChunk,
          chunkFileNames: 'static/js/[name]-[hash].js',
          entryFileNames: 'static/js/[name]-[hash].js',
          assetFileNames: 'static/[ext]/[name]-[hash].[ext]'
        }
      }
    },
    // vite 相关配置
    server: {
      port: devPort,
      host: true,
      open: true,
      proxy: {
        // https://cn.vitejs.dev/config/#server-proxy
        '/dev-api': {
          target: devProxyTarget,
          changeOrigin: true,
          rewrite: (p) => p.replace(/^\/dev-api/, '')
        }
      }
    },
    //fix:error:stdin>:7356:1: warning: "@charset" must be the first rule in the file
    css: {
      postcss: {
        plugins: [
          {
            postcssPlugin: 'internal:charset-removal',
            AtRule: {
              charset: (atRule) => {
                if (atRule.name === 'charset') {
                  atRule.remove();
                }
              }
            }
          }
        ]
      }
    }
  }
})
