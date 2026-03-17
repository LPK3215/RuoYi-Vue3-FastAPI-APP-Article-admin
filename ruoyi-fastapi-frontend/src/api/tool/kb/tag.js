import request from '@/utils/request'

// 查询教程标签列表
export function listKbTag(query) {
  return request({
    url: '/tool/kb/tag/list',
    method: 'get',
    params: query
  })
}

// 查询教程标签下拉选项
export function listKbTagOptions() {
  return request({
    url: '/tool/kb/tag/options',
    method: 'get'
  })
}

// 查询教程标签详细
export function getKbTag(tagId) {
  return request({
    url: '/tool/kb/tag/' + tagId,
    method: 'get'
  })
}

// 新增教程标签
export function addKbTag(data) {
  return request({
    url: '/tool/kb/tag',
    method: 'post',
    data: data
  })
}

// 修改教程标签
export function updateKbTag(data) {
  return request({
    url: '/tool/kb/tag',
    method: 'put',
    data: data
  })
}

// 删除教程标签
export function delKbTag(tagIds) {
  return request({
    url: '/tool/kb/tag/' + tagIds,
    method: 'delete'
  })
}

