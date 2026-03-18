<template>
  <div class="app-container kb-article">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="关键字" prop="keyword">
        <el-input
          v-model="queryParams.keyword"
          placeholder="标题/摘要"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="分类" prop="categoryId">
        <el-select v-model="queryParams.categoryId" placeholder="全部" clearable filterable style="width: 200px">
          <el-option v-for="c in categoryOptions" :key="c.categoryId" :label="c.categoryName" :value="c.categoryId" />
        </el-select>
      </el-form-item>
      <el-form-item label="标签" prop="tag">
        <el-select
          v-model="queryParams.tag"
          placeholder="选择/输入标签"
          clearable
          filterable
          allow-create
          default-first-option
          style="width: 200px"
        >
          <el-option v-for="t in tagOptions" :key="t.tagId" :label="t.tagName" :value="t.tagName" />
        </el-select>
      </el-form-item>
      <el-form-item label="类型" prop="articleType">
        <el-select v-model="queryParams.articleType" placeholder="全部" clearable filterable style="width: 180px">
          <el-option v-for="d in kb_article_type" :key="d.value" :label="d.label" :value="d.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="发布" prop="publishStatus">
        <el-select v-model="queryParams.publishStatus" placeholder="全部" clearable style="width: 160px">
          <el-option v-for="o in publishStatusOptions" :key="o.value" :label="o.label" :value="o.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="全部" clearable style="width: 160px">
          <el-option v-for="dict in sys_normal_disable" :key="dict.value" :label="dict.label" :value="dict.value" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8 kb-toolbar">
      <el-col :span="1.5">
        <el-button type="primary" plain icon="Plus" @click="handleAdd" v-hasPermi="['tool:kb:article:add']">
          新增
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single || viewMode !== 'table'"
          @click="handleEdit"
          v-hasPermi="['tool:kb:article:edit']"
        >
          编辑
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-dropdown
          :disabled="multiple || viewMode !== 'table'"
          @command="handleBatchPublishCommand"
          v-hasPermi="['tool:kb:article:publish']"
        >
          <el-button type="warning" plain icon="Promotion" :disabled="multiple || viewMode !== 'table'">
            发布状态
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="1">发布</el-dropdown-item>
              <el-dropdown-item command="2">下线</el-dropdown-item>
              <el-dropdown-item command="0" divided>设为草稿</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple || viewMode !== 'table'"
          @click="handleDelete"
          v-hasPermi="['tool:kb:article:remove']"
        >
          删除
        </el-button>
      </el-col>
      <div class="toolbar-right">
        <el-radio-group v-model="viewMode" class="view-toggle">
          <el-radio-button value="table">
            <el-icon><List /></el-icon>
            列表
          </el-radio-button>
          <el-radio-button value="card">
            <el-icon><Grid /></el-icon>
            卡片
          </el-radio-button>
        </el-radio-group>

        <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
      </div>
    </el-row>

    <el-card shadow="never" class="kb-list-card">
      <template #header>
        <div class="card-header">
          <div class="title">
            <span>教程文章</span>
            <el-tag type="info" effect="plain" class="count-tag">{{ total }} 条</el-tag>
          </div>
          <div class="actions">
            <el-button v-if="viewMode === 'card'" icon="Refresh" @click="getList">刷新</el-button>
          </div>
        </div>
      </template>

      <el-table
        v-if="viewMode === 'table'"
        ref="tableRef"
        v-loading="loading"
        :data="articleList"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column label="ID" align="center" prop="articleId" width="90" />
        <el-table-column label="分类" align="center" prop="categoryName" width="140" show-overflow-tooltip>
          <template #default="scope">
            <span>{{ scope.row.categoryName || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="标题" prop="title" min-width="240" show-overflow-tooltip>
          <template #default="scope">
            <div class="title-cell">
              <div class="title-main">
                {{ scope.row.title || '-' }}
              </div>
              <div class="title-sub" v-if="scope.row.summary">
                {{ scope.row.summary }}
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="标签" prop="tags" min-width="220">
          <template #default="scope">
            <div class="tag-wrap" v-if="splitTags(scope.row.tags).length">
              <el-tag v-for="t in splitTags(scope.row.tags).slice(0, 3)" :key="t" size="small" effect="plain">
                {{ t }}
              </el-tag>
              <el-tag v-if="splitTags(scope.row.tags).length > 3" size="small" effect="plain" type="info">
                +{{ splitTags(scope.row.tags).length - 3 }}
              </el-tag>
            </div>
            <span v-else class="muted">-</span>
          </template>
        </el-table-column>
        <el-table-column label="发布" prop="publishStatus" width="100" align="center">
          <template #default="scope">
            <el-tag effect="plain" :type="publishStatusTagType(scope.row.publishStatus)">
              {{ publishStatusLabel(scope.row.publishStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="排序" align="center" prop="articleSort" width="90" />
        <el-table-column label="状态" align="center" prop="status" width="90">
          <template #default="scope">
            <dict-tag :options="sys_normal_disable" :value="scope.row.status" />
          </template>
        </el-table-column>
        <el-table-column label="发布时间" align="center" prop="publishTime" width="180">
          <template #default="scope">
            <span>{{ parseTime(scope.row.publishTime) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="更新时间" align="center" prop="updateTime" width="180">
          <template #default="scope">
            <span>{{ parseTime(scope.row.updateTime) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="300" align="center" class-name="small-padding fixed-width">
          <template #default="scope">
            <el-button
              link
              type="primary"
              icon="View"
              @click="handleDetail(scope.row)"
              v-hasPermi="['tool:kb:article:query']"
            >
              详情
            </el-button>
            <el-button
              link
              type="primary"
              icon="Edit"
              @click="handleEdit(scope.row)"
              v-hasPermi="['tool:kb:article:edit']"
            >
              编辑
            </el-button>
            <el-dropdown
              v-hasPermi="['tool:kb:article:publish']"
              @command="(cmd) => handlePublishCommand(cmd, scope.row)"
            >
              <el-button link type="primary" icon="Promotion">发布</el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="1">发布</el-dropdown-item>
                  <el-dropdown-item command="2">下线</el-dropdown-item>
                  <el-dropdown-item command="0">草稿</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            <el-button
              link
              type="primary"
              icon="Delete"
              @click="handleDelete(scope.row)"
              v-hasPermi="['tool:kb:article:remove']"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-else v-loading="loading" class="card-view">
        <el-empty v-if="!articleList.length" description="暂无数据" />
        <div v-else class="card-grid">
          <el-card
            v-for="item in articleList"
            :key="item.articleId"
            class="article-card"
            :style="articleCardStyle(item)"
            shadow="hover"
            role="button"
            tabindex="0"
            @click="handleDetail(item)"
            @keydown.enter.prevent="handleDetail(item)"
            @keydown.space.prevent="handleDetail(item)"
          >
            <template #header>
              <div class="article-card-cover">
                <img
                  v-if="item.coverUrl"
                  :src="item.coverUrl"
                  :alt="item.title || '教程封面'"
                  referrerpolicy="no-referrer"
                />
                <div v-else class="article-card-cover__placeholder">
                  <div class="article-card-cover__glyph">{{ articleGlyph(item.title) }}</div>
                  <div class="article-card-cover__hint">
                    <span>{{ item.categoryName || '教程文章' }}</span>
                    <strong>{{ articleCoverLabel(item) }}</strong>
                  </div>
                </div>
                <div class="article-card-cover__veil"></div>
                <div class="article-card-cover__chips">
                  <el-tag v-if="item.categoryName" size="small" effect="dark">{{ item.categoryName }}</el-tag>
                  <el-tag v-if="item.articleType" size="small" type="warning" effect="dark">
                    {{ articleTypeLabel(item.articleType) }}
                  </el-tag>
                </div>
              </div>
            </template>

            <div class="article-card-shell">
              <div class="article-card-header">
                <div class="heading">
                  <div class="eyebrow">
                    <span>#{{ item.articleId || '-' }}</span>
                    <span>{{ articleTimeHint(item) }}</span>
                  </div>
                  <div class="name" :title="item.title">{{ item.title || '-' }}</div>
                </div>
                <div class="status-stack">
                  <dict-tag :options="sys_normal_disable" :value="item.status" />
                  <el-tag size="small" :type="publishStatusTagType(item.publishStatus)" effect="plain">
                    {{ publishStatusLabel(item.publishStatus) }}
                  </el-tag>
                </div>
              </div>

              <div class="article-card-body">
                <div class="summary">
                  <span v-if="item.summary">{{ item.summary }}</span>
                  <span v-else class="muted">暂无摘要</span>
                </div>

                <div v-if="splitTags(item.tags).length" class="tag-list">
                  <el-tag v-for="tag in splitTags(item.tags).slice(0, 5)" :key="tag" size="small" effect="plain">
                    {{ tag }}
                  </el-tag>
                  <el-tag v-if="splitTags(item.tags).length > 5" size="small" type="info" effect="plain">
                    +{{ splitTags(item.tags).length - 5 }}
                  </el-tag>
                </div>

                <div class="article-card-insights">
                  <div class="insight-pill">
                    <span class="label">排序</span>
                    <strong>{{ item.articleSort ?? '-' }}</strong>
                  </div>
                  <div class="insight-pill">
                    <span class="label">标签</span>
                    <strong>{{ splitTags(item.tags).length || 0 }}</strong>
                  </div>
                  <div class="insight-pill">
                    <span class="label">封面</span>
                    <strong>{{ item.coverUrl ? '已配' : '待补' }}</strong>
                  </div>
                </div>

                <div class="article-card-times">
                  <div class="time-item">
                    <span class="k">发布时间</span>
                    <span class="v">{{ formatCardTime(item.publishTime) }}</span>
                  </div>
                  <div class="time-item">
                    <span class="k">更新时间</span>
                    <span class="v">{{ formatCardTime(item.updateTime) }}</span>
                  </div>
                </div>
              </div>

              <div class="article-card-actions">
                <el-button
                  link
                  type="primary"
                  icon="View"
                  @click.stop="handleDetail(item)"
                  v-hasPermi="['tool:kb:article:query']"
                >
                  详情
                </el-button>
                <el-button
                  link
                  type="primary"
                  icon="Edit"
                  @click.stop="handleEdit(item)"
                  v-hasPermi="['tool:kb:article:edit']"
                >
                  编辑
                </el-button>
                <el-dropdown
                  v-hasPermi="['tool:kb:article:publish']"
                  @command="(cmd) => handlePublishCommand(cmd, item)"
                >
                  <el-button link type="primary" icon="Promotion" @click.stop>发布</el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="1">发布</el-dropdown-item>
                      <el-dropdown-item command="2">下线</el-dropdown-item>
                      <el-dropdown-item command="0">草稿</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
                <el-button
                  link
                  type="danger"
                  icon="Delete"
                  @click.stop="handleDelete(item)"
                  v-hasPermi="['tool:kb:article:remove']"
                >
                  删除
                </el-button>
              </div>
            </div>
          </el-card>
        </div>
      </div>

      <pagination
        v-show="total > 0"
        :total="total"
        v-model:page="queryParams.pageNum"
        v-model:limit="queryParams.pageSize"
        @pagination="getList"
      />
    </el-card>
  </div>
</template>

<script setup name="KbArticleIndex">
import { changeKbArticlePublishStatus, delKbArticle, listKbArticle } from '@/api/tool/kb/article'
import { listKbCategoryOptions } from '@/api/tool/kb/category'
import { listKbTagOptions } from '@/api/tool/kb/tag'
import { cardToneVars, firstCardGlyph } from '@/utils/cardTheme'
import { parseTime } from '@/utils/ruoyi'

const { proxy } = getCurrentInstance()
const { sys_normal_disable, kb_article_type } = proxy.useDict('sys_normal_disable', 'kb_article_type')
const router = useRouter()

const showSearch = ref(true)
const loading = ref(true)
const tableRef = ref()

const articleList = ref([])
const total = ref(0)
const ids = ref([])
const single = ref(true)
const multiple = ref(true)
const categoryOptions = ref([])
const tagOptions = ref([])
const viewModeStorageKey = 'tool:kb:article:viewMode'
const viewMode = ref('table')

const publishStatusOptions = [
  { label: '草稿', value: '0' },
  { label: '发布', value: '1' },
  { label: '下线', value: '2' }
]

const articleCardTones = [
  { accent: '#2f6fed', surface: '#d8e6ff', contrast: '#143a88' },
  { accent: '#1f8a70', surface: '#d8f3ec', contrast: '#0f4e40' },
  { accent: '#c27712', surface: '#f8e2be', contrast: '#7a4700' },
  { accent: '#9f3f7f', surface: '#f4d9ea', contrast: '#5f2149' },
  { accent: '#2c6fbb', surface: '#d9ebff', contrast: '#143f71' }
]

const queryParams = ref({
  pageNum: 1,
  pageSize: 10,
  keyword: undefined,
  categoryId: undefined,
  tag: undefined,
  articleType: undefined,
  publishStatus: undefined,
  status: undefined
})

function loadViewMode() {
  try {
    const cached = localStorage.getItem(viewModeStorageKey)
    viewMode.value = cached === 'card' ? 'card' : 'table'
  } catch (e) {
    viewMode.value = 'table'
  }
}

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
  const normalized = String(value ?? '')
  if (normalized === '1') return '发布'
  if (normalized === '2') return '下线'
  return '草稿'
}

function publishStatusTagType(value) {
  const normalized = String(value ?? '')
  if (normalized === '1') return 'success'
  if (normalized === '2') return 'warning'
  return 'info'
}

function articleTypeLabel(value) {
  return proxy.selectDictLabel(kb_article_type.value || [], String(value ?? '')) || '-'
}

function articleCardStyle(item) {
  return cardToneVars([item?.title, item?.categoryName, item?.articleType].filter(Boolean).join('|'), articleCardTones, 'article')
}

function articleGlyph(title) {
  return firstCardGlyph(title, '教')
}

function articleCoverLabel(item) {
  const label = articleTypeLabel(item?.articleType)
  return label !== '-' ? label : '内容封面'
}

function formatCardTime(value) {
  return parseTime(value) || '未记录'
}

function articleTimeHint(item) {
  if (item?.updateTime) return `更新 ${formatCardTime(item.updateTime)}`
  if (item?.publishTime) return `发布 ${formatCardTime(item.publishTime)}`
  return '待补时间信息'
}

function clearSelection() {
  ids.value = []
  single.value = true
  multiple.value = true
  nextTick(() => {
    try {
      tableRef.value?.clearSelection?.()
    } catch (e) {}
  })
}

watch(
  () => viewMode.value,
  (val) => {
    try {
      localStorage.setItem(viewModeStorageKey, val)
    } catch (e) {}
    clearSelection()
  }
)

function getList() {
  loading.value = true
  listKbArticle(queryParams.value)
    .then((response) => {
      articleList.value = response.rows || []
      total.value = response.total || 0
    })
    .finally(() => {
      loading.value = false
    })
}

function handleQuery() {
  queryParams.value.pageNum = 1
  getList()
}

function resetQuery() {
  proxy.resetForm('queryRef')
  handleQuery()
}

function handleSelectionChange(selection) {
  ids.value = selection.map((item) => String(item.articleId))
  single.value = selection.length !== 1
  multiple.value = !selection.length
}

function handleAdd() {
  router.push({ path: '/kb/article/edit' })
}

function handleEdit(row) {
  const articleId = row?.articleId || ids.value[0]
  if (!articleId) return
  router.push({ path: '/kb/article/edit', query: { articleId } })
}

function handleDetail(row) {
  const articleId = row?.articleId || ids.value[0]
  if (!articleId) return
  router.push({ path: '/kb/article/detail', query: { articleId } })
}

function handleDelete(row) {
  const articleIds = row?.articleId || ids.value.join(',')
  if (!articleIds) return
  proxy.$modal
    .confirm('是否确认删除教程文章编号为 "' + articleIds + '" 的数据项？')
    .then(() => delKbArticle(articleIds))
    .then(() => {
      proxy.$modal.msgSuccess('删除成功')
      clearSelection()
      getList()
    })
    .catch(() => {})
}

function handlePublishCommand(publishStatus, row) {
  const articleId = row?.articleId
  if (!articleId) return
  const label = publishStatus === '1' ? '发布' : publishStatus === '2' ? '下线' : '草稿'
  proxy.$modal
    .confirm(`是否确认将文章「${row.title || articleId}」设置为「${label}」？`)
    .then(() => changeKbArticlePublishStatus({ articleId, publishStatus }))
    .then(() => {
      proxy.$modal.msgSuccess('操作成功')
      getList()
    })
    .catch(() => {})
}

function handleBatchPublishCommand(command) {
  if (!ids.value?.length) return
  const label = command === '1' ? '发布' : command === '2' ? '下线' : '草稿'
  proxy.$modal
    .confirm(`是否确认将选中的 ${ids.value.length} 篇文章设置为「${label}」？`)
    .then(async () => {
      await Promise.all(ids.value.map((id) => changeKbArticlePublishStatus({ articleId: Number(id), publishStatus: command })))
    })
    .then(() => {
      proxy.$modal.msgSuccess('操作成功')
      clearSelection()
      getList()
    })
    .catch(() => {})
}

loadViewMode()
getList()
listKbCategoryOptions()
  .then((res) => {
    categoryOptions.value = res.data || []
  })
  .catch(() => {})

listKbTagOptions()
  .then((res) => {
    tagOptions.value = res.data || []
  })
  .catch(() => {})
</script>

<style scoped>
.kb-list-card {
  border-radius: 16px;
  border: 1px solid var(--app-border);
  background: color-mix(in srgb, var(--app-surface) 92%, transparent);
}

.kb-list-card :deep(.el-card__body) {
  padding-top: 8px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.title {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}

.count-tag {
  font-weight: 650;
}

.actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.kb-toolbar {
  align-items: center;
}

.toolbar-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
}

.toolbar-right :deep(.top-right-btn) {
  margin-left: 0;
}

.view-toggle :deep(.el-radio-button__inner) {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.card-view {
  min-height: 240px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 14px;
}

.article-card {
  cursor: pointer;
  overflow: hidden;
  border: 1px solid color-mix(in srgb, var(--article-accent) 16%, var(--app-border));
  background: linear-gradient(180deg, color-mix(in srgb, var(--article-surface) 14%, #fff) 0%, #fff 38%);
  transition: box-shadow 200ms ease, transform 200ms ease, border-color 200ms ease;
}

.article-card :deep(.el-card__header) {
  padding: 0;
  border-bottom: none;
}

.article-card :deep(.el-card__body) {
  padding: 14px 16px 16px;
}

.article-card:hover {
  transform: translateY(-2px);
  border-color: color-mix(in srgb, var(--article-accent) 42%, var(--app-border));
}

.article-card:focus {
  outline: 2px solid var(--el-color-primary);
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  .article-card {
    transition: none;
  }

  .article-card:hover {
    transform: none;
  }
}

.article-card-cover {
  position: relative;
  aspect-ratio: 16 / 8.8;
  overflow: hidden;
  background: linear-gradient(135deg, var(--article-accent) 0%, var(--article-contrast) 100%);
}

.article-card-cover img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.article-card-cover__placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 12px;
  padding: 18px 18px 16px;
  color: #fff;
  background:
    radial-gradient(circle at top right, color-mix(in srgb, var(--article-surface) 44%, transparent) 0%, transparent 34%),
    linear-gradient(155deg, color-mix(in srgb, var(--article-accent) 88%, #fff) 0%, var(--article-contrast) 100%);
}

.article-card-cover__glyph {
  font-size: 44px;
  line-height: 1;
  font-weight: 800;
  letter-spacing: -0.04em;
}

.article-card-cover__hint {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-width: 80%;
}

.article-card-cover__hint span {
  font-size: 12px;
  letter-spacing: 0.08em;
  opacity: 0.84;
}

.article-card-cover__hint strong {
  font-size: 16px;
  line-height: 1.35;
  font-weight: 700;
}

.article-card-cover__veil {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.06) 0%, rgba(15, 23, 42, 0.34) 100%);
  pointer-events: none;
}

.article-card-cover__chips {
  position: absolute;
  inset: 14px 14px auto 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.article-card-shell {
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-height: 308px;
}

.article-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.article-card-header .heading {
  min-width: 0;
}

.article-card-header .eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 8px;
  color: var(--el-text-color-secondary);
  font-size: 12px;
  line-height: 1.4;
}

.article-card-header .name {
  font-size: 17px;
  font-weight: 700;
  line-height: 1.45;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.status-stack {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
  flex-shrink: 0;
}

.article-card-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.summary {
  color: var(--el-text-color-regular);
  line-height: 20px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 58px;
}

.title-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.title-main {
  font-weight: 750;
}

.title-sub {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  line-height: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.tag-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.article-card-insights {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
}

.insight-pill {
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid color-mix(in srgb, var(--article-accent) 16%, var(--app-border));
  background: color-mix(in srgb, var(--article-surface) 52%, var(--app-surface));
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.insight-pill .label {
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

.insight-pill strong {
  color: var(--el-text-color-primary);
  font-size: 14px;
  font-weight: 700;
}

.article-card-times {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}

.time-item {
  padding: 10px 12px;
  border-radius: 12px;
  background: color-mix(in srgb, var(--app-surface) 88%, transparent);
  border: 1px solid var(--el-border-color-lighter);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.time-item .k {
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

.time-item .v {
  color: var(--el-text-color-regular);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 600;
}

.article-card-actions {
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid var(--el-border-color-lighter);
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.muted {
  color: var(--el-text-color-secondary);
}

@media (max-width: 991px) {
  .card-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
}

@media (max-width: 768px) {
  .toolbar-right {
    width: 100%;
    justify-content: space-between;
    flex-wrap: wrap;
  }

  .card-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .article-card :deep(.el-card__body) {
    padding: 12px;
  }

  .article-card-cover {
    aspect-ratio: 16 / 9.5;
  }

  .article-card-shell {
    min-height: auto;
    gap: 12px;
  }

  .article-card-header {
    flex-direction: column;
    align-items: stretch;
  }

  .status-stack {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }

  .article-card-insights,
  .article-card-times {
    grid-template-columns: 1fr;
  }

  .article-card-actions {
    justify-content: space-between;
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .article-card-cover__placeholder {
    padding: 16px 16px 14px;
  }

  .article-card-cover__hint {
    max-width: 100%;
  }

  .article-card-cover__glyph {
    font-size: 40px;
  }

  .article-card-insights {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
