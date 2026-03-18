<template>
  <div class="app-container kb-tag">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="标签名称" prop="tagName">
        <el-input
          v-model="queryParams.tagName"
          placeholder="请输入标签名称"
          clearable
          style="width: 220px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="标签状态" clearable style="width: 180px">
          <el-option v-for="dict in sys_normal_disable" :key="dict.value" :label="dict.label" :value="dict.value" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8 tag-toolbar">
      <el-col :span="1.5">
        <el-button type="primary" plain icon="Plus" @click="handleAdd" v-hasPermi="['tool:kb:tag:add']">
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
          v-hasPermi="['tool:kb:tag:edit']"
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
          v-hasPermi="['tool:kb:tag:remove']"
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

    <el-card shadow="never" class="tag-list-card">
      <template #header>
        <div class="card-header">
          <div class="title">
            <span>教程标签</span>
            <el-tag type="info" effect="plain" class="count-tag">{{ total }} 条</el-tag>
          </div>
        </div>
      </template>

      <el-table
        v-if="viewMode === 'table'"
        ref="tableRef"
        v-loading="loading"
        :data="tagList"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column label="ID" align="center" prop="tagId" width="90" />
        <el-table-column label="编码" align="center" prop="tagCode" width="160" />
        <el-table-column label="名称" align="center" prop="tagName" min-width="220" show-overflow-tooltip />
        <el-table-column label="排序" align="center" prop="tagSort" width="90" />
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
              v-hasPermi="['tool:kb:tag:edit']"
            >
              修改
            </el-button>
            <el-button
              link
              type="primary"
              icon="Delete"
              @click="handleDelete(scope.row)"
              v-hasPermi="['tool:kb:tag:remove']"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-else v-loading="loading" class="card-view">
        <el-empty v-if="!tagList.length" description="暂无数据" />
        <div v-else class="card-grid">
          <el-card
            v-for="item in tagList"
            :key="item.tagId"
            class="tag-card"
            :class="{ 'is-selected': isSelected(item.tagId) }"
            :style="tagCardStyle(item)"
            shadow="hover"
            role="button"
            tabindex="0"
            @click="toggleSelection(item.tagId)"
            @keydown.enter.prevent="toggleSelection(item.tagId)"
            @keydown.space.prevent="toggleSelection(item.tagId)"
          >
            <template #header>
              <div class="tag-card-header">
                <div class="left">
                  <el-checkbox
                    :model-value="isSelected(item.tagId)"
                    @click.stop
                    @change="toggleSelection(item.tagId)"
                  />
                  <el-avatar class="tag-avatar" shape="square" :size="42">
                    {{ tagGlyph(item.tagName) }}
                  </el-avatar>
                  <div class="heading">
                    <div class="name" :title="item.tagName">{{ item.tagName || '-' }}</div>
                    <div class="meta">
                      <span class="meta-chip">{{ item.tagCode || '未设编码' }}</span>
                      <span class="meta-chip">排序 {{ item.tagSort ?? 0 }}</span>
                    </div>
                  </div>
                </div>
                <dict-tag :options="sys_normal_disable" :value="item.status" />
              </div>
            </template>

            <div class="tag-card-body">
              <div class="tag-card-facts">
                <div class="fact">
                  <span class="label">标签ID</span>
                  <strong>#{{ item.tagId || '-' }}</strong>
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

            <div class="tag-card-actions">
              <el-button
                link
                type="primary"
                icon="Edit"
                @click.stop="handleUpdate(item)"
                v-hasPermi="['tool:kb:tag:edit']"
              >
                修改
              </el-button>
              <el-button
                link
                type="danger"
                icon="Delete"
                @click.stop="handleDelete(item)"
                v-hasPermi="['tool:kb:tag:remove']"
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
      <el-form ref="tagRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="标签名称" prop="tagName">
          <el-input v-model="form.tagName" placeholder="请输入标签名称" />
        </el-form-item>
        <el-form-item label="标签编码" prop="tagCode">
          <el-input v-model="form.tagCode" placeholder="可选：用于快速识别" />
        </el-form-item>
        <el-form-item label="排序" prop="tagSort">
          <el-input-number v-model="form.tagSort" controls-position="right" :min="0" />
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

<script setup name="KbTag">
import { addKbTag, delKbTag, getKbTag, listKbTag, updateKbTag } from '@/api/tool/kb/tag'
import { cardToneVars, firstCardGlyph } from '@/utils/cardTheme'
import { parseTime } from '@/utils/ruoyi'

const { proxy } = getCurrentInstance()
const { sys_normal_disable } = proxy.useDict('sys_normal_disable')

const tagList = ref([])
const open = ref(false)
const loading = ref(true)
const showSearch = ref(true)
const tableRef = ref()
const ids = ref([])
const single = ref(true)
const multiple = ref(true)
const total = ref(0)
const title = ref('')
const viewModeStorageKey = 'tool:kb:tag:viewMode'
const viewMode = ref('table')

const tagCardTones = [
  { accent: '#9f3f7f', surface: '#f4d9ea', contrast: '#64284f' },
  { accent: '#2f6fed', surface: '#dce8ff', contrast: '#173d84' },
  { accent: '#0f766e', surface: '#d7f3ee', contrast: '#114f4a' },
  { accent: '#c27712', surface: '#f7e2be', contrast: '#7a4700' },
  { accent: '#7b61ff', surface: '#e8e1ff', contrast: '#4b33ad' }
]

const queryParams = ref({
  pageNum: 1,
  pageSize: 10,
  tagName: undefined,
  status: undefined
})

const form = reactive({
  tagId: undefined,
  tagCode: undefined,
  tagName: undefined,
  tagSort: 0,
  status: '0',
  remark: undefined
})

const rules = {
  tagName: [{ required: true, message: '标签名称不能为空', trigger: 'blur' }],
  tagSort: [{ required: true, message: '排序不能为空', trigger: 'blur' }]
}

function loadViewMode() {
  try {
    const cached = localStorage.getItem(viewModeStorageKey)
    viewMode.value = cached === 'card' ? 'card' : 'table'
  } catch (e) {
    viewMode.value = 'table'
  }
}

function tagCardStyle(item) {
  return cardToneVars([item?.tagName, item?.tagCode].filter(Boolean).join('|'), tagCardTones, 'tag')
}

function tagGlyph(name) {
  return firstCardGlyph(name, '签')
}

function formatCardTime(value) {
  return parseTime(value) || '未记录'
}

function reset() {
  form.tagId = undefined
  form.tagCode = undefined
  form.tagName = undefined
  form.tagSort = 0
  form.status = '0'
  form.remark = undefined
  proxy.resetForm('tagRef')
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

function isSelected(tagId) {
  return ids.value.includes(String(tagId))
}

function toggleSelection(tagId) {
  const id = String(tagId)
  if (!id) return
  const next = ids.value.includes(id) ? ids.value.filter((item) => item !== id) : [...ids.value, id]
  ids.value = next
  single.value = next.length !== 1
  multiple.value = !next.length
}

function getList() {
  loading.value = true
  listKbTag(queryParams.value)
    .then((response) => {
      tagList.value = response.rows || []
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
  ids.value = selection.map((item) => String(item.tagId))
  single.value = selection.length !== 1
  multiple.value = !selection.length
}

function handleAdd() {
  reset()
  open.value = true
  title.value = '新增标签'
}

function handleUpdate(row) {
  reset()
  const tagId = row?.tagId || ids.value[0]
  if (!tagId) return
  getKbTag(tagId).then((response) => {
    Object.assign(form, response.data || {})
    open.value = true
    title.value = '修改标签'
  })
}

function submitForm() {
  proxy.$refs['tagRef'].validate((valid) => {
    if (!valid) return
    const request = form.tagId ? updateKbTag : addKbTag
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
  const tagIds = row?.tagId || ids.value.join(',')
  if (!tagIds) return
  proxy.$modal
    .confirm('是否确认删除标签编号为 "' + tagIds + '" 的数据项？')
    .then(() => delKbTag(tagIds))
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
.tag-list-card {
  border-radius: 16px;
  border: 1px solid var(--app-border);
  background: color-mix(in srgb, var(--app-surface) 92%, transparent);
}

.tag-list-card :deep(.el-card__body) {
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

.tag-toolbar {
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

.tag-card {
  cursor: pointer;
  overflow: hidden;
  border: 1px solid color-mix(in srgb, var(--tag-accent) 16%, var(--app-border));
  background: linear-gradient(180deg, color-mix(in srgb, var(--tag-surface) 18%, #fff) 0%, #fff 42%);
  transition: box-shadow 200ms ease, transform 200ms ease, border-color 200ms ease, background 200ms ease;
}

.tag-card :deep(.el-card__header) {
  border-bottom: none;
  padding: 14px 16px 0;
}

.tag-card :deep(.el-card__body) {
  padding: 12px 16px 16px;
}

.tag-card:hover {
  transform: translateY(-2px);
  border-color: color-mix(in srgb, var(--tag-accent) 42%, var(--app-border));
}

.tag-card.is-selected {
  border-color: color-mix(in srgb, var(--tag-accent) 56%, var(--el-color-primary));
  box-shadow: 0 0 0 1px color-mix(in srgb, var(--tag-accent) 20%, transparent), var(--el-box-shadow-light);
  background: linear-gradient(180deg, color-mix(in srgb, var(--tag-surface) 28%, #fff) 0%, #fff 56%);
}

.tag-card:focus {
  outline: 2px solid var(--el-color-primary);
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  .tag-card {
    transition: none;
  }

  .tag-card:hover {
    transform: none;
  }
}

.tag-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.tag-card-header .left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.tag-avatar {
  background: linear-gradient(145deg, var(--tag-accent) 0%, var(--tag-contrast) 100%);
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  flex-shrink: 0;
}

.tag-card-header .heading {
  min-width: 0;
}

.tag-card-header .name {
  font-size: 16px;
  font-weight: 700;
  line-height: 1.35;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.tag-card-header .meta {
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
  border: 1px solid color-mix(in srgb, var(--tag-accent) 16%, var(--app-border));
  background: color-mix(in srgb, var(--tag-surface) 46%, var(--app-surface));
  color: var(--el-text-color-secondary);
  font-size: 12px;
  white-space: nowrap;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tag-card-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tag-card-facts {
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

.tag-card-actions {
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

  .tag-card :deep(.el-card__header) {
    padding: 12px 12px 0;
  }

  .tag-card :deep(.el-card__body) {
    padding: 12px;
  }

  .tag-card-header {
    align-items: flex-start;
  }

  .tag-card-header .left {
    gap: 8px;
  }

  .tag-card-facts {
    grid-template-columns: 1fr;
  }

  .tag-card-actions {
    justify-content: space-between;
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .tag-avatar {
    width: 38px;
    height: 38px;
    font-size: 16px;
  }

  .meta-chip {
    max-width: calc(100vw - 160px);
  }
}
</style>
