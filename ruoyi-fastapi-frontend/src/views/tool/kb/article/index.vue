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
        <el-input
          v-model="queryParams.tag"
          placeholder="单个标签"
          clearable
          style="width: 200px"
          @keyup.enter="handleQuery"
        />
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
          :disabled="single"
          @click="handleEdit"
          v-hasPermi="['tool:kb:article:edit']"
        >
          编辑
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-dropdown @command="handleBatchPublishCommand" v-hasPermi="['tool:kb:article:publish']">
          <el-button type="warning" plain icon="Promotion" :disabled="multiple">
            发布状态
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
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
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['tool:kb:article:remove']"
        >
          删除
        </el-button>
      </el-col>
      <div class="toolbar-right">
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
        </div>
      </template>

      <el-table ref="tableRef" v-loading="loading" :data="articleList" @selection-change="handleSelectionChange">
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
import { parseTime } from '@/utils/ruoyi'

const { proxy } = getCurrentInstance()
const { sys_normal_disable } = proxy.useDict('sys_normal_disable')
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

const publishStatusOptions = [
  { label: '草稿', value: '0' },
  { label: '发布', value: '1' },
  { label: '下线', value: '2' }
]

const queryParams = ref({
  pageNum: 1,
  pageSize: 10,
  keyword: undefined,
  categoryId: undefined,
  tag: undefined,
  publishStatus: undefined,
  status: undefined
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

getList()
listKbCategoryOptions()
  .then((res) => {
    categoryOptions.value = res.data || []
  })
  .catch(() => {})
</script>

<style scoped>
.kb-list-card {
  border-radius: 16px;
  border: 1px solid var(--app-border);
  background: color-mix(in srgb, var(--app-surface) 92%, transparent);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 800;
}

.count-tag {
  font-weight: 650;
}

.kb-toolbar {
  align-items: center;
}

.toolbar-right {
  margin-left: auto;
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

.muted {
  color: var(--el-text-color-secondary);
}
</style>
