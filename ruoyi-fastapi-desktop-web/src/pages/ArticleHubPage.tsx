import {
  getPortalArticleCategories,
  getPortalArticleTags,
  listPortalArticle,
  type PortalArticleCategory,
  type PortalArticleTag,
  type PortalArticleListItem,
  type PortalArticleListQuery,
} from '@/api/portalArticle'
import { Button } from '@/ui/Button'
import { Chip } from '@/ui/Chip'
import { Input } from '@/ui/Input'
import { Select } from '@/ui/Select'
import { Spinner } from '@/ui/Spinner'
import { keepPreviousData, useQuery } from '@tanstack/react-query'
import clsx from 'clsx'
import { useMemo, useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'

const DEFAULT_PAGE_SIZE = 18

type Filters = {
  keyword: string
  tag: string
  categoryId: string
  articleType: string
}

const ARTICLE_TYPE_OPTIONS = [
  { value: 'tutorial', label: '教程' },
  { value: 'note', label: '笔记' },
  { value: 'faq', label: 'FAQ' },
] as const

function articleTypeLabel(value: string | null | undefined) {
  const v = (value || '').trim()
  if (!v) return '教程'
  const hit = ARTICLE_TYPE_OPTIONS.find((x) => x.value === v)
  return hit?.label || '教程'
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

function compactQuery(input: { pageNum: number; pageSize: number; filters: Filters }): PortalArticleListQuery {
  const q: PortalArticleListQuery = { pageNum: input.pageNum, pageSize: input.pageSize }
  if (input.filters.keyword.trim()) q.keyword = input.filters.keyword.trim()
  if (input.filters.categoryId.trim()) {
    const n = Number.parseInt(input.filters.categoryId.trim(), 10)
    if (Number.isFinite(n) && n > 0) q.categoryId = n
  }
  if (input.filters.tag.trim()) q.tag = input.filters.tag.trim()
  if (input.filters.articleType.trim()) q.articleType = input.filters.articleType.trim()
  return q
}

function formatDate(iso: string | null | undefined) {
  if (!iso) return '—'
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return '—'
  return new Intl.DateTimeFormat('zh-CN', { dateStyle: 'medium' }).format(d)
}

export function ArticleHubPage() {
  const navigate = useNavigate()
  const location = useLocation()

  const initial = useMemo(() => {
    const p = new URLSearchParams(window.location.search)
    const toInt = (key: string, fallback: number) => {
      const v = Number.parseInt(p.get(key) || '', 10)
      return Number.isFinite(v) && v > 0 ? v : fallback
    }

    const keyword = p.get('q') || ''
    const tag = p.get('tag') || ''
    const categoryId = p.get('cat') || ''
    const articleType = p.get('type') || ''

    return {
      pageNum: toInt('page', 1),
      pageSize: toInt('size', DEFAULT_PAGE_SIZE),
      filters: { keyword, tag, categoryId, articleType } satisfies Filters,
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
    if (next.filters.categoryId.trim()) p.set('cat', next.filters.categoryId.trim())
    if (next.filters.tag.trim()) p.set('tag', next.filters.tag.trim())
    if (next.filters.articleType.trim()) p.set('type', next.filters.articleType.trim())

    const search = p.toString() ? `?${p.toString()}` : ''
    navigate({ pathname: location.pathname, search }, { replace: true })
  }

  const categoryQuery = useQuery({
    queryKey: ['portal', 'article', 'categories'],
    queryFn: () => getPortalArticleCategories(),
    staleTime: 60_000,
  })

  const tagQuery = useQuery({
    queryKey: ['portalArticleTags'],
    queryFn: async () => {
      const res = await getPortalArticleTags(50)
      return res.data || []
    },
    staleTime: 60_000,
  })

  const hotTags = useMemo(() => {
    const list = (tagQuery.data || []) as PortalArticleTag[]
    return list
      .map((x) => ({
        tagId: Number(x.tagId),
        tagName: String(x.tagName || '').trim(),
        articleCount: Number(x.articleCount || 0),
      }))
      .filter((x) => Number.isFinite(x.tagId) && x.tagId > 0 && x.tagName)
  }, [tagQuery.data])

  const categories = useMemo(() => {
    const list = (categoryQuery.data?.data || []) as PortalArticleCategory[]
    return list
  }, [categoryQuery.data])

  const effectiveQuery = useMemo(
    () => compactQuery({ pageNum, pageSize, filters: appliedFilters }),
    [pageNum, pageSize, appliedFilters],
  )

  const listQuery = useQuery({
    queryKey: ['portal', 'article', 'list', effectiveQuery],
    queryFn: () => listPortalArticle(effectiveQuery),
    placeholderData: keepPreviousData,
  })

  const listTotalAllQuery = useQuery({
    queryKey: ['portal', 'article', 'total'],
    queryFn: () => listPortalArticle({ pageNum: 1, pageSize: 1 }),
    staleTime: 60_000,
  })

  const rows = listQuery.data?.rows || []
  const total = listQuery.data?.total ?? 0
  const pageCount = Math.max(1, Math.ceil(total / pageSize))

  const activeFilterCount = useMemo(() => {
    let c = 0
    if (appliedFilters.keyword.trim()) c += 1
    if (appliedFilters.categoryId.trim()) c += 1
    if (appliedFilters.tag.trim()) c += 1
    if (appliedFilters.articleType.trim()) c += 1
    return c
  }, [appliedFilters])

  const libraryTotalText = useMemo(() => {
    if (listTotalAllQuery.isError) return '—'
    if (listTotalAllQuery.isFetching && !listTotalAllQuery.data) return '…'
    return String(listTotalAllQuery.data?.total ?? '—')
  }, [listTotalAllQuery.data, listTotalAllQuery.isError, listTotalAllQuery.isFetching])

  const showLoading = listQuery.isLoading && !listQuery.data

  return (
    <div className="ds-portalPad">
      <section className="ds-portalHero" aria-label="教程/文章">
        <div className="ds-portalHeroText">
          <div className="ds-portalEyebrow ds-mono">DESKOPS · ARTICLES</div>
          <h1 className="ds-portalTitle">教程：步骤清晰，关联软件一键直达</h1>
          <div className="ds-portalLead">
            文章为 Markdown，支持分类与标签筛选；关联软件可直接跳到详情与下载。
          </div>

          <div className="ds-portalSearch">
            <div className="ds-portalSearchFields">
              <Input
                label="搜索"
                name="keyword"
                value={filters.keyword}
                onChange={(e) => setFilters((s) => ({ ...s, keyword: e.target.value }))}
                placeholder="标题 / 摘要…"
                autoComplete="off"
              />
              <Select
                label="分类"
                value={filters.categoryId}
                onChange={(e) => setFilters((s) => ({ ...s, categoryId: e.target.value }))}
                disabled={categoryQuery.isFetching && !categoryQuery.data}
              >
                <option value="">全部</option>
                {categories.map((c) => (
                  <option key={c.categoryId} value={String(c.categoryId)}>
                    {safeLabel(c.categoryName, `#${c.categoryId}`)} ({c.articleCount})
                  </option>
                ))}
              </Select>
              <Input
                label="标签"
                name="tag"
                value={filters.tag}
                onChange={(e) => setFilters((s) => ({ ...s, tag: e.target.value }))}
                placeholder="单个标签（可选）"
                autoComplete="off"
              />
              <Select
                label="类型"
                value={filters.articleType}
                onChange={(e) => setFilters((s) => ({ ...s, articleType: e.target.value }))}
              >
                <option value="">全部</option>
                {ARTICLE_TYPE_OPTIONS.map((t) => (
                  <option key={t.value} value={t.value}>
                    {t.label}
                  </option>
                ))}
              </Select>
            </div>

            {hotTags.length ? (
              <div className="ds-portalChips" aria-label="热门标签">
                {hotTags.slice(0, 16).map((t) => {
                  const active = appliedFilters.tag.trim() === t.tagName
                  return (
                    <Chip
                      key={t.tagId}
                      selected={active}
                      tone={active ? 'accent' : 'muted'}
                      size="sm"
                      title={`${t.tagName}（${t.articleCount}）`}
                      onClick={() => {
                        const nextTag = active ? '' : t.tagName
                        const nextFilters = { ...filters, tag: nextTag }
                        setFilters(nextFilters)
                        setAppliedFilters(nextFilters)
                        setPageNum(1)
                        syncUrl({ pageNum: 1, pageSize, filters: nextFilters })
                      }}
                    >
                      {t.tagName}
                      <span className="ds-chipCount">{t.articleCount}</span>
                    </Chip>
                  )
                })}
              </div>
            ) : null}

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
                  const empty: Filters = { keyword: '', tag: '', categoryId: '', articleType: '' }
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

      <section className="ds-portalResults" aria-label="文章列表">
        <div className="ds-portalToolbar">
          <div className="ds-portalToolbarLeft">
            <div className="ds-portalToolbarTitle">文章列表</div>
            <div className="ds-portalToolbarSubtitle">
              {listQuery.isFetching ? '更新中…' : '点击卡片查看正文与关联软件'}
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
            <Button variant="ghost" size="sm" onClick={() => listQuery.refetch()} disabled={listQuery.isFetching}>
              刷新
            </Button>
          </div>
        </div>

        {showLoading ? (
          <div className="ds-portalLoading">
            <Spinner label="正在加载文章…" />
          </div>
        ) : listQuery.isError ? (
          <div className="ds-alert ds-alert--error" role="alert">
            {(listQuery.error as Error)?.message || '请求失败'}
          </div>
        ) : rows.length ? (
          <>
            <div className="ds-softGrid" role="list">
              {rows.map((r) => (
                <ArticleCard key={r.articleId} item={r} backTo={`${location.pathname}${location.search}`} />
              ))}
            </div>

            <div className="ds-softFooter">
              <div className="ds-softFooterMeta">
                <span className="ds-muted">总数</span> <span className="ds-mono">{String(total)}</span>
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
            <div className="ds-emptyTitle">没有匹配的文章</div>
            <div className="ds-emptyText">换个关键词或标签再试试。</div>
          </div>
        )}
      </section>
    </div>
  )
}

function ArticleCard(props: { item: PortalArticleListItem; backTo: string }) {
  const title = safeLabel(props.item.title, `#${props.item.articleId}`)
  const cover = props.item.coverUrl?.trim() || ''
  const tags = splitTags(props.item.tags).slice(0, 4)
  const summary = (props.item.summary || '').trim() || '暂无摘要'
  const time = formatDate(props.item.publishTime || props.item.updateTime)
  const typeLabel = articleTypeLabel(props.item.articleType)

  return (
    <Link to={`/article/${props.item.articleId}`} state={{ backTo: props.backTo }} className="ds-softCard" role="listitem">
      <div className="ds-softTop">
        <div className="ds-softIcon" aria-hidden="true">
          {cover ? (
            <img
              src={cover}
              alt=""
              width={44}
              height={44}
              loading="lazy"
              referrerPolicy="no-referrer"
              style={{ width: 44, height: 44, objectFit: 'cover' }}
              onError={(e) => {
                ;(e.currentTarget as HTMLImageElement).style.display = 'none'
              }}
            />
          ) : (
            <span className="ds-softIconFallback" />
          )}
        </div>

        <div className="ds-softMeta">
          <div className="ds-softName">{title}</div>
          <div className="ds-softSub">
            <span className="ds-pill ds-pill--neutral">{typeLabel}</span>
            <span className="ds-softDot" aria-hidden="true" />
            <span className="ds-muted">
              发布于 <span className="ds-mono">{time}</span>
            </span>
          </div>
        </div>

        <div className="ds-softBadges">
          {tags.length ? <span className={clsx('ds-pill', 'ds-pill--muted')}>{tags.length} tags</span> : null}
        </div>
      </div>

      <div className="ds-softDesc">{summary}</div>

      <div className="ds-softBottom">
        <div className="ds-softTags">
          {tags.length
            ? tags.map((t) => (
                <Chip
                  key={t}
                  size="sm"
                  tone="muted"
                  className="ds-chip--static"
                  disabled
                  aria-hidden="true"
                  tabIndex={-1}
                  title={t}
                >
                  {t}
                </Chip>
              ))
            : (
                <span className="ds-muted">无标签</span>
              )}
        </div>
        <div className="ds-softTime ds-mono">{time}</div>
      </div>
    </Link>
  )
}

