import request from "@/utils/request";

// 用户端：获取教程分类列表（含数量）
export function getPortalArticleCategories() {
  return request({
    url: "/portal/article/categories",
    headers: { isToken: false },
    method: "get",
  });
}

// 用户端：获取教程热门标签列表（含数量）
export function getPortalArticleTags(limit = 50) {
  return request({
    url: "/portal/article/tags",
    headers: { isToken: false },
    method: "get",
    params: { limit },
  });
}

// 用户端：教程文章分页列表（仅已发布/正常）
export function listPortalArticle(params) {
  return request({
    url: "/portal/article/list",
    headers: { isToken: false },
    method: "get",
    params,
  });
}

// 用户端：教程文章详情（含关联软件、附件）
export function getPortalArticleDetail(articleId) {
  return request({
    url: `/portal/article/${articleId}`,
    headers: { isToken: false },
    method: "get",
  });
}
