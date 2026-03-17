import {
  getPortalSoftwareCategories,
  getPortalSoftwareFacets,
  listPortalSoftware,
  type PortalSoftwareCategory,
  type PortalSoftwareListQuery,
  type PortalSoftwareListItem,
} from '@/api/portalSoftware'
import { Button } from '@/ui/Button'
import { Card, CardHeader } from '@/ui/Card'
import { Chip } from '@/ui/Chip'
import { Input } from '@/ui/Input'
import { Select } from '@/ui/Select'
import { Spinner } from '@/ui/Spinner'
import { keepPreviousData, useQuery } from '@tanstack/react-query'
import clsx from 'clsx'
import { useMemo, useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'

const DEFAULT_PAGE_SIZE = 18
const EMPTY_CATEGORIES: PortalSoftwareCategory[] = []

type Filters = {
  keyword: string
  categoryId: string
  openSource: '' | '0' | '1'
  license: string
  tag: string
  platform: string
}

function isGarbled(text: string) {
  return /[\uD800-\uDFFF]/.test(text)
}

function safeLabel(text: string | null | undefined, fallback: string) {
  const t = (text || '').trim()
  if (!t) return fallback
  if (isGarbled(t)) return fallback
  return t
}

function splitTags(raw: string | null | undefined) {
  const safe = (raw || '').replaceAll('，', ',')
  const parts = safe
    .split(',')
    .map((p) => p.trim())
    .filter(Boolean)
  const seen = new Set<string>()
  const result: string[] = []
  for (const p of parts) {
    if (seen.has(p)) continue
    seen.add(p)
    result.push(p)
  }
  return result
}

function compactQuery(input: {
  pageNum: number
  pageSize: number
  filters: Filters
}): PortalSoftwareListQuery {
  const q: PortalSoftwareListQuery = { pageNum: input.pageNum, pageSize: input.pageSize }
  if (input.filters.keyword.trim()) q.keyword = input.filters.keyword.trim()
  if (input.filters.categoryId) q.categoryId = Number(input.filters.categoryId)
  if (input.filters.openSource) q.openSource = input.filters.openSource
  if (input.filters.license.trim()) q.license = input.filters.license.trim()
  if (input.filters.tag.trim()) q.tag = input.filters.tag.trim()
  if (input.filters.platform.trim()) q.platform = input.filters.platform.trim()
  return q
}

function formatDate(iso: string | null | undefined) {
  if (!iso) return '—'
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return '—'
  return new Intl.DateTimeFormat('zh-CN', { dateStyle: 'medium' }).format(d)
}

export function SoftwareHubPage() {
  const navigate = useNavigate()
  const location = useLocation()

  const initial = useMemo(() => {
    const p = new URLSearchParams(window.location.search)
    const toInt = (key: string, fallback: number) => {
      const v = Number.parseInt(p.get(key) || '', 10)
      return Number.isFinite(v) && v > 0 ? v : fallback
    }

    const keyword = p.get('q') || ''
    const categoryId = p.get('cat') || ''
    const openSource = (p.get('os') || '') as Filters['openSource']
    const license = p.get('license') || ''
    const tag = p.get('tag') || ''
    const platform = p.get('platform') || ''

    return {
      pageNum: toInt('page', 1),
      pageSize: toInt('size', DEFAULT_PAGE_SIZE),
      filters: { keyword, categoryId, openSource, license, tag, platform } satisfies Filters,
    }
  }, [])

  const [pageNum, setPageNum] = useState(initial.pageNum)
  const [pageSize, setPageSize] = useState(initial.pageSize)
  const [filters, setFilters] = useState<Filters>(initial.filters)
  const [appliedFilters, setAppliedFilters] = useState<Filters>(filters)

  function syncUrl(next: { pageNum: number; pageSize: number; filters: Filters }) {
    const p = new URLSearchParams()
    if (next.pageNum > 1) p.set('page', String(next.pageNum))
    if (next.pageSize !== DEFAULT_PAGE_SIZE) p.set('size', String(next.pageSize))
    if (next.filters.keyword.trim()) p.set('q', next.filters.keyword.trim())
    if (next.filters.categoryId) p.set('cat', next.filters.categoryId)
    if (next.filters.openSource) p.set('os', next.filters.openSource)
    if (next.filters.license.trim()) p.set('license', next.filters.license.trim())
    if (next.filters.tag.trim()) p.set('tag', next.filters.tag.trim())
    if (next.filters.platform.trim()) p.set('platform', next.filters.platform.trim())

    const search = p.toString() ? `?${p.toString()}` : ''
    navigate({ pathname: location.pathname, search }, { replace: true })
  }

  const effectiveQuery = useMemo(
    () => compactQuery({ pageNum, pageSize, filters: appliedFilters }),
    [pageNum, pageSize, appliedFilters],
  )

  const effectiveQueryWithoutCategory = useMemo(() => {
    return compactQuery({
      pageNum: 1,
      pageSize: 1,
      filters: {
        keyword: appliedFilters.keyword,
        categoryId: '',
        openSource: appliedFilters.openSource,
        license: appliedFilters.license,
        tag: appliedFilters.tag,
        platform: appliedFilters.platform,
      },
    })
  }, [
    appliedFilters.keyword,
    appliedFilters.openSource,
    appliedFilters.license,
    appliedFilters.tag,
    appliedFilters.platform,
  ])

  const categoriesQuery = useQuery({
    queryKey: ['portal', 'software', 'categories'],
    queryFn: getPortalSoftwareCategories,
  })

  const facetsQuery = useQuery({
    queryKey: ['portal', 'software', 'facets'],
    queryFn: () => getPortalSoftwareFacets(60),
  })

  const listQuery = useQuery({
    queryKey: ['portal', 'software', 'list', effectiveQuery],
    queryFn: () => listPortalSoftware(effectiveQuery),
    placeholderData: keepPreviousData,
  })

  const listTotalWithoutCategoryQuery = useQuery({
    queryKey: ['portal', 'software', 'list-total-without-category', effectiveQueryWithoutCategory],
    queryFn: () => listPortalSoftware(effectiveQueryWithoutCategory),
    placeholderData: keepPreviousData,
    enabled: Boolean(appliedFilters.categoryId),
  })

  const categories = categoriesQuery.data?.data ?? EMPTY_CATEGORIES
  const facets = facetsQuery.data?.data
  const rows = listQuery.data?.rows ?? []
  const total = listQuery.data?.total ?? 0
  const pageCount = Math.max(1, Math.ceil(total / pageSize))

  const libraryTotal = useMemo(() => {
    if (!categoriesQuery.data) return null
    return categories.reduce((sum, c) => sum + (c.softwareCount ?? 0), 0)
  }, [categories, categoriesQuery.data])

  const activeFilterCount = useMemo(() => {
    let c = 0
    if (appliedFilters.keyword.trim()) c += 1
    if (appliedFilters.categoryId) c += 1
    if (appliedFilters.openSource) c += 1
    if (appliedFilters.license.trim()) c += 1
    if (appliedFilters.tag.trim()) c += 1
    if (appliedFilters.platform.trim()) c += 1
    return c
  }, [appliedFilters])

  const showLoading =
    categoriesQuery.isLoading || facetsQuery.isLoading || (listQuery.isLoading && !listQuery.data)

  const allCategoryTotalText = useMemo(() => {
    if (!appliedFilters.categoryId) {
      if (listQuery.isFetching && !listQuery.data) return '…'
      return String(total)
    }
    if (listTotalWithoutCategoryQuery.isError) return '—'
    if (listTotalWithoutCategoryQuery.isFetching && !listTotalWithoutCategoryQuery.data) return '…'
    return String(listTotalWithoutCategoryQuery.data?.total ?? 0)
  }, [
    appliedFilters.categoryId,
    listQuery.data,
    listQuery.isFetching,
    listTotalWithoutCategoryQuery.data,
    listTotalWithoutCategoryQuery.isError,
    listTotalWithoutCategoryQuery.isFetching,
    total,
  ])

  const libraryTotalText = useMemo(() => {
    if (categoriesQuery.isFetching && !categoriesQuery.data) return '…'
    if (libraryTotal == null) return '—'
    return String(libraryTotal)
  }, [categoriesQuery.data, categoriesQuery.isFetching, libraryTotal])

  return (
    <div className="ds-portalPad">
      <section className="ds-portalHero" aria-label="软件库">
        <div className="ds-portalHeroText">
          <div className="ds-portalEyebrow ds-mono">DESKOPS · SOFTWARE</div>
          <h1 className="ds-portalTitle">软件库：快速查找、对比与下载</h1>
          <div className="ds-portalLead">
            分类/标签/许可证/平台，一键定位常用工具；支持直达官网、仓库与多平台下载。
          </div>

          <div className="ds-portalSearch">
            <Input
              label="搜索"
              name="keyword"
              value={filters.keyword}
              onChange={(e) => setFilters((s) => ({ ...s, keyword: e.target.value }))}
              placeholder="软件名称 / 描述 / 作者 / 标签…"
              autoComplete="off"
            />
            <div className="ds-portalSearchActions">
              <Button
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
                variant="ghost"
                onClick={() => {
                  const empty: Filters = {
                    keyword: '',
                    categoryId: '',
                    openSource: '',
                    license: '',
                    tag: '',
                    platform: '',
                  }
                  setFilters(empty)
                  setAppliedFilters(empty)
                  setPageNum(1)
                  setPageSize(DEFAULT_PAGE_SIZE)
                  syncUrl({ pageNum: 1, pageSize: DEFAULT_PAGE_SIZE, filters: empty })
                }}
                disabled={activeFilterCount === 0 && pageNum === 1 && pageSize === DEFAULT_PAGE_SIZE}
              >
                清空
              </Button>
            </div>
          </div>

          <div className="ds-portalHeroMeta">
            <div className="ds-portalStat">
              <div className="ds-portalStatKey">当前结果</div>
              <div className="ds-portalStatVal ds-mono">
                {listQuery.isFetching && !listQuery.data ? '…' : String(total)}
              </div>
            </div>
            <div className="ds-portalStat">
              <div className="ds-portalStatKey">筛选条件</div>
              <div className="ds-portalStatVal ds-mono">{activeFilterCount || 0}</div>
            </div>
            <div className="ds-portalStat">
              <div className="ds-portalStatKey">收录总数</div>
              <div className="ds-portalStatVal ds-mono">{libraryTotalText}</div>
            </div>
          </div>
        </div>

        <div className="ds-portalHeroArt" aria-hidden="true">
          <div className="ds-portalHeroOrb" />
          <div className="ds-portalHeroGrid" />
        </div>
      </section>

      <div className="ds-portalGrid">
        <aside className="ds-portalAside">
          <Card>
            <CardHeader title="分类" subtitle="仅显示有上架软件的分类" />
            <div className="ds-portalCats">
              <button
                type="button"
                className={clsx('ds-catItem', !appliedFilters.categoryId && 'ds-catItem--active')}
                onClick={() => {
                  const next = { ...appliedFilters, categoryId: '' }
                  setFilters(next)
                  setAppliedFilters(next)
                  setPageNum(1)
                  syncUrl({ pageNum: 1, pageSize, filters: next })
                }}
              >
                <span>全部</span>
                <span className="ds-catCount ds-mono">{allCategoryTotalText}</span>
              </button>

              {categoriesQuery.isError ? (
                <div className="ds-portalAsideMsg ds-alert ds-alert--error" role="alert">
                  {(categoriesQuery.error as Error)?.message || '分类加载失败'}
                </div>
              ) : (
                categories.map((c) => (
                  <button
                    key={c.categoryId}
                    type="button"
                    className={clsx(
                      'ds-catItem',
                      String(c.categoryId) === appliedFilters.categoryId && 'ds-catItem--active',
                    )}
                    onClick={() => {
                      const next = { ...appliedFilters, categoryId: String(c.categoryId) }
                      setFilters(next)
                      setAppliedFilters(next)
                      setPageNum(1)
                      syncUrl({ pageNum: 1, pageSize, filters: next })
                    }}
                  >
                    <span>{safeLabel(c.categoryName, c.categoryCode || `#${c.categoryId}`)}</span>
                    <span className="ds-catCount ds-mono">{String(c.softwareCount ?? 0)}</span>
                  </button>
                ))
              )}
            </div>
          </Card>

          <Card className="ds-portalAsideCard">
            <CardHeader title="筛选" subtitle="按标签 / 许可证 / 平台快速定位" />
            <div className="ds-portalAsideBody">
              <div className="ds-portalFieldRow">
                <div className="ds-portalFieldTitle">开源</div>
                <div className="ds-portalFieldControls">
                  <Chip
                    size="sm"
                    selected={!appliedFilters.openSource}
                    onClick={() => {
                      const next: Filters = { ...appliedFilters, openSource: '' }
                      setFilters(next)
                      setAppliedFilters(next)
                      setPageNum(1)
                      syncUrl({ pageNum: 1, pageSize, filters: next })
                    }}
                  >
                    全部
                  </Chip>
                  <Chip
                    size="sm"
                    tone="accent"
                    selected={appliedFilters.openSource === '1'}
                    onClick={() => {
                      const next: Filters = { ...appliedFilters, openSource: '1' }
                      setFilters(next)
                      setAppliedFilters(next)
                      setPageNum(1)
                      syncUrl({ pageNum: 1, pageSize, filters: next })
                    }}
                  >
                    仅开源
                  </Chip>
                </div>
              </div>

              <Select
                label="许可证"
                value={appliedFilters.license}
                onChange={(e) => {
                  const next = { ...appliedFilters, license: e.target.value }
                  setFilters(next)
                  setAppliedFilters(next)
                  setPageNum(1)
                  syncUrl({ pageNum: 1, pageSize, filters: next })
                }}
              >
                <option value="">全部</option>
                {(facets?.licenses || []).map((x) => (
                  <option key={x.value} value={x.value}>
                    {x.value} ({x.count})
                  </option>
                ))}
              </Select>

              <Select
                label="平台"
                value={appliedFilters.platform}
                onChange={(e) => {
                  const next = { ...appliedFilters, platform: e.target.value }
                  setFilters(next)
                  setAppliedFilters(next)
                  setPageNum(1)
                  syncUrl({ pageNum: 1, pageSize, filters: next })
                }}
              >
                <option value="">全部</option>
                {(facets?.platforms || []).map((x) => (
                  <option key={x.value} value={x.value}>
                    {x.value} ({x.count})
                  </option>
                ))}
              </Select>

              <div className="ds-portalTags">
                <div className="ds-portalTagsTitle">热门标签</div>
                <div className="ds-portalTagsGrid">
                  {(facets?.tags || []).slice(0, 18).map((t) => (
                    <Chip
                      key={t.value}
                      size="sm"
                      tone="muted"
                      selected={appliedFilters.tag === t.value}
                      onClick={() => {
                        const next = {
                          ...appliedFilters,
                          tag: appliedFilters.tag === t.value ? '' : t.value,
                        }
                        setFilters(next)
                        setAppliedFilters(next)
                        setPageNum(1)
                        syncUrl({ pageNum: 1, pageSize, filters: next })
                      }}
                      title={`${t.value}（${t.count}）`}
                    >
                      <span className="ds-portalTagText">{t.value}</span>
                      <span className="ds-portalTagCount ds-mono">{t.count}</span>
                    </Chip>
                  ))}
                </div>
              </div>

              {facetsQuery.isError ? (
                <div className="ds-portalAsideMsg ds-alert ds-alert--error" role="alert">
                  {(facetsQuery.error as Error)?.message || '筛选项加载失败'}
                </div>
              ) : null}
            </div>
          </Card>
        </aside>

        <section className="ds-portalResults" aria-label="软件列表">
          <div className="ds-portalToolbar">
            <div className="ds-portalToolbarLeft">
              <div className="ds-portalToolbarTitle">软件列表</div>
              <div className="ds-portalToolbarSubtitle">
                {listQuery.isFetching ? '更新中…' : '点击卡片查看详情与下载'}
              </div>
            </div>
            <div className="ds-portalToolbarRight">
              <Select
                label="每页"
                value={String(pageSize)}
                onChange={(e) => {
                  const nextSize = Number.parseInt(e.target.value, 10) || DEFAULT_PAGE_SIZE
                  setPageSize(nextSize)
                  setPageNum(1)
                  syncUrl({ pageNum: 1, pageSize: nextSize, filters: appliedFilters })
                }}
              >
                {[12, 18, 24, 36].map((n) => (
                  <option key={n} value={String(n)}>
                    {n}
                  </option>
                ))}
              </Select>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => listQuery.refetch()}
                disabled={listQuery.isFetching}
              >
                刷新
              </Button>
            </div>
          </div>

          {showLoading ? (
            <div className="ds-portalLoading">
              <Spinner label="正在加载软件库…" />
            </div>
          ) : listQuery.isError ? (
            <div className="ds-alert ds-alert--error" role="alert">
              {(listQuery.error as Error)?.message || '请求失败'}
            </div>
          ) : rows.length ? (
            <>
              <div className="ds-softGrid" role="list">
                {rows.map((r) => (
                  <SoftwareCard
                    key={r.softwareId}
                    item={r}
                    backTo={`${location.pathname}${location.search}`}
                  />
                ))}
              </div>

              <div className="ds-softFooter">
                <div className="ds-softFooterMeta">
                  <span className="ds-muted">总数</span>{' '}
                  <span className="ds-mono">{String(total)}</span>
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
          ) : (
            <div className="ds-portalEmpty">
              <div className="ds-emptyTitle">没有匹配的软件</div>
              <div className="ds-emptyText">换个关键词、标签或分类再试试。</div>
            </div>
          )}
        </section>
      </div>
    </div>
  )
}

function SoftwareCard(props: { item: PortalSoftwareListItem; backTo: string }) {
  const tags = splitTags(props.item.tags).slice(0, 4)
  const icon = props.item.iconUrl?.trim() || ''
  const name = safeLabel(props.item.softwareName, `#${props.item.softwareId}`)

  const category = safeLabel(props.item.categoryName, props.item.categoryId ? `#${props.item.categoryId}` : '未分类')
  const license = (props.item.license || '').trim()
  const openSource = props.item.openSource === '1'

  return (
    <Link
      to={`/software/${props.item.softwareId}`}
      state={{ backTo: props.backTo }}
      className="ds-softCard"
      role="listitem"
    >
      <div className="ds-softTop">
        <div className="ds-softIcon" aria-hidden="true">
          {icon ? (
            <img
              src={icon}
              alt=""
              width={36}
              height={36}
              loading="lazy"
              referrerPolicy="no-referrer"
              onError={(e) => {
                ;(e.currentTarget as HTMLImageElement).style.display = 'none'
              }}
            />
          ) : (
            <span className="ds-softIconFallback" />
          )}
        </div>

        <div className="ds-softMeta">
          <div className="ds-softName">{name}</div>
          <div className="ds-softSub">
            <span className="ds-softCategory">{category}</span>
            {license ? (
              <>
                <span className="ds-softDot" aria-hidden="true" />
                <span className="ds-softLicense ds-mono">{license}</span>
              </>
            ) : null}
          </div>
        </div>

        <div className="ds-softBadges">
          {openSource ? <span className="ds-pill ds-pill--ok">OSS</span> : null}
        </div>
      </div>

      <div className="ds-softDesc">{props.item.shortDesc || '—'}</div>

      <div className="ds-softBottom">
        <div className="ds-softTags">
          {tags.length
            ? tags.map((t) => (
                <span key={t} className="ds-chip ds-chip--sm ds-chip--muted ds-chip--static">
                  {t}
                </span>
              ))
            : null}
        </div>
        <div className="ds-softTime ds-mono">{formatDate(props.item.updateTime)}</div>
      </div>
    </Link>
  )
}


