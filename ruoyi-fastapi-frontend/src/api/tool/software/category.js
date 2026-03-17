import request from '@/utils/request'

// 查询软件分类列表
export function listSoftwareCategory(query) {
  return request({
    url: '/tool/software/category/list',
    method: 'get',
    params: query
  })
}

// 查询软件分类下拉选项
export function listSoftwareCategoryOptions() {
  return request({
    url: '/tool/software/category/options',
    method: 'get'
  })
}

// 查询软件分类详细
export function getSoftwareCategory(categoryId) {
  return request({
    url: '/tool/software/category/' + categoryId,
    method: 'get'
  })
}

// 新增软件分类
export function addSoftwareCategory(data) {
  return request({
    url: '/tool/software/category',
    method: 'post',
    data: data
  })
}

// 修改软件分类
export function updateSoftwareCategory(data) {
  return request({
    url: '/tool/software/category',
    method: 'put',
    data: data
  })
}

// 删除软件分类
export function delSoftwareCategory(categoryIds) {
  return request({
    url: '/tool/software/category/' + categoryIds,
    method: 'delete'
  })
}
