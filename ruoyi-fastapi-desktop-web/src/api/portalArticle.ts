import { apiRequest } from './http'
import type { ApiPageResponse, ApiResponse } from './types'
import type { PortalSoftwareListItem } from './portalSoftware'

export type PortalArticleCategory = {
  categoryId: number
  categoryCode?: string | null
  categoryName: string
  articleCount: number
}

export type PortalArticleTag = {
  tagId: number
  tagName: string
  articleCount: number
}

export type PortalArticleListItem = {
  articleId: number
  title: string
  summary?: string | null
  coverUrl?: string | null
  tags?: string | null
  articleType?: string | null
  publishTime?: string | null
  updateTime?: string | null
}

export type PortalAttachmentItem = {
  name: string
  url: string
  size?: number | null
}

export type PortalArticleDetail = PortalArticleListItem & {
  contentMd?: string | null
  softwares: PortalSoftwareListItem[]
  attachments?: PortalAttachmentItem[]
}

export type PortalArticleListQuery = {
  pageNum: number
  pageSize: number
  keyword?: string
  categoryId?: number
  tag?: string
  articleType?: string
  softwareId?: number
}

export async function getPortalArticleCategories() {
  return apiRequest<ApiResponse<PortalArticleCategory[]>>({
    url: '/portal/article/categories',
    method: 'get',
    headers: { isToken: false },
  })
}

export async function getPortalArticleTags(limit = 50) {
  return apiRequest<ApiResponse<PortalArticleTag[]>>({
    url: '/portal/article/tags',
    method: 'get',
    params: { limit },
    headers: { isToken: false },
  })
}

export async function listPortalArticle(query: PortalArticleListQuery) {
  return apiRequest<ApiPageResponse<PortalArticleListItem>>({
    url: '/portal/article/list',
    method: 'get',
    params: query,
    headers: { isToken: false },
  })
}

export async function getPortalArticleDetail(articleId: number) {
  return apiRequest<ApiResponse<PortalArticleDetail>>({
    url: `/portal/article/${articleId}`,
    method: 'get',
    headers: { isToken: false },
  })
}
