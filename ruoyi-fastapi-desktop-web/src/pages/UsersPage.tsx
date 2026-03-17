import { listUsers, type ListUsersQuery, type UserRow } from '@/api/system'
import { Button } from '@/ui/Button'
import { Card, CardHeader } from '@/ui/Card'
import { DataTable } from '@/ui/DataTable'
import { Input } from '@/ui/Input'
import { Select } from '@/ui/Select'
import { Spinner } from '@/ui/Spinner'
import { StatusPill } from '@/ui/StatusPill'
import { keepPreviousData, useQuery } from '@tanstack/react-query'
import type { ColumnDef } from '@tanstack/react-table'
import { useMemo, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

function compactQuery(q: ListUsersQuery) {
  const next: ListUsersQuery = { pageNum: q.pageNum, pageSize: q.pageSize }
  if (q.userName?.trim()) next.userName = q.userName.trim()
  if (q.phonenumber?.trim()) next.phonenumber = q.phonenumber.trim()
  if (q.status?.trim()) next.status = q.status.trim()
  return next
}

export function UsersPage() {
  const navigate = useNavigate()
  const location = useLocation()

  const initial = useMemo(() => {
    const p = new URLSearchParams(window.location.search)
    const toInt = (key: string, fallback: number) => {
      const v = Number.parseInt(p.get(key) || '', 10)
      return Number.isFinite(v) && v > 0 ? v : fallback
    }

    const userName = p.get('userName') || ''
    const phonenumber = p.get('phonenumber') || ''
    const status = p.get('status') || ''

    return {
      pageNum: toInt('page', 1),
      pageSize: toInt('size', 10),
      filters: { userName, phonenumber, status },
    }
  }, [])

  const [pageNum, setPageNum] = useState(initial.pageNum)
  const [pageSize, setPageSize] = useState(initial.pageSize)
  const [filters, setFilters] = useState(initial.filters)
  const [appliedFilters, setAppliedFilters] = useState(filters)
  const [selected, setSelected] = useState<UserRow | null>(null)

  function syncUrl(next: { pageNum: number; pageSize: number; filters: typeof filters }) {
    const p = new URLSearchParams()
    p.set('page', String(next.pageNum))
    p.set('size', String(next.pageSize))
    if (next.filters.userName.trim()) p.set('userName', next.filters.userName.trim())
    if (next.filters.phonenumber.trim()) p.set('phonenumber', next.filters.phonenumber.trim())
    if (next.filters.status.trim()) p.set('status', next.filters.status.trim())

    const search = p.toString() ? `?${p.toString()}` : ''
    navigate({ pathname: location.pathname, search }, { replace: true })
  }

  const effectiveQuery = useMemo(
    () => compactQuery({ pageNum, pageSize, ...appliedFilters }),
    [pageNum, pageSize, appliedFilters],
  )

  const usersQuery = useQuery({
    queryKey: ['system', 'user', 'list', effectiveQuery],
    queryFn: () => listUsers(effectiveQuery),
    placeholderData: keepPreviousData,
  })

  const columns = useMemo<Array<ColumnDef<UserRow, unknown>>>(
    () => [
      {
        header: 'ID',
        accessorKey: 'userId',
        cell: (ctx) => <span className="ds-mono">{String(ctx.getValue() ?? '')}</span>,
      },
      { header: '用户名', accessorKey: 'userName' },
      { header: '昵称', accessorKey: 'nickName' },
      {
        header: '部门',
        accessorFn: (row) => row.dept?.deptName || '',
        cell: (ctx) => <span className="ds-muted">{String(ctx.getValue() || '—')}</span>,
      },
      { header: '手机', accessorKey: 'phonenumber' },
      {
        header: '状态',
        accessorKey: 'status',
        cell: (ctx) => <StatusPill value={String(ctx.getValue() ?? '')} />,
      },
      {
        header: '创建时间',
        accessorKey: 'createTime',
        cell: (ctx) => (
          <span className="ds-mono ds-muted">{String(ctx.getValue() || '—')}</span>
        ),
      },
    ],
    [],
  )

  const rows = usersQuery.data?.rows ?? []
  const total = usersQuery.data?.total ?? 0
  const pageCount = Math.max(1, Math.ceil(total / pageSize))

  return (
    <div className="ds-pad">
      <div className="ds-gridUsers">
        <Card className="ds-usersCard">
          <CardHeader
            title="用户列表"
            subtitle="GET /system/user/list → rows/total → 表格渲染"
            right={
              <div className="ds-inline">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => usersQuery.refetch()}
                  disabled={usersQuery.isFetching}
                >
                  刷新
                </Button>
              </div>
            }
          />

          <div className="ds-filters">
            <Input
              label="用户名称"
              value={filters.userName || ''}
              onChange={(e) => setFilters((s) => ({ ...s, userName: e.target.value }))}
              placeholder="userName"
            />
            <Input
              label="手机号码"
              value={filters.phonenumber || ''}
              onChange={(e) => setFilters((s) => ({ ...s, phonenumber: e.target.value }))}
              placeholder="phonenumber"
            />
            <Select
              label="状态"
              value={filters.status || ''}
              onChange={(e) => setFilters((s) => ({ ...s, status: e.target.value }))}
            >
              <option value="">全部</option>
              <option value="0">启用</option>
              <option value="1">停用</option>
            </Select>

            <div className="ds-filterActions">
              <Button
                size="sm"
                onClick={() => {
                  const nextFilters = filters
                  setAppliedFilters(nextFilters)
                  setPageNum(1)
                  syncUrl({ pageNum: 1, pageSize, filters: nextFilters })
                }}
              >
                搜索
              </Button>
              <Button
                size="sm"
                variant="ghost"
                onClick={() => {
                  const empty = { userName: '', phonenumber: '', status: '' }
                  setFilters(empty)
                  setAppliedFilters(empty)
                  setPageNum(1)
                  setPageSize(10)
                  syncUrl({ pageNum: 1, pageSize: 10, filters: empty })
                }}
              >
                重置
              </Button>
            </div>
          </div>

          {usersQuery.isLoading ? (
            <div className="ds-padSm">
              <Spinner label="正在拉取数据…" />
            </div>
          ) : usersQuery.isError ? (
            <div className="ds-padSm">
              <div className="ds-alert ds-alert--error" role="alert">
                {(usersQuery.error as Error)?.message || '请求失败'}
              </div>
            </div>
          ) : (
            <>
              <DataTable<UserRow>
                data={rows}
                columns={columns}
                onRowClick={setSelected}
                busy={usersQuery.isFetching}
              />

              <div className="ds-tableFooter">
                <div className="ds-tableMeta">
                  <span className="ds-muted">总数</span>{' '}
                  <span className="ds-mono">{total}</span>
                  {usersQuery.isFetching ? <span className="ds-muted">（更新中…）</span> : null}
                </div>
                <div className="ds-pager">
                  <Button
                    variant="ghost"
                    size="sm"
                    disabled={pageNum <= 1}
                    onClick={() => {
                      const next = Math.max(1, pageNum - 1)
                      setPageNum(next)
                      syncUrl({ pageNum: next, pageSize, filters: appliedFilters })
                    }}
                  >
                    上一页
                  </Button>
                  <div className="ds-pagerText">
                    <span className="ds-mono">
                      {pageNum}/{pageCount}
                    </span>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    disabled={pageNum >= pageCount}
                    onClick={() => {
                      const next = Math.min(pageCount, pageNum + 1)
                      setPageNum(next)
                      syncUrl({ pageNum: next, pageSize, filters: appliedFilters })
                    }}
                  >
                    下一页
                  </Button>
                </div>
              </div>
            </>
          )}
        </Card>

        <Card className="ds-detailCard">
          <CardHeader title="行详情" subtitle="点一行查看 JSON 详情" />
          {selected ? (
            <pre className="ds-json">{JSON.stringify(selected, null, 2)}</pre>
          ) : (
            <div className="ds-empty">
              <div className="ds-emptyTitle">未选择任何行</div>
              <div className="ds-emptyText">点击表格中的某一行，把接口返回数据直接渲染到这里。</div>
            </div>
          )}
        </Card>
      </div>
    </div>
  )
}
