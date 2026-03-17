import { getPortalArticleDetail } from '@/api/portalArticle'
import { Button } from '@/ui/Button'
import { Card, CardHeader } from '@/ui/Card'
import { Chip } from '@/ui/Chip'
import { Markdown } from '@/ui/Markdown'
import { Spinner } from '@/ui/Spinner'
import { useQuery } from '@tanstack/react-query'
import clsx from 'clsx'
import { useMemo } from 'react'
import { Link, useLocation, useNavigate, useParams } from 'react-router-dom'

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

function formatDateTime(iso: string | null | undefined) {
  if (!iso) return '—'
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return '—'
  return new Intl.DateTimeFormat('zh-CN', { dateStyle: 'medium', timeStyle: 'short' }).format(d)
}

export function ArticleDetailPage() {
  const params = useParams()
  const navigate = useNavigate()
  const location = useLocation()

  const articleId = Number(params.articleId || '')
  const backTo = (location.state as { backTo?: string } | null)?.backTo || '/articles'

  const detailQuery = useQuery({
    queryKey: ['portal', 'article', 'detail', articleId],
    queryFn: () => getPortalArticleDetail(articleId),
    enabled: Number.isFinite(articleId) && articleId > 0,
  })

  const data = detailQuery.data?.data
  const tags = splitTags(data?.tags).slice(0, 18)

  const title = safeLabel(data?.title, `#${articleId}`)
  const summary = (data?.summary || '').trim()
  const cover = data?.coverUrl?.trim() || ''

  const softwares = useMemo(() => {
    const list = data?.softwares ? [...data.softwares] : []
    return list
  }, [data])

  const currentBackTo = `${location.pathname}${location.search}`

  return (
    <div className="ds-portalPad">
      <div className="ds-detailTop">
        <Button variant="ghost" size="sm" onClick={() => navigate(backTo)}>
          ← 返回文章列表
        </Button>
        <div className="ds-detailTopRight">
          <Button variant="ghost" size="sm" onClick={() => detailQuery.refetch()} disabled={detailQuery.isFetching}>
            刷新
          </Button>
        </div>
      </div>

      {detailQuery.isLoading ? (
        <div className="ds-portalLoading">
          <Spinner label="正在加载文章…" />
        </div>
      ) : detailQuery.isError ? (
        <div className="ds-alert ds-alert--error" role="alert">
          {(detailQuery.error as Error)?.message || '加载失败'}
        </div>
      ) : !data ? (
        <div className="ds-alert ds-alert--error" role="alert">
          文章不存在或未发布
        </div>
      ) : (
        <>
          <section className="ds-detailHero">
            <div className="ds-detailHeroLeft">
              <div className="ds-detailIcon" aria-hidden="true">
                {cover ? (
                  <img
                    src={cover}
                    alt=""
                    width={62}
                    height={62}
                    loading="eager"
                    referrerPolicy="no-referrer"
                    style={{ width: 62, height: 62, objectFit: 'cover' }}
                    onError={(e) => {
                      ;(e.currentTarget as HTMLImageElement).style.display = 'none'
                    }}
                  />
                ) : (
                  <span className="ds-softIconFallback" />
                )}
              </div>

              <div className="ds-detailHeroText">
                <div className="ds-detailName">{title}</div>
                <div className="ds-detailSub">{summary || '—'}</div>
                <div className="ds-detailMeta">
                  <span className="ds-pill ds-pill--neutral">教程</span>
                  <span className="ds-muted">
                    发布时间 <span className="ds-mono">{formatDateTime(data.publishTime || data.updateTime)}</span>
                  </span>
                </div>
              </div>
            </div>

            <div className="ds-detailHeroRight">
              <div className="ds-detailTags">
                {tags.length ? (
                  tags.map((t) => (
                    <Chip
                      key={t}
                      size="sm"
                      tone="muted"
                      className="ds-chip--static"
                      disabled
                      aria-hidden="true"
                      tabIndex={-1}
                    >
                      {t}
                    </Chip>
                  ))
                ) : (
                  <div className="ds-muted">无标签</div>
                )}
              </div>
            </div>
          </section>

          <div className="ds-detailGrid">
            <div className="ds-detailMain">
              <Card>
                <CardHeader title="正文" subtitle="contentMd" />
                <div className="ds-detailBody">
                  <Markdown>{data.contentMd}</Markdown>
                  {!data.contentMd ? <div className="ds-muted">暂无正文</div> : null}
                </div>
              </Card>
            </div>

            <aside className="ds-detailAside">
              <Card>
                <CardHeader title="本文用到的软件" subtitle="点击跳转到下载页" />
                <div className="ds-detailAsideBody">
                  {softwares.length ? (
                    <div className="ds-detailResources">
                      {softwares.map((s) => (
                        <Link
                          key={s.softwareId}
                          to={`/software/${s.softwareId}`}
                          state={{ backTo: currentBackTo }}
                          className={clsx('ds-detailResource')}
                        >
                          <div className="ds-detailResourceTitle">
                            {safeLabel(s.softwareName, `#${s.softwareId}`)}
                          </div>
                          <div className="ds-detailResourceUrl ds-mono">
                            {safeLabel(s.shortDesc, s.categoryName ? String(s.categoryName) : '—')}
                          </div>
                        </Link>
                      ))}
                    </div>
                  ) : (
                    <div className="ds-muted">暂无关联软件</div>
                  )}
                </div>
              </Card>
            </aside>
          </div>
        </>
      )}
    </div>
  )
}

