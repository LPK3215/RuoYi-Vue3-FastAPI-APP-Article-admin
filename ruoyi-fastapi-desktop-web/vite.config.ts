import path from 'node:path'
import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

const PORTAL_CHUNK_GROUPS = [
  { name: 'vendor-react', packages: ['react', 'react-dom', 'react-router-dom'] },
  { name: 'vendor-data', packages: ['@tanstack/react-query', '@tanstack/react-table'] },
  { name: 'vendor-markdown', packages: ['react-markdown', 'remark-gfm'] },
  { name: 'vendor-utils', packages: ['axios', 'clsx'] }
]

function resolveManualChunk(id: string): string | undefined {
  const normalizedId = id.replace(/\\/g, '/')
  if (!normalizedId.includes('/node_modules/')) {
    return undefined
  }
  for (const group of PORTAL_CHUNK_GROUPS) {
    if (group.packages.some((pkg) => normalizedId.includes(`/node_modules/${pkg}/`))) {
      return group.name
    }
  }
  return 'vendor-misc'
}

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const apiBase = env.VITE_API_BASE || '/dev-api'
  const apiTarget = env.VITE_API_TARGET || 'http://127.0.0.1:9099'
  const devPort = Number(env.VITE_DEV_PORT || 5175)

  return {
    plugins: [react()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src')
      }
    },
    server: {
      port: devPort,
      host: true,
      proxy: {
        [apiBase]: {
          target: apiTarget,
          changeOrigin: true,
          rewrite: (p) => p.replace(new RegExp(`^${apiBase}`), '')
        }
      }
    },
    build: {
      chunkSizeWarningLimit: 400,
      rollupOptions: {
        output: {
          manualChunks: resolveManualChunk
        }
      }
    }
  }
})
