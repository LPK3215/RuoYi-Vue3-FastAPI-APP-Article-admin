<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="分类名称" prop="categoryName">
        <el-input
          v-model="queryParams.categoryName"
          placeholder="请输入分类名称"
          clearable
          style="width: 200px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="分类状态" clearable style="width: 200px">
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
        <el-button type="primary" plain icon="Plus" @click="handleAdd" v-hasPermi="['tool:software:category:add']">
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
          v-hasPermi="['tool:software:category:edit']"
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
          v-hasPermi="['tool:software:category:remove']"
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
            <span>分类列表</span>
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
        <el-table-column label="分类ID" align="center" prop="categoryId" width="90" />
        <el-table-column label="分类编码" align="center" prop="categoryCode" />
        <el-table-column label="分类名称" align="center" prop="categoryName" />
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
              v-hasPermi="['tool:software:category:edit']"
            >
              修改
            </el-button>
            <el-button
              link
              type="primary"
              icon="Delete"
              @click="handleDelete(scope.row)"
              v-hasPermi="['tool:software:category:remove']"
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
                  <div class="name" :title="item.categoryName">{{ item.categoryName || '-' }}</div>
                </div>
                <dict-tag :options="sys_normal_disable" :value="item.status" />
              </div>
            </template>

            <div class="category-card-body">
              <div class="kv">
                <div class="kv-item">
                  <span class="k">编码</span>
                  <span class="v">{{ item.categoryCode || '-' }}</span>
                </div>
                <div class="kv-item">
                  <span class="k">排序</span>
                  <span class="v">{{ item.categorySort }}</span>
                </div>
                <div class="kv-item">
                  <span class="k">创建</span>
                  <span class="v">{{ parseTime(item.createTime) || '-' }}</span>
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
                v-hasPermi="['tool:software:category:edit']"
              >
                修改
              </el-button>
              <el-button
                link
                type="danger"
                icon="Delete"
                @click.stop="handleDelete(item)"
                v-hasPermi="['tool:software:category:remove']"
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

    <!-- 添加或修改分类对话框 -->
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

<script setup name="SoftwareCategory">
import {
  addSoftwareCategory,
  delSoftwareCategory,
  getSoftwareCategory,
  listSoftwareCategory,
  updateSoftwareCategory
} from '@/api/tool/software/category'

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

const viewModeStorageKey = 'tool:software:category:viewMode'
const viewMode = ref('table')

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    categoryName: undefined,
    status: undefined
  },
  rules: {
    categoryName: [{ required: true, message: '分类名称不能为空', trigger: 'blur' }],
    categorySort: [{ required: true, message: '排序不能为空', trigger: 'blur' }]
  }
})

const { queryParams, form, rules } = toRefs(data)

function loadViewMode() {
  try {
    const cached = localStorage.getItem(viewModeStorageKey)
    viewMode.value = cached === 'card' ? 'card' : 'table'
  } catch (e) {
    viewMode.value = 'table'
  }
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
  const next = ids.value.includes(id) ? ids.value.filter((x) => x !== id) : [...ids.value, id]
  ids.value = next
  single.value = next.length !== 1
  multiple.value = !next.length
}

function getList() {
  loading.value = true
  listSoftwareCategory(queryParams.value).then((response) => {
    categoryList.value = response.rows || []
    total.value = response.total || 0
    loading.value = false
  })
}

function cancel() {
  open.value = false
  reset()
}

function reset() {
  form.value = {
    categoryId: undefined,
    categoryCode: undefined,
    categoryName: undefined,
    categorySort: 0,
    status: '0',
    remark: undefined
  }
  proxy.resetForm('categoryRef')
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
  getSoftwareCategory(categoryId).then((response) => {
    form.value = response.data
    open.value = true
    title.value = '修改分类'
  })
}

function submitForm() {
  proxy.$refs['categoryRef'].validate((valid) => {
    if (!valid) return
    const request = form.value.categoryId ? updateSoftwareCategory : addSoftwareCategory
    request(form.value).then(() => {
      proxy.$modal.msgSuccess('操作成功')
      open.value = false
      getList()
    })
  })
}

function handleDelete(row) {
  const categoryIds = row?.categoryId || ids.value.join(',')
  proxy.$modal
    .confirm('是否确认删除分类编号为 "' + categoryIds + '" 的数据项？')
    .then(() => delSoftwareCategory(categoryIds))
    .then(() => {
      getList()
      proxy.$modal.msgSuccess('删除成功')
    })
    .catch(() => {})
}

loadViewMode()
getList()
</script>

<style scoped>
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

.category-list-card :deep(.el-card__body) {
  padding-top: 8px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.card-header .title {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}

.card-view {
  min-height: 240px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 12px;
}

.category-card {
  cursor: pointer;
  transition: box-shadow 200ms ease, transform 200ms ease, border-color 200ms ease;
}

.category-card:hover {
  transform: translateY(-2px);
}

.category-card.is-selected {
  border-color: var(--el-color-primary);
  box-shadow: var(--el-box-shadow-light);
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

.category-card-header .name {
  font-weight: 600;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.category-card-body {
  padding: 2px 2px 0;
}

.kv {
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
}

.kv-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.kv-item .k {
  color: var(--el-text-color-secondary);
  white-space: nowrap;
}

.kv-item .v {
  color: var(--el-text-color-regular);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 220px;
}

.remark {
  margin-top: 10px;
  color: var(--el-text-color-regular);
  line-height: 20px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 40px;
}

.muted {
  color: var(--el-text-color-secondary);
}

.category-card-actions {
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid var(--el-border-color-lighter);
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
