import request from '@/utils/request'

// 查询教程文章列表
export function listKbArticle(query) {
  return request({
    url: '/tool/kb/article/list',
    method: 'get',
    params: query
  })
}

// 查询教程文章详情（含关联软件ID列表）
export function getKbArticle(articleId) {
  return request({
    url: '/tool/kb/article/' + articleId,
    method: 'get'
  })
}

// 新增教程文章
export function addKbArticle(data) {
  return request({
    url: '/tool/kb/article',
    method: 'post',
    data: data
  })
}

// 修改教程文章
export function updateKbArticle(data) {
  return request({
    url: '/tool/kb/article',
    method: 'put',
    data: data
  })
}

// 删除教程文章
export function delKbArticle(articleIds) {
  return request({
    url: '/tool/kb/article/' + articleIds,
    method: 'delete'
  })
}

// 修改发布状态（草稿/发布/下线）
export function changeKbArticlePublishStatus(data) {
  return request({
    url: '/tool/kb/article/changePublishStatus',
    method: 'put',
    data: data
  })
}

