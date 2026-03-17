import { apiRequest } from './http'
import type { ApiBase } from './types'

export type CaptchaImageResponse = ApiBase & {
  captchaEnabled?: boolean
  registerEnabled?: boolean
  img?: string
  uuid?: string
}

export async function getCaptchaImage() {
  return apiRequest<CaptchaImageResponse>({
    url: '/captchaImage',
    method: 'get',
    headers: { isToken: false },
    timeout: 20_000,
  })
}

export type LoginPayload = {
  username: string
  password: string
  code?: string
  uuid?: string
}

export type LoginResponse = ApiBase & {
  token: string
}

export async function login(payload: LoginPayload) {
  const body = new URLSearchParams()
  body.set('username', payload.username)
  body.set('password', payload.password)
  body.set('code', payload.code || '')
  body.set('uuid', payload.uuid || '')

  return apiRequest<LoginResponse>({
    url: '/login',
    method: 'post',
    headers: {
      isToken: false,
      repeatSubmit: false,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    data: body,
  })
}

export type UserInfo = {
  userId: number
  userName: string
  nickName?: string
  avatar?: string
  [key: string]: unknown
}

export type GetInfoResponse = ApiBase & {
  user: UserInfo
  roles?: string[]
  permissions?: string[]
  isDefaultModifyPwd?: boolean
  isPasswordExpired?: boolean
}

export async function getInfo() {
  return apiRequest<GetInfoResponse>({
    url: '/getInfo',
    method: 'get',
  })
}

export async function logout() {
  return apiRequest<ApiBase>({
    url: '/logout',
    method: 'post',
  })
}

