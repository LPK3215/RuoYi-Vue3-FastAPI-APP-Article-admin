import request from '@/utils/request'

// 扫描本机已安装软件（Windows）
export function scanLocalSoftware(query) {
  return request({
    url: '/tool/software/scan/list',
    method: 'get',
    params: query
  })
}

// 导入本机扫描结果到软件库
export function importLocalSoftware(data) {
  return request({
    url: '/tool/software/scan/import',
    method: 'post',
    data: data
  })
}
