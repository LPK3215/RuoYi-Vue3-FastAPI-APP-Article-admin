<template>
  <div class="app-container software-detail">
    <section class="header">
      <div class="header-left">
        <el-button icon="ArrowLeft" @click="goBack">返回</el-button>
        <div class="title">
          <div class="name">
            <el-skeleton v-if="loading" animated :rows="0">
              <template #template>
                <el-skeleton-item variant="text" style="width: 220px; height: 22px" />
              </template>
            </el-skeleton>
            <span v-else>{{ detail.softwareName || '软件详情' }}</span>
          </div>
          <div class="sub">
            <span v-if="!loading">ID：{{ detail.softwareId || '-' }}</span>
            <span class="dot" v-if="!loading">•</span>
            <span v-if="!loading">更新时间：{{ parseTime(detail.updateTime) || '-' }}</span>
          </div>
        </div>
      </div>

      <div class="header-right">
        <el-tag effect="plain" :type="publishStatusTagType(detail.publishStatus)" v-if="!loading">
          {{ publishStatusLabel(detail.publishStatus) }}
        </el-tag>
        <el-tag effect="plain" :type="detail.openSource === '1' ? 'success' : 'info'" v-if="!loading">
          {{ detail.openSource === '1' ? '开源' : '闭源' }}
        </el-tag>
        <el-button type="primary" icon="Edit" @click="goEdit" v-hasPermi="['tool:software:item:edit']">编辑</el-button>
      </div>
    </section>

    <el-row :gutter="16">
      <el-col :xs="24" :lg="9">
        <el-card shadow="never" class="info-card">
          <template #header>
            <div class="card-hd">
              <div class="hd-left">
                <el-avatar class="icon" shape="square" :size="44" :src="detail.iconUrl">
                  {{ (detail.softwareName || '').slice(0, 1) }}
                </el-avatar>
                <div class="hd-text">
                  <div class="hd-name">{{ detail.softwareName || '-' }}</div>
                  <div class="hd-meta">
                    <el-tag v-if="detail.categoryName" size="small" effect="plain">{{ detail.categoryName }}</el-tag>
                    <dict-tag v-if="detail.status" :options="sys_normal_disable" :value="detail.status" />
                  </div>
                </div>
              </div>
              <el-button text icon="Refresh" :loading="loading" @click="loadDetail">刷新</el-button>
            </div>
          </template>

          <div class="kv">
            <div class="kv-item">
              <span class="k">简短描述</span>
              <span class="v">{{ detail.shortDesc || '-' }}</span>
            </div>
            <div class="kv-item">
              <span class="k">许可证</span>
              <span class="v">{{ detail.license || '-' }}</span>
            </div>
            <div class="kv-item">
              <span class="k">作者/团队</span>
              <span class="v">{{ detail.author || detail.team || '-' }}</span>
            </div>
            <div class="kv-item">
              <span class="k">排序</span>
              <span class="v">{{ detail.softwareSort ?? '-' }}</span>
            </div>
          </div>

          <div class="tags" v-if="tagList.length">
            <el-tag v-for="t in tagList" :key="t" size="small" effect="plain">{{ t }}</el-tag>
          </div>
          <div class="tags muted" v-else>暂无标签</div>

          <div class="links" v-if="detail.officialUrl || detail.repoUrl">
            <el-link
              v-if="detail.officialUrl"
              :href="detail.officialUrl"
              target="_blank"
              rel="noopener noreferrer"
              underline="never"
            >
              官网
            </el-link>
            <el-link
              v-if="detail.repoUrl"
              :href="detail.repoUrl"
              target="_blank"
              rel="noopener noreferrer"
              underline="never"
            >
              仓库
            </el-link>
          </div>

          <el-divider content-position="left">数据质量</el-divider>
          <div class="quality">
            <el-tag v-for="q in qualityBadges" :key="q.key" :type="q.type" effect="plain" size="small">
              {{ q.label }}
            </el-tag>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="15">
        <el-card shadow="never" class="content-card">
          <template #header>
            <div class="card-hd">
              <span class="card-title">内容</span>
              <el-tag effect="plain" type="info" size="small">Markdown 预览</el-tag>
            </div>
          </template>

          <el-tabs v-model="activeTab" type="border-card" class="md-tabs">
            <el-tab-pane label="介绍" name="desc">
              <div class="md-wrap">
                <MarkdownRender :content="detail.descriptionMd || ''" />
              </div>
            </el-tab-pane>
            <el-tab-pane label="使用" name="usage">
              <div class="md-wrap">
                <MarkdownRender :content="detail.usageMd || ''" />
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-card>

        <el-row :gutter="16" class="tables">
          <el-col :xs="24" :lg="12">
            <el-card shadow="never" class="table-card">
              <template #header>
                <div class="card-hd">
                  <span class="card-title">下载配置</span>
                  <el-tag effect="plain" size="small" type="info">{{ (detail.downloads || []).length }} 条</el-tag>
                </div>
              </template>
              <el-table :data="detail.downloads || []" size="small" border>
                <el-table-column label="平台" prop="platform" width="120" />
                <el-table-column label="版本" prop="version" width="120" />
                <el-table-column label="下载地址" min-width="220">
                  <template #default="scope">
                    <el-link
                      v-if="scope.row.downloadUrl"
                      :href="scope.row.downloadUrl"
                      target="_blank"
                      rel="noopener noreferrer"
                      underline="never"
                    >
                      {{ scope.row.downloadUrl }}
                    </el-link>
                    <span v-else class="muted">-</span>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-col>

          <el-col :xs="24" :lg="12">
            <el-card shadow="never" class="table-card">
              <template #header>
                <div class="card-hd">
                  <span class="card-title">资源</span>
                  <el-tag effect="plain" size="small" type="info">{{ (detail.resources || []).length }} 条</el-tag>
                </div>
              </template>
              <el-table :data="detail.resources || []" size="small" border>
                <el-table-column label="类型" prop="resourceType" width="120" />
                <el-table-column label="标题" prop="title" width="140" show-overflow-tooltip />
                <el-table-column label="URL" min-width="220">
                  <template #default="scope">
                    <el-link
                      v-if="scope.row.resourceUrl"
                      :href="scope.row.resourceUrl"
                      target="_blank"
                      rel="noopener noreferrer"
                      underline="never"
                    >
                      {{ scope.row.resourceUrl }}
                    </el-link>
                    <span v-else class="muted">-</span>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script setup name="SoftwareItemDetail">
import { MarkdownRender } from 'markstream-vue'
import 'markstream-vue/index.css'

import { parseTime } from '@/utils/ruoyi'
import { getSoftwareItem } from '@/api/tool/software/item'

const { proxy } = getCurrentInstance()
const { sys_normal_disable } = proxy.useDict('sys_normal_disable')

const router = useRouter()
const route = useRoute()

const activeTab = ref('desc')
const loading = ref(false)

const detail = reactive({
  softwareId: undefined,
  softwareName: undefined,
  categoryId: undefined,
  categoryName: undefined,
  shortDesc: undefined,
  iconUrl: undefined,
  officialUrl: undefined,
  repoUrl: undefined,
  author: undefined,
  team: undefined,
  license: undefined,
  openSource: undefined,
  tags: undefined,
  descriptionMd: undefined,
  usageMd: undefined,
  publishStatus: undefined,
  softwareSort: undefined,
  status: undefined,
  updateTime: undefined,
  downloads: [],
  resources: []
})

const tagList = computed(() => splitTags(detail.tags || ''))

const qualityBadges = computed(() => {
  const checks = [
    { key: 'icon', label: '缺图标', missing: !String(detail.iconUrl || '').trim() },
    { key: 'license', label: '缺许可证', missing: !String(detail.license || '').trim() },
    { key: 'official', label: '缺官网', missing: !String(detail.officialUrl || '').trim() },
    { key: 'shortDesc', label: '缺简述', missing: !String(detail.shortDesc || '').trim() },
    { key: 'tags', label: '缺标签', missing: splitTags(detail.tags || '').length === 0 },
    { key: 'downloads', label: '缺下载', missing: !(detail.downloads || []).length },
    { key: 'resources', label: '缺资源', missing: !(detail.resources || []).length }
  ]
  return checks.map((x) => ({ ...x, type: x.missing ? 'warning' : 'success' }))
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
  if (value === '1') return '上架'
  if (value === '2') return '下架'
  return '草稿'
}

function publishStatusTagType(value) {
  if (value === '1') return 'success'
  if (value === '2') return 'warning'
  return 'info'
}

function goBack() {
  router.back()
}

function goEdit() {
  if (!detail.softwareId) return
  router.push({ path: '/software/edit', query: { softwareId: detail.softwareId } })
}

function loadDetail() {
  const softwareId = route.query?.softwareId
  if (!softwareId) return
  loading.value = true
  getSoftwareItem(softwareId)
    .then((res) => {
      const data = res.data || {}
      Object.assign(detail, data)
      if (!detail.downloads) detail.downloads = []
      if (!detail.resources) detail.resources = []
    })
    .catch(() => {})
    .finally(() => {
      loading.value = false
    })
}

watch(
  () => route.query?.softwareId,
  () => loadDetail(),
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
}

.card-hd {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.card-title {
  font-weight: 700;
}

.hd-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.hd-text {
  min-width: 0;
}

.hd-name {
  font-weight: 750;
  line-height: 20px;
  max-width: 260px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.hd-meta {
  margin-top: 6px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.kv {
  margin-top: 6px;
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
  color: var(--el-text-color-regular);
  text-align: right;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 260px;
}

.tags {
  margin-top: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.links {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.quality {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.muted {
  color: var(--el-text-color-secondary);
}

.tables {
  margin-top: 16px;
}

.md-wrap {
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 12px;
  padding: 10px 12px;
  min-height: 260px;
  max-height: 520px;
  overflow: auto;
  background: color-mix(in srgb, var(--app-surface) 86%, transparent);
}

.md-tabs :deep(.el-tabs__content) {
  padding: 12px;
}
</style>
