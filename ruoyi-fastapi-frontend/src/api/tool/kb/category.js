import request from '@/utils/request'

// 查询教程分类列表
export function listKbCategory(query) {
  return request({
    url: '/tool/kb/category/list',
    method: 'get',
    params: query
  })
}

// 查询教程分类下拉选项
export function listKbCategoryOptions() {
  return request({
    url: '/tool/kb/category/options',
    method: 'get'
  })
}

// 查询教程分类详细
export function getKbCategory(categoryId) {
  return request({
    url: '/tool/kb/category/' + categoryId,
    method: 'get'
  })
}

// 新增教程分类
export function addKbCategory(data) {
  return request({
    url: '/tool/kb/category',
    method: 'post',
    data: data
  })
}

// 修改教程分类
export function updateKbCategory(data) {
  return request({
    url: '/tool/kb/category',
    method: 'put',
    data: data
  })
}

// 删除教程分类
export function delKbCategory(categoryIds) {
  return request({
    url: '/tool/kb/category/' + categoryIds,
    method: 'delete'
  })
}

