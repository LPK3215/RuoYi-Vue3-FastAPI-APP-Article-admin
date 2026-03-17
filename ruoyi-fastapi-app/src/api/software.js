import request from "@/utils/request";

// 用户端：获取软件分类列表（含数量）
export function getPortalSoftwareCategories() {
  return request({
    url: "/portal/software/categories",
    headers: {
      isToken: false,
    },
    method: "get",
  });
}

// 用户端：软件分页列表（仅上架）
export function listPortalSoftware(params) {
  return request({
    url: "/portal/software/list",
    headers: {
      isToken: false,
    },
    method: "get",
    params,
  });
}

// 用户端：筛选项聚合（标签/许可证/平台等）
export function getPortalSoftwareFacets(limit = 50) {
  return request({
    url: "/portal/software/facets",
    headers: {
      isToken: false,
    },
    method: "get",
    params: { limit },
  });
}

// 用户端：软件详情（含下载配置）
export function getPortalSoftwareDetail(softwareId) {
  return request({
    url: `/portal/software/${softwareId}`,
    headers: {
      isToken: false,
    },
    method: "get",
  });
}
