import { apiRequest } from './http'
import type { ApiPageResponse, ApiResponse } from './types'

export type PortalSoftwareCategory = {
  categoryId: number
  categoryCode?: string | null
  categoryName: string
  softwareCount: number
}

export type SoftwareFacetItem = { value: string; count: number }

export type SoftwareFacets = {
  tags: SoftwareFacetItem[]
  licenses: SoftwareFacetItem[]
  authors: SoftwareFacetItem[]
  teams: SoftwareFacetItem[]
  platforms: SoftwareFacetItem[]
}

export type PortalSoftwareListItem = {
  softwareId: number
  categoryId?: number | null
  categoryName?: string | null
  softwareName: string
  shortDesc?: string | null
  iconUrl?: string | null
  officialUrl?: string | null
  repoUrl?: string | null
  author?: string | null
  team?: string | null
  license?: string | null
  openSource?: '0' | '1' | null
  tags?: string | null
  publishStatus?: '1' | string
  updateTime?: string | null
}

export type PortalSoftwareDownload = {
  platform: string
  downloadUrl: string
  version?: string | null
  checksum?: string | null
  sort?: number | null
  remark?: string | null
}

export type PortalSoftwareResource = {
  resourceType: string
  title?: string | null
  resourceUrl: string
  sort?: number | null
  remark?: string | null
}

export type PortalSoftwareDetail = {
  softwareId: number
  categoryId?: number | null
  categoryName?: string | null
  softwareName: string
  shortDesc?: string | null
  iconUrl?: string | null
  officialUrl?: string | null
  repoUrl?: string | null
  author?: string | null
  team?: string | null
  license?: string | null
  openSource?: '0' | '1' | null
  tags?: string | null
  descriptionMd?: string | null
  usageMd?: string | null
  updateTime?: string | null
  downloads: PortalSoftwareDownload[]
  resources: PortalSoftwareResource[]
}

export type PortalSoftwareListQuery = {
  pageNum: number
  pageSize: number
  categoryId?: number
  keyword?: string
  openSource?: '0' | '1'
  license?: string
  tag?: string
  platform?: string
}

export async function getPortalSoftwareCategories() {
  return apiRequest<ApiResponse<PortalSoftwareCategory[]>>({
    url: '/portal/software/categories',
    method: 'get',
    headers: { isToken: false },
  })
}

export async function getPortalSoftwareFacets(limit = 50) {
  return apiRequest<ApiResponse<SoftwareFacets>>({
    url: '/portal/software/facets',
    method: 'get',
    params: { limit },
    headers: { isToken: false },
  })
}

export async function listPortalSoftware(query: PortalSoftwareListQuery) {
  return apiRequest<ApiPageResponse<PortalSoftwareListItem>>({
    url: '/portal/software/list',
    method: 'get',
    params: query,
    headers: { isToken: false },
  })
}

export async function getPortalSoftwareDetail(softwareId: number) {
  return apiRequest<ApiResponse<PortalSoftwareDetail>>({
    url: `/portal/software/${softwareId}`,
    method: 'get',
    headers: { isToken: false },
  })
}

