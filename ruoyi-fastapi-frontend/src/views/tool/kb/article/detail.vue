<template>
  <div class="app-container kb-article-detail">
    <section class="header">
      <div class="header-left">
        <el-button icon="ArrowLeft" @click="goList">返回</el-button>
        <div class="title">
          <div class="name">
            <el-skeleton v-if="loading" animated :rows="0">
              <template #template>
                <el-skeleton-item variant="text" style="width: 240px; height: 22px" />
              </template>
            </el-skeleton>
            <span v-else>{{ detail.title || '教程详情' }}</span>
          </div>
          <div class="sub" v-if="!loading">
            <span>ID：{{ detail.articleId || '-' }}</span>
            <span class="dot">•</span>
            <span>更新时间：{{ parseTime(detail.updateTime) || '-' }}</span>
          </div>
        </div>
      </div>

      <div class="header-right">
        <el-tag effect="plain" :type="publishStatusTagType(detail.publishStatus)" v-if="!loading">
          {{ publishStatusLabel(detail.publishStatus) }}
        </el-tag>
        <dict-tag v-if="!loading && detail.status" :options="sys_normal_disable" :value="detail.status" />
        <el-button text icon="Refresh" :loading="loading" @click="loadDetail">刷新</el-button>
        <el-button type="primary" icon="Edit" @click="goEdit" v-hasPermi="['tool:kb:article:edit']">编辑</el-button>
      </div>
    </section>

  <el-row :gutter="16">
      <el-col :xs="24" :lg="16">
        <el-card shadow="never" class="content-card" v-loading="loading">
          <template #header>
            <div class="card-hd">
              <div class="card-title">正文（Markdown）</div>
              <el-tag v-if="detail.publishTime" size="small" effect="plain" type="info">
                发布时间：{{ parseTime(detail.publishTime) }}
              </el-tag>
            </div>
          </template>

          <div class="md-preview">
            <MarkdownRender :content="detail.contentMd || ''" />
            <div class="muted" v-if="!detail.contentMd">暂无正文</div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="8">
        <el-card shadow="never" class="info-card" v-loading="loading">
          <template #header>
            <div class="card-hd">
              <div class="card-title">信息</div>
            </div>
          </template>

          <div class="cover" v-if="detail.coverUrl">
            <img :src="detail.coverUrl" alt="封面" referrerpolicy="no-referrer" />
          </div>

          <div class="kv">
            <div class="kv-item">
              <span class="k">摘要</span>
              <span class="v">{{ detail.summary || '-' }}</span>
            </div>
            <div class="kv-item">
              <span class="k">类型</span>
              <span class="v">
                <dict-tag v-if="detail.articleType" :options="kb_article_type" :value="detail.articleType" />
                <span v-else>-</span>
              </span>
            </div>
            <div class="kv-item">
              <span class="k">排序</span>
              <span class="v">{{ detail.articleSort ?? '-' }}</span>
            </div>
          </div>

          <div class="tags">
            <div class="tags-hd">标签</div>
            <div class="tag-list" v-if="tagList.length">
              <el-tag v-for="t in tagList" :key="t" size="small" effect="plain">{{ t }}</el-tag>
            </div>
            <div class="muted" v-else>暂无标签</div>
          </div>
        </el-card>

        <el-card shadow="never" class="table-card" v-loading="loading">
          <template #header>
            <div class="card-hd">
              <div class="card-title">附件</div>
              <el-tag size="small" effect="plain" type="info">{{ attachmentsList.length }} 个</el-tag>
            </div>
          </template>

          <el-table v-if="attachmentsList.length" :data="attachmentsList" size="small" border>
            <el-table-column label="#" width="56" align="center">
              <template #default="scope">
                {{ scope.$index + 1 }}
              </template>
            </el-table-column>
            <el-table-column label="文件" min-width="220">
              <template #default="scope">
                <el-button link type="primary" @click="openAttachment(scope.row)">{{ scope.row.name }}</el-button>
                <div class="muted" v-if="scope.row.size">{{ formatFileSize(scope.row.size) }}</div>
              </template>
            </el-table-column>
            <el-table-column label="链接" min-width="240">
              <template #default="scope">
                <el-link :href="scope.row.url" target="_blank" type="info" :underline="false">
                  {{ scope.row.url }}
                </el-link>
              </template>
            </el-table-column>
          </el-table>

          <el-empty v-else-if="!loading" description="暂无附件" :image-size="68" />
        </el-card>

        <el-card shadow="never" class="table-card" v-loading="loading">
          <template #header>
            <div class="card-hd">
              <div class="card-title">关联软件</div>
              <el-tag size="small" effect="plain" type="info">{{ relatedSoftwares.length }} 个</el-tag>
            </div>
          </template>

          <el-table :data="relatedSoftwares" size="small" border>
            <el-table-column label="#" width="56" align="center">
              <template #default="scope">
                {{ scope.$index + 1 }}
              </template>
            </el-table-column>
            <el-table-column label="软件" min-width="220">
              <template #default="scope">
                <div class="soft-cell">
                  <el-avatar class="soft-icon" shape="square" :size="26" :src="scope.row.iconUrl">
                    {{ (scope.row.softwareName || '').slice(0, 1) }}
                  </el-avatar>
                  <div class="soft-text">
                    <el-button link type="primary" class="soft-name" @click="goSoftwareDetail(scope.row.softwareId)">
                      {{ scope.row.softwareName || '-' }}
                    </el-button>
                    <div class="soft-meta">
                      <span>{{ scope.row.categoryName || '未分类' }}</span>
                      <span class="dot">•</span>
                      <span>ID：{{ scope.row.softwareId }}</span>
                    </div>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="发布" width="96" align="center">
              <template #default="scope">
                <el-tag effect="plain" :type="softwarePublishTagType(scope.row.publishStatus)">
                  {{ softwarePublishLabel(scope.row.publishStatus) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="更新时间" width="170" align="center">
              <template #default="scope">
                <span>{{ parseTime(scope.row.updateTime) }}</span>
              </template>
            </el-table-column>
          </el-table>

          <el-empty v-if="!relatedSoftwares.length && !loading" description="暂无关联软件" :image-size="68" />
        </el-card>
      </el-col>
    </el-row>

    <el-empty v-if="!articleId && !loading" description="缺少 articleId 参数" />
  </div>
</template>

<script setup name="KbArticleDetail">
import { MarkdownRender } from 'markstream-vue'
import 'markstream-vue/index.css'

import { getKbArticle } from '@/api/tool/kb/article'
import { getSoftwareItem } from '@/api/tool/software/item'
import { parseTime } from '@/utils/ruoyi'

const { proxy } = getCurrentInstance()
const { sys_normal_disable, kb_article_type } = proxy.useDict('sys_normal_disable', 'kb_article_type')

const router = useRouter()
const route = useRoute()

const loading = ref(false)

const detail = reactive({
  articleId: undefined,
  title: undefined,
  summary: undefined,
  coverUrl: undefined,
  contentMd: undefined,
  tags: undefined,
  articleType: undefined,
  attachments: undefined,
  publishStatus: '0',
  publishTime: undefined,
  articleSort: 0,
  status: '0',
  updateTime: undefined,
  softwareIds: []
})

const softwareMeta = ref({})

const articleId = computed(() => {
  const raw = route.query.articleId
  const n = Number(raw)
  return Number.isFinite(n) && n > 0 ? n : 0
})

const tagList = computed(() => splitTags(detail.tags).slice(0, 48))

const attachmentsList = computed(() => {
  const raw = detail.attachments
  if (!raw) return []
  if (Array.isArray(raw)) {
    return raw
      .map((x) => ({
        name: String(x?.name || '').trim(),
        url: String(x?.url || '').trim(),
        size: x?.size
      }))
      .filter((x) => x.name && x.url)
  }
  const text = String(raw || '').trim()
  if (!text) return []
  try {
    const arr = JSON.parse(text)
    if (!Array.isArray(arr)) return []
    return arr
      .map((x) => ({
        name: String(x?.name || '').trim(),
        url: String(x?.url || '').trim(),
        size: x?.size
      }))
      .filter((x) => x.name && x.url)
  } catch (e) {
    return []
  }
})

const relatedSoftwares = computed(() => {
  const ids = Array.isArray(detail.softwareIds) ? detail.softwareIds : []
  return ids
    .map((id) => Number(id))
    .filter((id) => Number.isFinite(id) && id > 0)
    .map((id) => {
      const meta = softwareMeta.value?.[String(id)] || {}
      return {
        softwareId: id,
        softwareName: meta.softwareName || `软件 #${id}`,
        categoryName: meta.categoryName,
        iconUrl: meta.iconUrl,
        publishStatus: meta.publishStatus,
        updateTime: meta.updateTime
      }
    })
})

function splitTags(raw) {
  const s = String(raw || '')
    .replace(/，/g, ',')
    .replace(/；/g, ',')
    .replace(/;/g, ',')
    .replace(/\r\n/g, ',')
    .replace(/\n/g, ',')
    .replace(/\r/g, ',')
    .replace(/\t/g, ',')
  const parts = s
    .split(',')
    .map((x) => x.trim())
    .filter(Boolean)
  const seen = new Set()
  const out = []
  for (const p of parts) {
    if (seen.has(p)) continue
    seen.add(p)
    out.push(p)
  }
  return out
}

function publishStatusLabel(value) {
  if (value === '1') return '发布'
  if (value === '2') return '下线'
  return '草稿'
}

function publishStatusTagType(value) {
  if (value === '1') return 'success'
  if (value === '2') return 'warning'
  return 'info'
}

function softwarePublishLabel(value) {
  if (value === '1') return '上架'
  if (value === '2') return '下架'
  return '草稿'
}

function softwarePublishTagType(value) {
  if (value === '1') return 'success'
  if (value === '2') return 'warning'
  return 'info'
}

function formatFileSize(size) {
  const n = Number(size)
  if (!Number.isFinite(n) || n <= 0) return ''
  const kb = n / 1024
  if (kb < 1024) return `${kb.toFixed(kb < 10 ? 1 : 0)} KB`
  const mb = kb / 1024
  if (mb < 1024) return `${mb.toFixed(mb < 10 ? 1 : 0)} MB`
  const gb = mb / 1024
  return `${gb.toFixed(gb < 10 ? 1 : 0)} GB`
}

function openAttachment(item) {
  const url = String(item?.url || '').trim()
  if (!url) return
  window.open(url, '_blank')
}

function goList() {
  const fallbackTimer = window.setTimeout(() => {
    if (router.currentRoute.value?.path !== '/kb/article') {
      window.location.assign('/kb/article')
    }
  }, 320)

  Promise.resolve(router.push({ path: '/kb/article' }))
    .then(() => {
      if (router.currentRoute.value?.path === '/kb/article') {
        window.clearTimeout(fallbackTimer)
        return
      }
      try {
        router.back()
      } catch (e) {}
    })
    .catch(() => {
      try {
        router.back()
      } catch (e) {}
    })
}

function goEdit() {
  if (!articleId.value) return
  router.push({ path: '/kb/article/edit', query: { articleId: articleId.value } })
}

function goSoftwareDetail(softwareId) {
  const n = Number(softwareId)
  if (!Number.isFinite(n) || n <= 0) return
  router.push({ path: '/software/detail', query: { softwareId: n } })
}

async function hydrateSoftwares(ids) {
  const unique = Array.from(new Set((ids || []).map((x) => Number(x)).filter((x) => Number.isFinite(x) && x > 0)))
  if (!unique.length) return

  const tasks = unique.map(async (id) => {
    if (softwareMeta.value?.[String(id)]) return
    try {
      const res = await getSoftwareItem(id)
      const data = res.data || {}
      softwareMeta.value = { ...softwareMeta.value, [String(id)]: data }
    } catch (e) {
      softwareMeta.value = {
        ...softwareMeta.value,
        [String(id)]: { softwareId: id, softwareName: `软件 #${id}` }
      }
    }
  })
  await Promise.all(tasks)
}

function resetDetail() {
  Object.assign(detail, {
    articleId: undefined,
    title: undefined,
    summary: undefined,
    coverUrl: undefined,
    contentMd: undefined,
    tags: undefined,
    publishStatus: '0',
    publishTime: undefined,
    articleSort: 0,
    status: '0',
    updateTime: undefined,
    softwareIds: []
  })
  softwareMeta.value = {}
}

function loadDetail() {
  if (!articleId.value) return
  loading.value = true
  getKbArticle(articleId.value)
    .then(async (res) => {
      const data = res.data || {}
      resetDetail()
      Object.assign(detail, data)
      detail.softwareIds = Array.isArray(data.softwareIds) ? data.softwareIds : []
      await hydrateSoftwares(detail.softwareIds)
    })
    .catch(() => {})
    .finally(() => {
      loading.value = false
    })
}

watch(
  () => articleId.value,
  (id) => {
    if (id) loadDetail()
  },
  { immediate: true }
)
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.title {
  min-width: 0;
}

.name {
  font-size: 18px;
  font-weight: 750;
  color: var(--el-text-color-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sub {
  margin-top: 2px;
  color: var(--el-text-color-secondary);
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot {
  opacity: 0.7;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.info-card,
.content-card,
.table-card {
  border-radius: 16px;
  border: 1px solid var(--app-border);
  background: color-mix(in srgb, var(--app-surface) 92%, transparent);
  margin-bottom: 12px;
}

.card-hd {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.card-title {
  font-weight: 800;
}

.cover {
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--app-border);
  background: var(--el-fill-color-lighter);
  margin-bottom: 10px;
}

.cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.kv {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}

.kv-item {
  display: flex;
  gap: 10px;
  align-items: baseline;
  justify-content: space-between;
}

.kv-item .k {
  color: var(--el-text-color-secondary);
  white-space: nowrap;
}

.kv-item .v {
  color: var(--el-text-color-primary);
  text-align: right;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tags {
  margin-top: 14px;
}

.tags-hd {
  font-weight: 700;
  margin-bottom: 8px;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.md-preview {
  min-height: 260px;
}

.muted {
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

.soft-cell {
  display: flex;
  gap: 10px;
  align-items: center;
}

.soft-text {
  min-width: 0;
}

.soft-name {
  padding: 0;
  font-weight: 750;
}

.soft-meta {
  margin-top: 2px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
  display: flex;
  align-items: center;
  gap: 6px;
}
</style>
