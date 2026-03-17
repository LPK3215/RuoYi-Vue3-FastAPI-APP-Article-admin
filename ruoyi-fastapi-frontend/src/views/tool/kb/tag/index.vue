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

      <el-table ref="tableRef" v-loading="loading" :data="tagList" @selection-change="handleSelectionChange">
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
import { parseTime } from '@/utils/ruoyi'

const { proxy } = getCurrentInstance()
const { sys_normal_disable } = proxy.useDict('sys_normal_disable')

const tagList = ref([])
const open = ref(false)
const loading = ref(true)
const showSearch = ref(true)
const ids = ref([])
const single = ref(true)
const multiple = ref(true)
const total = ref(0)
const title = ref('')

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

function reset() {
  form.tagId = undefined
  form.tagCode = undefined
  form.tagName = undefined
  form.tagSort = 0
  form.status = '0'
  form.remark = undefined
  proxy.resetForm('tagRef')
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
  ids.value = selection.map((item) => item.tagId)
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
      getList()
    })
    .catch(() => {})
}

function cancel() {
  open.value = false
  reset()
}

getList()
</script>

<style scoped>
.tag-list-card {
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

.tag-toolbar {
  align-items: center;
}

.toolbar-right {
  margin-left: auto;
}
</style>

