<template>
  <div class="app-container software-edit">
    <section class="page-header">
      <div class="page-header__left">
        <el-button icon="ArrowLeft" @click="goBack">返回</el-button>
        <div class="page-header__title">
          <div class="page-header__h">编辑软件</div>
          <div class="page-header__sub" v-if="softwareId">
            <span class="sub-item">ID：{{ softwareId }}</span>
            <span class="dot">•</span>
            <span class="sub-item">{{ form.softwareName || '未命名' }}</span>
          </div>
        </div>
      </div>

      <div class="page-header__right">
        <el-button plain icon="View" :disabled="!softwareId" @click="goDetail">预览</el-button>
        <el-button type="primary" icon="Check" :loading="saving" @click="submit(false)">保存</el-button>
        <el-button type="success" icon="CircleCheck" :loading="saving" @click="submit(true)">保存并返回</el-button>
      </div>
    </section>

    <el-card shadow="never" class="edit-card" v-loading="loading">
      <el-form ref="softwareRef" :model="form" :rules="rules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="软件名称" prop="softwareName">
              <el-input v-model="form.softwareName" placeholder="请输入软件名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="分类" prop="categoryId">
              <el-select v-model="form.categoryId" placeholder="请选择分类" filterable style="width: 100%">
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

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="发布状态" prop="publishStatus">
              <el-select v-model="form.publishStatus" placeholder="请选择发布状态" style="width: 100%">
                <el-option v-for="o in publishStatusOptions" :key="o.value" :label="o.label" :value="o.value" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-radio-group v-model="form.status">
                <el-radio v-for="dict in sys_normal_disable" :key="dict.value" :value="dict.value">
                  {{ dict.label }}
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="排序" prop="softwareSort">
              <el-input-number v-model="form.softwareSort" controls-position="right" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="图标" prop="iconUrl">
              <ImageUpload v-model="form.iconUrl" :limit="1" :fileSize="2" :fileType="['png', 'jpg', 'jpeg', 'svg']" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="简短描述" prop="shortDesc">
          <el-input
            v-model="form.shortDesc"
            type="textarea"
            :autosize="{ minRows: 2, maxRows: 4 }"
            placeholder="可选：一句话描述"
          />
        </el-form-item>

        <el-divider content-position="left">元信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="开源" prop="openSource">
              <el-switch v-model="form.openSource" active-value="1" inactive-value="0" />
            </el-form-item>
          </el-col>
          <el-col :span="18">
            <el-form-item label="许可证" prop="license">
              <el-select
                v-model="form.license"
                placeholder="例如：MIT / Apache-2.0 / GPL-3.0"
                clearable
                filterable
                allow-create
                default-first-option
                style="width: 100%"
              >
                <el-option v-for="o in facets.licenses" :key="o.value" :label="o.value" :value="o.value" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="标签" prop="tags">
          <el-select
            v-model="formTagsList"
            multiple
            filterable
            allow-create
            default-first-option
            clearable
            collapse-tags
            collapse-tags-tooltip
            placeholder="输入标签后回车（支持逗号/换行/分号，会自动规范化）"
            style="width: 100%"
          >
            <el-option v-for="o in facets.tags" :key="o.value" :label="o.value" :value="o.value" />
          </el-select>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="官网" prop="officialUrl">
              <el-input v-model="form.officialUrl" placeholder="https://..." />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="仓库" prop="repoUrl">
              <el-input v-model="form.repoUrl" placeholder="https://github.com/..." />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="作者" prop="author">
              <el-input v-model="form.author" placeholder="可选" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="团队" prop="team">
              <el-input v-model="form.team" placeholder="可选" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-tabs v-model="activeMdTab" type="border-card">
          <el-tab-pane label="介绍（Markdown）" name="desc">
            <div class="md-actions">
              <el-button size="small" plain icon="Upload" @click="openImportMarkdown('descriptionMd')">导入 .md/.txt</el-button>
              <span class="md-actions__hint">支持 UTF-8，最大 1MB（会覆盖当前内容）</span>
            </div>
            <el-row :gutter="12">
              <el-col :span="12">
                <el-input
                  v-model="form.descriptionMd"
                  type="textarea"
                  :autosize="{ minRows: 14, maxRows: 20 }"
                  placeholder="支持 Markdown，左侧编辑，右侧预览"
                />
              </el-col>
              <el-col :span="12">
                <div class="md-preview">
                  <MarkdownPreview :content="form.descriptionMd || ''" />
                </div>
              </el-col>
            </el-row>
          </el-tab-pane>
          <el-tab-pane label="使用说明（Markdown）" name="usage">
            <div class="md-actions">
              <el-button size="small" plain icon="Upload" @click="openImportMarkdown('usageMd')">导入 .md/.txt</el-button>
              <span class="md-actions__hint">支持 UTF-8，最大 1MB（会覆盖当前内容）</span>
            </div>
            <el-row :gutter="12">
              <el-col :span="12">
                <el-input
                  v-model="form.usageMd"
                  type="textarea"
                  :autosize="{ minRows: 14, maxRows: 20 }"
                  placeholder="支持 Markdown，左侧编辑，右侧预览"
                />
              </el-col>
              <el-col :span="12">
                <div class="md-preview">
                  <MarkdownPreview :content="form.usageMd || ''" />
                </div>
              </el-col>
            </el-row>
          </el-tab-pane>
        </el-tabs>
        <input
          ref="mdFileInputRef"
          class="hidden-file-input"
          type="file"
          accept=".md,.markdown,.txt,text/markdown,text/plain"
          @change="handleMarkdownFileImport"
        />

        <el-divider content-position="left">多平台下载配置</el-divider>
        <el-row class="mb8">
          <el-col :span="24">
            <el-button type="primary" plain icon="Plus" @click="handleAddDownloadRow">新增下载</el-button>
          </el-col>
        </el-row>

        <el-table :data="form.downloads" border>
          <el-table-column label="平台" prop="platform" width="140">
            <template #default="scope">
              <el-select v-model="scope.row.platform" placeholder="平台" clearable style="width: 120px">
                <el-option v-for="p in platformOptions" :key="p.value" :label="p.label" :value="p.value" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="下载地址" prop="downloadUrl" min-width="260">
            <template #default="scope">
              <el-input v-model="scope.row.downloadUrl" placeholder="https://..." />
            </template>
          </el-table-column>
          <el-table-column label="版本" prop="version" width="120">
            <template #default="scope">
              <el-input v-model="scope.row.version" placeholder="可选" />
            </template>
          </el-table-column>
          <el-table-column label="校验值" prop="checksum" width="160">
            <template #default="scope">
              <el-input v-model="scope.row.checksum" placeholder="可选" />
            </template>
          </el-table-column>
          <el-table-column label="排序" prop="sort" width="90">
            <template #default="scope">
              <el-input-number v-model="scope.row.sort" controls-position="right" :min="0" style="width: 70px" />
            </template>
          </el-table-column>
          <el-table-column label="备注" prop="remark" width="180">
            <template #default="scope">
              <el-input v-model="scope.row.remark" placeholder="可选" />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="80" align="center">
            <template #default="scope">
              <el-button link type="primary" icon="Delete" @click="handleRemoveDownloadRow(scope.$index)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-divider content-position="left">资源（仅 URL）</el-divider>
        <el-row class="mb8">
          <el-col :span="24">
            <el-button type="primary" plain icon="Plus" @click="handleAddResourceRow">新增资源</el-button>
          </el-col>
        </el-row>

        <el-table :data="form.resources" border>
          <el-table-column label="类型" prop="resourceType" width="140">
            <template #default="scope">
              <el-select v-model="scope.row.resourceType" placeholder="类型" clearable style="width: 120px">
                <el-option v-for="t in resourceTypeOptions" :key="t.value" :label="t.label" :value="t.value" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="标题" prop="title" width="180">
            <template #default="scope">
              <el-input v-model="scope.row.title" placeholder="可选" />
            </template>
          </el-table-column>
          <el-table-column label="URL" prop="resourceUrl" min-width="260">
            <template #default="scope">
              <el-input v-model="scope.row.resourceUrl" placeholder="https://..." />
            </template>
          </el-table-column>
          <el-table-column label="排序" prop="sort" width="90">
            <template #default="scope">
              <el-input-number v-model="scope.row.sort" controls-position="right" :min="0" style="width: 70px" />
            </template>
          </el-table-column>
          <el-table-column label="备注" prop="remark" width="180">
            <template #default="scope">
              <el-input v-model="scope.row.remark" placeholder="可选" />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="80" align="center">
            <template #default="scope">
              <el-button link type="primary" icon="Delete" @click="handleRemoveResourceRow(scope.$index)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-form>
    </el-card>
  </div>
</template>

<script setup name="SoftwareItemEdit">
import MarkdownPreview from '@/components/MarkdownPreview'

import { listSoftwareCategoryOptions } from '@/api/tool/software/category'
import { getSoftwareItem, getSoftwareItemFacets, updateSoftwareItem } from '@/api/tool/software/item'

const { proxy } = getCurrentInstance()
const { sys_normal_disable } = proxy.useDict('sys_normal_disable')

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const saving = ref(false)
const activeMdTab = ref('desc')

const mdFileInputRef = ref()
const mdImportTarget = ref('descriptionMd')
const MAX_MARKDOWN_FILE_SIZE = 1024 * 1024
const ALLOWED_MD_EXTS = ['md', 'markdown', 'txt']

const publishStatusOptions = [
  { label: '草稿', value: '0' },
  { label: '上架', value: '1' },
  { label: '下架', value: '2' }
]

const platformOptions = [
  { label: 'Windows', value: 'windows' },
  { label: 'macOS', value: 'mac' },
  { label: 'Linux', value: 'linux' },
  { label: 'Android', value: 'android' },
  { label: 'iOS', value: 'ios' },
  { label: 'Web', value: 'web' },
  { label: '其他', value: 'other' }
]

const resourceTypeOptions = [
  { label: '截图', value: 'screenshot' },
  { label: '文档', value: 'doc' },
  { label: '链接', value: 'link' },
  { label: '视频', value: 'video' },
  { label: '其他', value: 'other' }
]

const categoryOptions = ref([])
const facets = reactive({
  tags: [],
  licenses: [],
  authors: [],
  teams: [],
  platforms: []
})

function defaultForm() {
  return {
    softwareId: undefined,
    categoryId: undefined,
    softwareName: undefined,
    shortDesc: undefined,
    iconUrl: undefined,
    officialUrl: undefined,
    repoUrl: undefined,
    author: undefined,
    team: undefined,
    license: undefined,
    openSource: '0',
    tags: undefined,
    descriptionMd: undefined,
    usageMd: undefined,
    publishStatus: '0',
    softwareSort: 0,
    status: '0',
    downloads: [],
    resources: []
  }
}

const form = reactive(defaultForm())
const rules = {
  softwareName: [{ required: true, message: '软件名称不能为空', trigger: 'blur' }],
  categoryId: [{ required: true, message: '分类不能为空', trigger: 'change' }],
  softwareSort: [{ required: true, message: '排序不能为空', trigger: 'blur' }]
}

const softwareId = computed(() => {
  const raw = route.query?.softwareId
  const val = Array.isArray(raw) ? raw[0] : raw
  const n = Number(val)
  return Number.isFinite(n) && n > 0 ? n : undefined
})

const formTagsList = computed({
  get: () => splitTags(form.tags || ''),
  set: (arr) => {
    const next = splitTags((arr || []).join(','))
    form.tags = next.length ? next.join(',') : undefined
  }
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

function goBack() {
  router.back()
}

function goDetail() {
  if (!softwareId.value) return
  router.push({ path: '/software/detail', query: { softwareId: softwareId.value } })
}

function getCategoryOptions() {
  listSoftwareCategoryOptions().then((res) => {
    categoryOptions.value = res.data || []
  })
}

function getFacets() {
  getSoftwareItemFacets({ limit: 80 })
    .then((res) => {
      const data = res.data || {}
      facets.tags = data.tags || []
      facets.licenses = data.licenses || []
      facets.authors = data.authors || []
      facets.teams = data.teams || []
      facets.platforms = data.platforms || []
    })
    .catch(() => {})
}

function loadDetail() {
  if (!softwareId.value) {
    proxy.$modal.msgError('缺少 softwareId 参数，无法进入编辑页')
    return
  }
  loading.value = true
  getSoftwareItem(softwareId.value)
    .then((res) => {
      const data = res.data || {}
      Object.assign(form, defaultForm(), data)
      form.downloads = data.downloads || []
      form.resources = data.resources || []
    })
    .catch(() => {})
    .finally(() => {
      loading.value = false
    })
}

function getMdTargetLabel(target) {
  if (target === 'usageMd') return '使用说明'
  return '介绍'
}

function getFileExt(name) {
  const base = String(name || '')
  const idx = base.lastIndexOf('.')
  if (idx <= -1) return ''
  return base.slice(idx + 1).toLowerCase()
}

function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(String(reader.result || ''))
    reader.onerror = () => reject(reader.error || new Error('read failed'))
    reader.readAsText(file, 'utf-8')
  })
}

function openImportMarkdown(target) {
  mdImportTarget.value = target
  const inputEl = mdFileInputRef.value
  if (!inputEl) return
  // 允许选择同一个文件多次触发 change
  inputEl.value = ''
  inputEl.click()
}

async function handleMarkdownFileImport(e) {
  const inputEl = e?.target
  const file = inputEl?.files?.[0]
  if (inputEl) inputEl.value = ''
  if (!file) return

  const ext = getFileExt(file.name)
  if (!ALLOWED_MD_EXTS.includes(ext)) {
    proxy.$modal.msgError('仅支持导入 .md/.markdown/.txt 文件')
    return
  }

  if (file.size > MAX_MARKDOWN_FILE_SIZE) {
    const kb = (file.size / 1024).toFixed(1)
    proxy.$modal.msgError(`文件过大（${kb}KB），最大支持 ${(MAX_MARKDOWN_FILE_SIZE / 1024).toFixed(0)}KB`)
    return
  }

  const target = mdImportTarget.value
  const label = getMdTargetLabel(target)
  const current = String(form[target] || '').trim()
  if (current) {
    try {
      await proxy.$modal.confirm(`当前「${label}」不为空，导入将覆盖现有内容，是否继续？`)
    } catch (e) {
      return
    }
  }

  try {
    const text = await readFileAsText(file)
    form[target] = text
    proxy.$modal.msgSuccess(`已导入「${file.name}」到「${label}」`)
  } catch (e) {
    proxy.$modal.msgError('读取文件失败，请确认文件编码为 UTF-8')
  }
}

function validateDownloads() {
  if (!form.downloads || !form.downloads.length) return true
  for (const [index, d] of form.downloads.entries()) {
    if (!d.platform || !d.downloadUrl) {
      proxy.$modal.msgError(`第 ${index + 1} 行下载配置未填写完整（平台/下载地址必填）`)
      return false
    }
  }
  return true
}

function validateResources() {
  if (!form.resources || !form.resources.length) return true
  for (const [index, r] of form.resources.entries()) {
    if (!r.resourceType || !r.resourceUrl) {
      proxy.$modal.msgError(`第 ${index + 1} 行资源未填写完整（类型/URL必填）`)
      return false
    }
  }
  return true
}

function submit(backToDetail) {
  if (!softwareId.value) return
  proxy.$refs['softwareRef'].validate((valid) => {
    if (!valid) return
    if (!validateDownloads()) return
    if (!validateResources()) return

    saving.value = true
    updateSoftwareItem(form)
      .then((res) => {
        proxy.$modal.msgSuccess(res?.msg || '保存成功')
        if (backToDetail) {
          goDetail()
          return
        }
        loadDetail()
      })
      .catch(() => {})
      .finally(() => {
        saving.value = false
      })
  })
}

function handleAddDownloadRow() {
  if (!form.downloads) form.downloads = []
  form.downloads.push({
    platform: undefined,
    downloadUrl: undefined,
    version: undefined,
    checksum: undefined,
    sort: 0,
    remark: undefined
  })
}

function handleRemoveDownloadRow(index) {
  form.downloads.splice(index, 1)
}

function handleAddResourceRow() {
  if (!form.resources) form.resources = []
  form.resources.push({
    resourceType: undefined,
    title: undefined,
    resourceUrl: undefined,
    sort: 0,
    remark: undefined
  })
}

function handleRemoveResourceRow(index) {
  form.resources.splice(index, 1)
}

getCategoryOptions()
getFacets()
loadDetail()
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.page-header__left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.page-header__title {
  min-width: 0;
}

.page-header__h {
  font-size: 18px;
  font-weight: 800;
  color: var(--el-text-color-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.page-header__sub {
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

.page-header__right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.edit-card {
  border-radius: 16px;
  border: 1px solid var(--app-border);
  background: color-mix(in srgb, var(--app-surface) 92%, transparent);
}

.md-preview {
  border: 1px solid var(--el-border-color);
  border-radius: 12px;
  padding: 10px 12px;
  min-height: 320px;
  max-height: 520px;
  overflow: auto;
  background: color-mix(in srgb, var(--app-surface) 86%, transparent);
}

.md-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.md-actions__hint {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.hidden-file-input {
  display: none;
}
</style>
