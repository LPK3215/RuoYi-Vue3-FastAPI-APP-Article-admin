<template>
  <el-drawer
    v-model="open"
    size="720px"
    append-to-body
    :destroy-on-close="false"
    class="software-filter-drawer"
  >
    <template #header>
      <div class="drawer-header">
        <div class="drawer-title">
          <span>选择软件</span>
          <el-tag effect="plain" type="info" size="small">筛选</el-tag>
        </div>
        <div class="drawer-actions">
          <el-button
            type="primary"
            plain
            icon="Plus"
            :disabled="!selectedRows.length"
            @click="emitPickSelected"
          >
            批量添加（{{ selectedRows.length }}）
          </el-button>
          <el-button text icon="Refresh" :loading="loading" @click="reloadFacets">刷新筛选项</el-button>
          <el-button type="primary" icon="Search" :loading="loading" @click="handleQuery">查询</el-button>
        </div>
      </div>
    </template>

    <div class="drawer-body">
      <el-form :model="query" label-width="86px" class="filter-form">
        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="关键词">
              <el-input
                v-model="query.keyword"
                placeholder="名称/描述/作者/团队/许可证/标签"
                clearable
                @keyup.enter="handleQuery"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="分类">
              <el-select v-model="query.categoryId" placeholder="全部" clearable filterable style="width: 100%">
                <el-option
                  v-for="c in categoryOptions"
                  :key="c.categoryId"
                  :label="c.categoryName"
                  :value="c.categoryId"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="标签">
              <el-select v-model="query.tag" placeholder="全部" clearable filterable style="width: 100%">
                <el-option v-for="t in facets.tags" :key="t.value" :label="t.value" :value="t.value" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="许可证">
              <el-select v-model="query.license" placeholder="全部" clearable filterable style="width: 100%">
                <el-option v-for="x in facets.licenses" :key="x.value" :label="x.value" :value="x.value" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="作者">
              <el-select v-model="query.author" placeholder="全部" clearable filterable style="width: 100%">
                <el-option v-for="x in facets.authors" :key="x.value" :label="x.value" :value="x.value" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="团队">
              <el-select v-model="query.team" placeholder="全部" clearable filterable style="width: 100%">
                <el-option v-for="x in facets.teams" :key="x.value" :label="x.value" :value="x.value" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="平台">
              <el-select v-model="query.platform" placeholder="全部" clearable filterable style="width: 100%">
                <el-option v-for="x in facets.platforms" :key="x.value" :label="x.value" :value="x.value" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="是否开源">
              <el-select v-model="query.openSource" placeholder="全部" clearable style="width: 100%">
                <el-option label="开源" value="1" />
                <el-option label="非开源" value="0" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="发布状态">
              <el-select v-model="query.publishStatus" placeholder="全部" clearable style="width: 100%">
                <el-option label="草稿" value="0" />
                <el-option label="上架" value="1" />
                <el-option label="下架" value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="仅上架">
              <el-switch v-model="onlyPublished" />
              <span class="muted" style="margin-left: 10px">开启后会强制筛选 publishStatus=1</span>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="12">
          <el-col :span="24">
            <el-form-item label="数据质量">
              <div class="quality-row">
                <el-checkbox v-model="quality.hasIcon">有图标</el-checkbox>
                <el-checkbox v-model="quality.hasLicense">有许可证</el-checkbox>
                <el-checkbox v-model="quality.hasOfficialUrl">有官网</el-checkbox>
                <el-checkbox v-model="quality.hasDownloads">有下载</el-checkbox>
                <el-checkbox v-model="quality.hasTags">有标签</el-checkbox>
              </div>
            </el-form-item>
          </el-col>
        </el-row>

        <div class="form-actions">
          <el-button icon="Refresh" @click="resetQuery">重置</el-button>
          <el-button type="primary" icon="Search" :loading="loading" @click="handleQuery">查询</el-button>
        </div>
      </el-form>

      <el-divider content-position="left">结果</el-divider>

      <el-table
        v-loading="loading"
        :data="rows"
        size="small"
        border
        height="520"
        @selection-change="onSelectionChange"
        row-key="softwareId"
      >
        <el-table-column type="selection" width="44" align="center" />
        <el-table-column label="软件" min-width="280">
          <template #default="scope">
            <div class="soft-cell">
              <el-avatar class="soft-icon" shape="square" :size="26" :src="scope.row.iconUrl">
                {{ (scope.row.softwareName || '').slice(0, 1) }}
              </el-avatar>
              <div class="soft-text">
                <div class="soft-name">{{ scope.row.softwareName || '-' }}</div>
                <div class="soft-meta">
                  <span>{{ scope.row.categoryName || '未分类' }}</span>
                  <span class="dot">•</span>
                  <span>ID：{{ scope.row.softwareId }}</span>
                </div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="发布" width="90" align="center">
          <template #default="scope">
            <el-tag effect="plain" :type="publishTagType(scope.row.publishStatus)">
              {{ publishLabel(scope.row.publishStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="更新时间" width="170" align="center">
          <template #default="scope">
            {{ parseTime(scope.row.updateTime) || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="190" align="center">
          <template #default="scope">
            <el-button link type="primary" icon="View" @click="emit('view', scope.row)">查看</el-button>
            <el-button link type="primary" icon="Plus" @click="emit('pick', scope.row)">添加</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pager">
        <pagination
          v-show="total > 0"
          :total="total"
          v-model:page="query.pageNum"
          v-model:limit="query.pageSize"
          @pagination="handleQuery"
        />
      </div>
    </div>
  </el-drawer>
</template>

<script setup>
import { listSoftwareCategoryOptions } from '@/api/tool/software/category'
import { getSoftwareItemFacets, listSoftwareItem } from '@/api/tool/software/item'
import { parseTime } from '@/utils/ruoyi'

const props = defineProps({
  modelValue: { type: Boolean, default: false }
})

const emit = defineEmits(['update:modelValue', 'pick', 'view'])

const open = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v)
})

const loading = ref(false)

const categoryOptions = ref([])
const facets = reactive({ tags: [], licenses: [], authors: [], teams: [], platforms: [] })

const onlyPublished = ref(true)
const quality = reactive({
  hasIcon: false,
  hasLicense: false,
  hasOfficialUrl: false,
  hasDownloads: false,
  hasTags: false
})

const query = reactive({
  pageNum: 1,
  pageSize: 10,
  keyword: undefined,
  categoryId: undefined,
  tag: undefined,
  license: undefined,
  author: undefined,
  team: undefined,
  platform: undefined,
  openSource: undefined,
  publishStatus: undefined
})

const rows = ref([])
const total = ref(0)
const selectedRows = ref([])

let queryTimer = 0

function queueQuery() {
  if (!open.value) return
  if (queryTimer) window.clearTimeout(queryTimer)
  queryTimer = window.setTimeout(() => {
    query.pageNum = 1
    handleQuery()
  }, 260)
}

function publishLabel(value) {
  if (value === '1') return '上架'
  if (value === '2') return '下架'
  return '草稿'
}

function publishTagType(value) {
  if (value === '1') return 'success'
  if (value === '2') return 'warning'
  return 'info'
}

function buildRequestParams() {
  const params = {
    pageNum: query.pageNum,
    pageSize: query.pageSize,
    keyword: query.keyword || undefined,
    categoryId: query.categoryId || undefined,
    tag: query.tag || undefined,
    license: query.license || undefined,
    author: query.author || undefined,
    team: query.team || undefined,
    platform: query.platform || undefined,
    openSource: query.openSource,
    publishStatus: onlyPublished.value ? '1' : query.publishStatus || undefined,
    hasIcon: quality.hasIcon ? '1' : undefined,
    hasLicense: quality.hasLicense ? '1' : undefined,
    hasOfficialUrl: quality.hasOfficialUrl ? '1' : undefined,
    hasDownloads: quality.hasDownloads ? '1' : undefined,
    hasTags: quality.hasTags ? '1' : undefined
  }
  return params
}

function onSelectionChange(list) {
  selectedRows.value = Array.isArray(list) ? list : []
}

function emitPickSelected() {
  const list = selectedRows.value || []
  for (const row of list) {
    emit('pick', row)
  }
  selectedRows.value = []
}

async function reloadFacets() {
  try {
    const res = await getSoftwareItemFacets({ limit: 80 })
    const data = res?.data || {}
    facets.tags = data.tags || []
    facets.licenses = data.licenses || []
    facets.authors = data.authors || []
    facets.teams = data.teams || []
    facets.platforms = data.platforms || []
  } catch (e) {
    // ignore
  }
}

async function ensureCategoryOptions() {
  if (categoryOptions.value.length) return
  try {
    const res = await listSoftwareCategoryOptions()
    categoryOptions.value = res?.data || []
  } catch (e) {
    categoryOptions.value = []
  }
}

function resetQuery() {
  query.pageNum = 1
  query.pageSize = 10
  query.keyword = undefined
  query.categoryId = undefined
  query.tag = undefined
  query.license = undefined
  query.author = undefined
  query.team = undefined
  query.platform = undefined
  query.openSource = undefined
  query.publishStatus = undefined
  quality.hasIcon = false
  quality.hasLicense = false
  quality.hasOfficialUrl = false
  quality.hasDownloads = false
  quality.hasTags = false
}

function handleQuery() {
  loading.value = true
  selectedRows.value = []
  listSoftwareItem(buildRequestParams())
    .then((res) => {
      rows.value = res?.rows || []
      total.value = Number(res?.total || 0)
    })
    .catch(() => {})
    .finally(() => {
      loading.value = false
    })
}

watch(
  () => open.value,
  async (v) => {
    if (!v) return
    await ensureCategoryOptions()
    if (!facets.tags.length && !facets.licenses.length && !facets.authors.length && !facets.teams.length && !facets.platforms.length) {
      await reloadFacets()
    }
    handleQuery()
  }
)

watch(
  () => [query.keyword, query.categoryId, query.tag, query.license, query.author, query.team, query.platform, query.openSource, query.publishStatus],
  () => {
    queueQuery()
  }
)

watch(
  () => [quality.hasIcon, quality.hasLicense, quality.hasOfficialUrl, quality.hasDownloads, quality.hasTags, onlyPublished.value],
  () => {
    queueQuery()
  }
)

watch(
  () => onlyPublished.value,
  () => {
    query.pageNum = 1
    if (open.value) handleQuery()
  }
)

watch(
  () => open.value,
  (v) => {
    if (!v) selectedRows.value = []
  }
)
</script>

<style scoped>
.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  width: 100%;
}

.drawer-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 800;
}

.drawer-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.drawer-body {
  padding: 0 4px;
}

.filter-form {
  padding: 10px 8px 0;
  border-radius: 12px;
  border: 1px solid var(--el-border-color);
  background: color-mix(in srgb, var(--app-surface) 86%, transparent);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 0 10px 10px;
}

.quality-row {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}

.muted {
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

.soft-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.soft-text {
  min-width: 0;
}

.soft-name {
  font-weight: 750;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 360px;
}

.soft-meta {
  margin-top: 2px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.dot {
  opacity: 0.7;
}

.pager {
  margin-top: 10px;
}
</style>





