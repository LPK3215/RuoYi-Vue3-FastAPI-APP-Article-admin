import axios, { AxiosError, type AxiosRequestConfig } from 'axios'
import { clearToken, getToken } from '@/auth/token'

type UnknownRecord = Record<string, unknown>

const baseURL = import.meta.env.VITE_API_BASE || '/dev-api'

export const http = axios.create({
  baseURL,
  timeout: 15_000,
  headers: {
    'Content-Type': 'application/json;charset=utf-8',
  },
})

http.interceptors.request.use(
  (config) => {
    const isToken = (config.headers as UnknownRecord | undefined)?.isToken === false
    if (!isToken) {
      const token = getToken()
      if (token) {
        config.headers = config.headers || {}
        config.headers.Authorization = `Bearer ${token}`
      }
    }
    return config
  },
  (error) => Promise.reject(error),
)

http.interceptors.response.use(
  (res) => {
    const data = res.data as UnknownRecord | undefined

    // blob/arraybuffer：直接返回
    if (
      res.request?.responseType === 'blob' ||
      res.request?.responseType === 'arraybuffer'
    ) {
      return res.data
    }

    const code = (data?.code as number | undefined) ?? 200
    const msg = (data?.msg as string | undefined) || '请求失败'

    if (code === 200) return res.data

    if (code === 401) {
      clearToken()
      window.location.href = '/admin/login'
      return Promise.reject(new Error('登录状态已过期，请重新登录'))
    }

    return Promise.reject(new Error(msg))
  },
  (error: AxiosError) => {
    if (error.code === 'ECONNABORTED') {
      return Promise.reject(new Error('请求超时，请稍后再试'))
    }

    if (error.message === 'Network Error') {
      return Promise.reject(new Error('后端接口连接异常'))
    }

    return Promise.reject(error)
  },
)

export async function apiRequest<T>(config: AxiosRequestConfig): Promise<T> {
  const data = await http.request(config)
  return data as T
}
