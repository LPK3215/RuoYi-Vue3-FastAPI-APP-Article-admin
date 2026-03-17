import { apiRequest } from './http'
import type { ApiTableResponse } from './types'

export type UserRow = {
  userId: number
  userName: string
  nickName?: string
  dept?: { deptName?: string }
  phonenumber?: string
  status?: string
  createTime?: string
  [key: string]: unknown
}

export type ListUsersQuery = {
  pageNum: number
  pageSize: number
  userName?: string
  phonenumber?: string
  status?: string
}

export async function listUsers(query: ListUsersQuery) {
  return apiRequest<ApiTableResponse<UserRow>>({
    url: '/system/user/list',
    method: 'get',
    params: query,
  })
}
