import request from '@/utils/request'

// 后台首页看板（聚合接口）
export function getSoftwareDashboardOverview(params) {
  return request({
    url: '/tool/software/item/overview',
    method: 'get',
    params: params
  })
}

