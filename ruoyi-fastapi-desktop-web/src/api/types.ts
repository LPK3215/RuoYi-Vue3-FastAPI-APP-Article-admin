export type ApiCode = number

export interface ApiBase {
  code: ApiCode
  msg: string
}

export type ApiResponse<T = unknown> = ApiBase & {
  data?: T
  [key: string]: unknown
}

export type ApiTableResponse<T> = ApiBase & {
  rows: T[]
  total: number
}

export type ApiPageResponse<T> = ApiBase & {
  rows: T[]
  total: number
  pageNum?: number
  pageSize?: number
  hasNext?: boolean
}
