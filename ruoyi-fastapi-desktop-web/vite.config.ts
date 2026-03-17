import path from 'node:path'
import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const apiBase = env.VITE_API_BASE || '/dev-api'
  const apiTarget = env.VITE_API_TARGET || 'http://127.0.0.1:9099'

  return {
    plugins: [react()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src')
      }
    },
    server: {
      port: 5175,
      host: true,
      proxy: {
        [apiBase]: {
          target: apiTarget,
          changeOrigin: true,
          rewrite: (p) => p.replace(new RegExp(`^${apiBase}`), '')
        }
      }
    }
  }
})
