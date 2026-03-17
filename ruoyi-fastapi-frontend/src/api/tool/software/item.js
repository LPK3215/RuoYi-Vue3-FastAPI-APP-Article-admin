import request from '@/utils/request'

// 查询软件列表
export function listSoftwareItem(query) {
  return request({
    url: '/tool/software/item/list',
    method: 'get',
    params: query
  })
}

// 查询软件详细（含下载配置）
export function getSoftwareItem(softwareId) {
  return request({
    url: '/tool/software/item/' + softwareId,
    method: 'get'
  })
}

// 新增软件
export function addSoftwareItem(data) {
  return request({
    url: '/tool/software/item',
    method: 'post',
    data: data
  })
}

// 修改软件
export function updateSoftwareItem(data) {
  return request({
    url: '/tool/software/item',
    method: 'put',
    data: data
  })
}

// 删除软件
export function delSoftwareItem(softwareIds) {
  return request({
    url: '/tool/software/item/' + softwareIds,
    method: 'delete'
  })
}

// 修改发布状态
export function changeSoftwarePublishStatus(data) {
  return request({
    url: '/tool/software/item/changePublishStatus',
    method: 'put',
    data: data
  })
}

// 批量修改发布状态
export function batchChangeSoftwarePublishStatus(data) {
  return request({
    url: '/tool/software/item/batchChangePublishStatus',
    method: 'put',
    data: data
  })
}

// 批量移动分类
export function batchMoveSoftwareCategory(data) {
  return request({
    url: '/tool/software/item/batchMoveCategory',
    method: 'put',
    data: data
  })
}

// 批量标签治理（追加/移除/覆盖）
export function batchManageSoftwareTags(data) {
  return request({
    url: '/tool/software/item/batchManageTags',
    method: 'put',
    data: data
  })
}

// 获取软件筛选项聚合（标签/许可证/作者/平台等）
export function getSoftwareItemFacets(query) {
  return request({
    url: '/tool/software/item/facets',
    method: 'get',
    params: query
  })
}
