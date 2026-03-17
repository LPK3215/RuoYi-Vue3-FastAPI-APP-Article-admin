import { listPortalArticle } from '@/api/portalArticle'
import { getPortalSoftwareDetail } from '@/api/portalSoftware'
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

export function SoftwareDetailPage() {
  const params = useParams()
  const navigate = useNavigate()
  const location = useLocation()

  const softwareId = Number(params.softwareId || '')
  const backTo = (location.state as { backTo?: string } | null)?.backTo || '/'
  const currentBackTo = `${location.pathname}${location.search}`

  const detailQuery = useQuery({
    queryKey: ['portal', 'software', 'detail', softwareId],
    queryFn: () => getPortalSoftwareDetail(softwareId),
    enabled: Number.isFinite(softwareId) && softwareId > 0,
  })

  const data = detailQuery.data?.data

  const relatedArticlesQuery = useQuery({
    queryKey: ['portal', 'article', 'list', { pageNum: 1, pageSize: 6, softwareId }],
    queryFn: () => listPortalArticle({ pageNum: 1, pageSize: 6, softwareId }),
    enabled: Number.isFinite(softwareId) && softwareId > 0,
  })

  const relatedArticles = relatedArticlesQuery.data?.rows || []

  const downloads = useMemo(() => {
    const list = data?.downloads ? [...data.downloads] : []
    list.sort((a, b) => (a.sort ?? 0) - (b.sort ?? 0))
    return list
  }, [data])

  const resources = useMemo(() => {
    const list = data?.resources ? [...data.resources] : []
    list.sort((a, b) => (a.sort ?? 0) - (b.sort ?? 0))
    return list
  }, [data])

  const tags = splitTags(data?.tags)
  const name = safeLabel(data?.softwareName, `#${softwareId}`)
  const category = safeLabel(data?.categoryName, data?.categoryId ? `#${data.categoryId}` : '未分类')

  const icon = data?.iconUrl?.trim() || ''
  const officialUrl = data?.officialUrl?.trim() || ''
  const repoUrl = data?.repoUrl?.trim() || ''

  return (
    <div className="ds-portalPad">
      <div className="ds-detailTop">
        <Button variant="ghost" size="sm" onClick={() => navigate(backTo)}>
          ← 返回列表
        </Button>

        <div className="ds-detailTopRight">
          {officialUrl ? (
            <a className={clsx('ds-btn', 'ds-btn--ghost', 'ds-btn--sm')} href={officialUrl} target="_blank" rel="noreferrer">
              官网
            </a>
          ) : null}
          {repoUrl ? (
            <a className={clsx('ds-btn', 'ds-btn--ghost', 'ds-btn--sm')} href={repoUrl} target="_blank" rel="noreferrer">
              仓库
            </a>
          ) : null}
        </div>
      </div>

      {detailQuery.isLoading ? (
        <div className="ds-portalLoading">
          <Spinner label="正在加载软件详情…" />
        </div>
      ) : detailQuery.isError ? (
        <div className="ds-alert ds-alert--error" role="alert">
          {(detailQuery.error as Error)?.message || '加载失败'}
        </div>
      ) : !data ? (
        <div className="ds-alert ds-alert--error" role="alert">
          软件不存在或未上架
        </div>
      ) : (
        <>
          <section className="ds-detailHero">
            <div className="ds-detailHeroLeft">
              <div className="ds-detailIcon" aria-hidden="true">
                {icon ? (
                  <img
                    src={icon}
                    alt=""
                    width={56}
                    height={56}
                    loading="eager"
                    referrerPolicy="no-referrer"
                    onError={(e) => {
                      ;(e.currentTarget as HTMLImageElement).style.display = 'none'
                    }}
                  />
                ) : (
                  <span className="ds-softIconFallback" />
                )}
              </div>

              <div className="ds-detailHeroText">
                <div className="ds-detailName">{name}</div>
                <div className="ds-detailSub">{data.shortDesc || '—'}</div>
                <div className="ds-detailMeta">
                  <span className="ds-chip ds-chip--sm ds-chip--neutral ds-chip--static">{category}</span>
                  {data.license ? (
                    <span className="ds-chip ds-chip--sm ds-chip--muted ds-chip--static ds-mono">
                      {data.license}
                    </span>
                  ) : null}
                  {data.openSource === '1' ? (
                    <span className="ds-pill ds-pill--ok">开源</span>
                  ) : (
                    <span className="ds-pill ds-pill--muted">闭源</span>
                  )}
                  <span className="ds-muted">
                    更新于 <span className="ds-mono">{formatDateTime(data.updateTime)}</span>
                  </span>
                </div>
              </div>
            </div>

            <div className="ds-detailHeroRight">
              <div className="ds-detailTags">
                {tags.length ? (
                  tags.slice(0, 12).map((t) => (
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
                <CardHeader title="介绍" subtitle="descriptionMd" />
                <div className="ds-detailBody">
                  <Markdown>{data.descriptionMd}</Markdown>
                  {!data.descriptionMd ? <div className="ds-muted">暂无介绍</div> : null}
                </div>
              </Card>

              <Card className="ds-detailCardGap">
                <CardHeader title="使用说明" subtitle="usageMd" />
                <div className="ds-detailBody">
                  <Markdown>{data.usageMd}</Markdown>
                  {!data.usageMd ? <div className="ds-muted">暂无使用说明</div> : null}
                </div>
              </Card>
            </div>

            <aside className="ds-detailAside">
              <Card>
                <CardHeader title="下载" subtitle="按平台" />
                <div className="ds-detailAsideBody">
                  {downloads.length ? (
                    <div className="ds-detailDownloads">
                      {downloads.map((d, idx) => (
                        <a
                          key={`${d.platform}-${idx}`}
                          className={clsx('ds-btn', 'ds-btn--primary', 'ds-btn--md', 'ds-btnLink')}
                          href={d.downloadUrl}
                          target="_blank"
                          rel="noreferrer"
                        >
                          <span className="ds-detailDownloadLeft">
                            <span className="ds-detailDownloadPlatform">{d.platform}</span>
                            {d.version ? (
                              <span className="ds-detailDownloadVersion ds-mono">{d.version}</span>
                            ) : null}
                          </span>
                          <span className="ds-detailDownloadRight ds-mono">↓</span>
                        </a>
                      ))}
                    </div>
                  ) : (
                    <div className="ds-muted">暂无下载配置</div>
                  )}
                </div>
              </Card>

              <Card className="ds-detailCardGap">
                <CardHeader title="资源" subtitle="相关链接" />
                <div className="ds-detailAsideBody">
                  {resources.length ? (
                    <div className="ds-detailResources">
                      {resources.map((r, idx) => (
                        <a
                          key={`${r.resourceType}-${idx}`}
                          className="ds-detailResource"
                          href={r.resourceUrl}
                          target="_blank"
                          rel="noreferrer"
                        >
                          <div className="ds-detailResourceTitle">
                            {r.title?.trim() ? r.title.trim() : r.resourceType}
                          </div>
                          <div className="ds-detailResourceUrl ds-mono">{r.resourceUrl}</div>
                        </a>
                      ))}
                    </div>
                  ) : (
                    <div className="ds-muted">暂无资源链接</div>
                  )}
                </div>
              </Card>

              <Card className="ds-detailCardGap">
                <CardHeader title="相关教程" subtitle="从教程库跳转阅读" />
                <div className="ds-detailAsideBody">
                  {relatedArticlesQuery.isLoading ? (
                    <div className="ds-muted">正在加载相关教程…</div>
                  ) : relatedArticlesQuery.isError ? (
                    <div className="ds-muted">相关教程加载失败</div>
                  ) : relatedArticles.length ? (
                    <div className="ds-detailResources">
                      {relatedArticles.map((a) => (
                        <Link
                          key={a.articleId}
                          to={`/article/${a.articleId}`}
                          state={{ backTo: currentBackTo }}
                          className={clsx('ds-detailResource')}
                        >
                          <div className="ds-detailResourceTitle">{safeLabel(a.title, `#${a.articleId}`)}</div>
                          <div className="ds-detailResourceUrl ds-mono">
                            {safeLabel(a.summary, formatDateTime(a.publishTime || a.updateTime))}
                          </div>
                        </Link>
                      ))}
                    </div>
                  ) : (
                    <div className="ds-muted">暂无相关教程</div>
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
