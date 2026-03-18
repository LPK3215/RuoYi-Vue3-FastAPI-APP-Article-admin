<template>
  <div class="app-container kb-category">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="分类名称" prop="categoryName">
        <el-input
          v-model="queryParams.categoryName"
          placeholder="请输入分类名称"
          clearable
          style="width: 220px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="分类状态" clearable style="width: 180px">
          <el-option v-for="dict in sys_normal_disable" :key="dict.value" :label="dict.label" :value="dict.value" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8 category-toolbar">
      <el-col :span="1.5">
        <el-button type="primary" plain icon="Plus" @click="handleAdd" v-hasPermi="['tool:kb:category:add']">
          新增
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['tool:kb:category:edit']"
        >
          修改
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['tool:kb:category:remove']"
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

    <el-card shadow="never" class="category-list-card">
      <template #header>
        <div class="card-header">
          <div class="title">
            <span>教程分类</span>
            <el-tag type="info" effect="plain" class="count-tag">{{ total }} 条</el-tag>
          </div>
        </div>
      </template>

      <el-table
        v-if="viewMode === 'table'"
        ref="tableRef"
        v-loading="loading"
        :data="categoryList"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column label="ID" align="center" prop="categoryId" width="90" />
        <el-table-column label="编码" align="center" prop="categoryCode" width="160" />
        <el-table-column label="名称" align="center" prop="categoryName" min-width="220" show-overflow-tooltip />
        <el-table-column label="排序" align="center" prop="categorySort" width="90" />
        <el-table-column label="状态" align="center" prop="status" width="90">
          <template #default="scope">
            <dict-tag :options="sys_normal_disable" :value="scope.row.status" />
          </template>
        </el-table-column>
        <el-table-column label="创建时间" align="center" prop="createTime" width="180">
          <template #default="scope">
            <span>{{ parseTime(scope.row.createTime) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center" class-name="small-padding fixed-width">
          <template #default="scope">
            <el-button
              link
              type="primary"
              icon="Edit"
              @click="handleUpdate(scope.row)"
              v-hasPermi="['tool:kb:category:edit']"
            >
              修改
            </el-button>
            <el-button
              link
              type="primary"
              icon="Delete"
              @click="handleDelete(scope.row)"
              v-hasPermi="['tool:kb:category:remove']"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-else v-loading="loading" class="card-view">
        <el-empty v-if="!categoryList.length" description="暂无数据" />
        <div v-else class="card-grid">
          <el-card
            v-for="item in categoryList"
            :key="item.categoryId"
            class="category-card"
            :class="{ 'is-selected': isSelected(item.categoryId) }"
            :style="categoryCardStyle(item)"
            shadow="hover"
            role="button"
            tabindex="0"
            @click="toggleSelection(item.categoryId)"
            @keydown.enter.prevent="toggleSelection(item.categoryId)"
            @keydown.space.prevent="toggleSelection(item.categoryId)"
          >
            <template #header>
              <div class="category-card-header">
                <div class="left">
                  <el-checkbox
                    :model-value="isSelected(item.categoryId)"
                    @click.stop
                    @change="toggleSelection(item.categoryId)"
                  />
                  <el-avatar class="category-avatar" shape="square" :size="42">
                    {{ categoryGlyph(item.categoryName) }}
                  </el-avatar>
                  <div class="heading">
                    <div class="name" :title="item.categoryName">{{ item.categoryName || '-' }}</div>
                    <div class="meta">
                      <span class="meta-chip">{{ item.categoryCode || '未设编码' }}</span>
                      <span class="meta-chip">排序 {{ item.categorySort ?? 0 }}</span>
                    </div>
                  </div>
                </div>
                <dict-tag :options="sys_normal_disable" :value="item.status" />
              </div>
            </template>

            <div class="category-card-body">
              <div class="category-card-facts">
                <div class="fact">
                  <span class="label">分类ID</span>
                  <strong>#{{ item.categoryId || '-' }}</strong>
                </div>
                <div class="fact">
                  <span class="label">创建时间</span>
                  <strong>{{ formatCardTime(item.createTime) }}</strong>
                </div>
              </div>

              <div class="remark">
                <span v-if="item.remark">{{ item.remark }}</span>
                <span v-else class="muted">暂无备注</span>
              </div>
            </div>

            <div class="category-card-actions">
              <el-button
                link
                type="primary"
                icon="Edit"
                @click.stop="handleUpdate(item)"
                v-hasPermi="['tool:kb:category:edit']"
              >
                修改
              </el-button>
              <el-button
                link
                type="danger"
                icon="Delete"
                @click.stop="handleDelete(item)"
                v-hasPermi="['tool:kb:category:remove']"
              >
                删除
              </el-button>
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

    <el-dialog :title="title" v-model="open" width="520px" append-to-body>
      <el-form ref="categoryRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="分类名称" prop="categoryName">
          <el-input v-model="form.categoryName" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="分类编码" prop="categoryCode">
          <el-input v-model="form.categoryCode" placeholder="可选：用于快速识别" />
        </el-form-item>
        <el-form-item label="排序" prop="categorySort">
          <el-input-number v-model="form.categorySort" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio v-for="dict in sys_normal_disable" :key="dict.value" :value="dict.value">
              {{ dict.label }}
            </el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="KbCategory">
import { addKbCategory, delKbCategory, getKbCategory, listKbCategory, updateKbCategory } from '@/api/tool/kb/category'
import { cardToneVars, firstCardGlyph } from '@/utils/cardTheme'
import { parseTime } from '@/utils/ruoyi'

const { proxy } = getCurrentInstance()
const { sys_normal_disable } = proxy.useDict('sys_normal_disable')

const categoryList = ref([])
const open = ref(false)
const loading = ref(true)
const showSearch = ref(true)
const tableRef = ref()
const ids = ref([])
const single = ref(true)
const multiple = ref(true)
const total = ref(0)
const title = ref('')
const viewModeStorageKey = 'tool:kb:category:viewMode'
const viewMode = ref('table')

const categoryCardTones = [
  { accent: '#2f6fed', surface: '#dce8ff', contrast: '#173d84' },
  { accent: '#1f8a70', surface: '#d8f3ec', contrast: '#145445' },
  { accent: '#b85c38', surface: '#f5ddcf', contrast: '#7b341b' },
  { accent: '#7f56d9', surface: '#eadfff', contrast: '#4e2e8e' },
  { accent: '#0f766e', surface: '#d5f2ee', contrast: '#114f4a' }
]

const queryParams = ref({
  pageNum: 1,
  pageSize: 10,
  categoryName: undefined,
  status: undefined
})

const form = reactive({
  categoryId: undefined,
  parentId: 0,
  categoryCode: undefined,
  categoryName: undefined,
  categorySort: 0,
  status: '0',
  remark: undefined
})

const rules = {
  categoryName: [{ required: true, message: '分类名称不能为空', trigger: 'blur' }],
  categorySort: [{ required: true, message: '排序不能为空', trigger: 'blur' }]
}

function loadViewMode() {
  try {
    const cached = localStorage.getItem(viewModeStorageKey)
    viewMode.value = cached === 'card' ? 'card' : 'table'
  } catch (e) {
    viewMode.value = 'table'
  }
}

function categoryCardStyle(item) {
  return cardToneVars([item?.categoryName, item?.categoryCode].filter(Boolean).join('|'), categoryCardTones, 'category')
}

function categoryGlyph(name) {
  return firstCardGlyph(name, '分')
}

function formatCardTime(value) {
  return parseTime(value) || '未记录'
}

function reset() {
  form.categoryId = undefined
  form.parentId = 0
  form.categoryCode = undefined
  form.categoryName = undefined
  form.categorySort = 0
  form.status = '0'
  form.remark = undefined
  proxy.resetForm('categoryRef')
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

function isSelected(categoryId) {
  return ids.value.includes(String(categoryId))
}

function toggleSelection(categoryId) {
  const id = String(categoryId)
  if (!id) return
  const next = ids.value.includes(id) ? ids.value.filter((item) => item !== id) : [...ids.value, id]
  ids.value = next
  single.value = next.length !== 1
  multiple.value = !next.length
}

function getList() {
  loading.value = true
  listKbCategory(queryParams.value)
    .then((response) => {
      categoryList.value = response.rows || []
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
  ids.value = selection.map((item) => String(item.categoryId))
  single.value = selection.length !== 1
  multiple.value = !selection.length
}

function handleAdd() {
  reset()
  open.value = true
  title.value = '新增分类'
}

function handleUpdate(row) {
  reset()
  const categoryId = row?.categoryId || ids.value[0]
  if (!categoryId) return
  getKbCategory(categoryId).then((response) => {
    Object.assign(form, response.data || {})
    open.value = true
    title.value = '修改分类'
  })
}

function submitForm() {
  proxy.$refs['categoryRef'].validate((valid) => {
    if (!valid) return
    const request = form.categoryId ? updateKbCategory : addKbCategory
    request({ ...form })
      .then((response) => {
        proxy.$modal.msgSuccess(response.msg || '操作成功')
        open.value = false
        getList()
      })
      .catch(() => {})
  })
}

function handleDelete(row) {
  const categoryIds = row?.categoryId || ids.value.join(',')
  if (!categoryIds) return
  proxy.$modal
    .confirm('是否确认删除分类编号为 "' + categoryIds + '" 的数据项？')
    .then(() => delKbCategory(categoryIds))
    .then(() => {
      proxy.$modal.msgSuccess('删除成功')
      clearSelection()
      getList()
    })
    .catch(() => {})
}

function cancel() {
  open.value = false
  reset()
}

loadViewMode()
getList()
</script>

<style scoped>
.category-list-card {
  border-radius: 16px;
  border: 1px solid var(--app-border);
  background: color-mix(in srgb, var(--app-surface) 92%, transparent);
}

.category-list-card :deep(.el-card__body) {
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

.category-toolbar {
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
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 14px;
}

.category-card {
  cursor: pointer;
  overflow: hidden;
  border: 1px solid color-mix(in srgb, var(--category-accent) 16%, var(--app-border));
  background: linear-gradient(180deg, color-mix(in srgb, var(--category-surface) 18%, #fff) 0%, #fff 42%);
  transition: box-shadow 200ms ease, transform 200ms ease, border-color 200ms ease, background 200ms ease;
}

.category-card :deep(.el-card__header) {
  border-bottom: none;
  padding: 14px 16px 0;
}

.category-card :deep(.el-card__body) {
  padding: 12px 16px 16px;
}

.category-card:hover {
  transform: translateY(-2px);
  border-color: color-mix(in srgb, var(--category-accent) 42%, var(--app-border));
}

.category-card.is-selected {
  border-color: color-mix(in srgb, var(--category-accent) 56%, var(--el-color-primary));
  box-shadow: 0 0 0 1px color-mix(in srgb, var(--category-accent) 20%, transparent), var(--el-box-shadow-light);
  background: linear-gradient(180deg, color-mix(in srgb, var(--category-surface) 28%, #fff) 0%, #fff 56%);
}

.category-card:focus {
  outline: 2px solid var(--el-color-primary);
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  .category-card {
    transition: none;
  }

  .category-card:hover {
    transform: none;
  }
}

.category-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.category-card-header .left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.category-avatar {
  background: linear-gradient(145deg, var(--category-accent) 0%, var(--category-contrast) 100%);
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  flex-shrink: 0;
}

.category-card-header .heading {
  min-width: 0;
}

.category-card-header .name {
  font-size: 16px;
  font-weight: 700;
  line-height: 1.35;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.category-card-header .meta {
  margin-top: 6px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.meta-chip {
  display: inline-flex;
  align-items: center;
  min-height: 26px;
  padding: 0 10px;
  border-radius: 999px;
  border: 1px solid color-mix(in srgb, var(--category-accent) 16%, var(--app-border));
  background: color-mix(in srgb, var(--category-surface) 46%, var(--app-surface));
  color: var(--el-text-color-secondary);
  font-size: 12px;
  white-space: nowrap;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}

.category-card-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.category-card-facts {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}

.fact {
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid var(--el-border-color-lighter);
  background: color-mix(in srgb, var(--app-surface) 88%, transparent);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.fact .label {
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

.fact strong {
  color: var(--el-text-color-primary);
  font-size: 14px;
  font-weight: 700;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.remark {
  color: var(--el-text-color-regular);
  line-height: 20px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 60px;
}

.muted {
  color: var(--el-text-color-secondary);
}

.category-card-actions {
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid var(--el-border-color-lighter);
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
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

  .category-card :deep(.el-card__header) {
    padding: 12px 12px 0;
  }

  .category-card :deep(.el-card__body) {
    padding: 12px;
  }

  .category-card-header {
    align-items: flex-start;
  }

  .category-card-header .left {
    gap: 8px;
  }

  .category-card-facts {
    grid-template-columns: 1fr;
  }

  .category-card-actions {
    justify-content: space-between;
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .category-avatar {
    width: 38px;
    height: 38px;
    font-size: 16px;
  }

  .meta-chip {
    max-width: calc(100vw - 160px);
  }
}
</style>
