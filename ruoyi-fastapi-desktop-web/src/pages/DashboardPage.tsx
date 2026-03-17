import { getInfo } from '@/api/auth'
import { Card, CardHeader } from '@/ui/Card'
import { Spinner } from '@/ui/Spinner'
import { useQuery } from '@tanstack/react-query'

export function DashboardPage() {
  const infoQuery = useQuery({
    queryKey: ['auth', 'getInfo'],
    queryFn: getInfo,
  })

  if (infoQuery.isLoading) {
    return (
      <div className="ds-pad">
        <Spinner label="正在加载…" />
      </div>
    )
  }

  if (infoQuery.isError) {
    return (
      <div className="ds-pad">
        <div className="ds-alert ds-alert--error" role="alert">
          {(infoQuery.error as Error)?.message || '加载失败'}
        </div>
      </div>
    )
  }

  const user = infoQuery.data?.user
  const roles = infoQuery.data?.roles || []
  const perms = infoQuery.data?.permissions || []

  return (
    <div className="ds-pad">
      <div className="ds-grid2">
        <Card>
          <CardHeader title="当前会话" subtitle="来自 /getInfo" />
          <div className="ds-kv">
            <div className="ds-kvRow">
              <div className="ds-kvKey">用户</div>
              <div className="ds-kvVal">
                <span className="ds-mono">{user?.userName ?? '—'}</span>
                <span className="ds-muted">（ID: {user?.userId ?? '—'}）</span>
              </div>
            </div>
            <div className="ds-kvRow">
              <div className="ds-kvKey">角色</div>
              <div className="ds-kvVal">{roles.length ? roles.join(', ') : '—'}</div>
            </div>
            <div className="ds-kvRow">
              <div className="ds-kvKey">权限数量</div>
              <div className="ds-kvVal">
                <span className="ds-mono">{perms.length}</span>
              </div>
            </div>
          </div>
        </Card>

        <Card>
          <CardHeader
            title="下一步渲染"
            subtitle="建议把你的业务接口接进来"
          />
          <div className="ds-next">
            <div className="ds-nextItem">
              <div className="ds-nextTitle">1) 在 `src/api/` 新增接口函数</div>
              <div className="ds-nextDesc">
                用 `apiRequest` 调你的后端接口（GET/POST），返回值直接就是后端的 JSON。
              </div>
            </div>
            <div className="ds-nextItem">
              <div className="ds-nextTitle">2) 用 `useQuery` 拿数据</div>
              <div className="ds-nextDesc">把 queryKey 做到“参数可控”，就能自动刷新/缓存。</div>
            </div>
            <div className="ds-nextItem">
              <div className="ds-nextTitle">3) 用 `DataTable`/卡片/图表渲染</div>
              <div className="ds-nextDesc">示例：用户列表页就是“拿 rows + total → 表格 + 分页”。</div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}
