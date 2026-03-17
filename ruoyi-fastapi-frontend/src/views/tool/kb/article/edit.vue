<template>
  <div class="app-container kb-article-edit">
    <section class="page-header">
      <div class="page-header__left">
        <el-button icon="ArrowLeft" @click="goList">返回</el-button>
        <div class="page-header__title">
          <div class="page-header__h">
            {{ articleId ? '编辑教程' : '新增教程' }}
          </div>
          <div class="page-header__sub" v-if="articleId">
            <span class="sub-item">ID：{{ articleId }}</span>
            <span class="dot">•</span>
            <span class="sub-item">{{ form.title || '未命名' }}</span>
            <span class="dot">•</span>
            <span class="sub-item">更新时间：{{ parseTime(form.updateTime) || '-' }}</span>
          </div>
        </div>
      </div>

      <div class="page-header__right">
        <el-tag effect="plain" :type="publishStatusTagType(form.publishStatus)">
          {{ publishStatusLabel(form.publishStatus) }}
        </el-tag>
        <el-button type="primary" icon="Check" :loading="saving" @click="submit(false)">保存</el-button>
        <el-button type="success" icon="CircleCheck" :loading="saving" @click="submit(true)">保存并返回</el-button>
      </div>
    </section>

    <el-card shadow="never" class="edit-card" v-loading="loading">
      <el-form ref="articleRef" :model="form" :rules="rules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="标题" prop="title">
              <el-input v-model="form.title" placeholder="请输入标题" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="分类" prop="categoryId">
              <el-select v-model="form.categoryId" placeholder="未分类" clearable filterable style="width: 100%">
                <el-option v-for="c in categoryOptions" :key="c.categoryId" :label="c.categoryName" :value="c.categoryId" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="排序" prop="articleSort">
              <el-input-number v-model="form.articleSort" controls-position="right" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="摘要" prop="summary">
          <el-input
            v-model="form.summary"
            type="textarea"
            :autosize="{ minRows: 2, maxRows: 4 }"
            placeholder="可选：用于列表展示的摘要"
          />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="封面" prop="coverUrl">
              <ImageUpload v-model="form.coverUrl" :limit="1" :fileSize="4" :fileType="['png', 'jpg', 'jpeg', 'webp']" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="发布状态" prop="publishStatus">
              <el-select v-model="form.publishStatus" placeholder="请选择发布状态" style="width: 100%">
                <el-option v-for="o in publishStatusOptions" :key="o.value" :label="o.label" :value="o.value" />
              </el-select>
            </el-form-item>
            <el-form-item label="类型" prop="articleType">
              <el-select v-model="form.articleType" placeholder="教程/笔记/FAQ" clearable filterable style="width: 100%">
                <el-option v-for="d in kb_article_type" :key="d.value" :label="d.label" :value="d.value" />
              </el-select>
            </el-form-item>
            <el-form-item label="状态" prop="status">
              <el-radio-group v-model="form.status">
                <el-radio v-for="dict in sys_normal_disable" :key="dict.value" :value="dict.value">
                  {{ dict.label }}
                </el-radio>
              </el-radio-group>
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
            placeholder="输入标签后回车（支持逗号/换行/分号，会自动规整）"
            style="width: 100%"
          >
            <el-option v-for="t in tagOptions" :key="t.tagId" :label="t.tagName" :value="t.tagName" />
          </el-select>
        </el-form-item>

        <el-divider content-position="left">附件</el-divider>
        <el-form-item label="附件上传" prop="attachments">
          <FileUpload
            v-model="attachmentsValue"
            :limit="10"
            :fileSize="50"
            :fileType="['zip','rar','7z','txt','md','pdf','doc','docx','xls','xlsx','ppt','pptx','png','jpg','jpeg','webp']"
          />
          <div class="hint">上传后会保存为附件列表，可在 Portal 文章详情页下载。</div>
        </el-form-item>

        <el-divider content-position="left">正文（Markdown）</el-divider>
        <div class="md-actions">
          <el-button size="small" plain icon="Upload" @click="openImportMarkdown('contentMd')">导入 .md/.txt</el-button>
          <span class="md-actions__hint">支持 UTF-8，最大 1MB（会覆盖当前内容）</span>
        </div>
        <el-row :gutter="12">
          <el-col :span="12">
            <el-input
              v-model="form.contentMd"
              type="textarea"
              :autosize="{ minRows: 16, maxRows: 22 }"
              placeholder="支持 Markdown，左侧编辑，右侧预览"
            />
          </el-col>
          <el-col :span="12">
            <div class="md-preview">
              <MarkdownRender :content="form.contentMd || ''" />
            </div>
          </el-col>
        </el-row>
        <input
          ref="mdFileInputRef"
          class="hidden-file-input"
          type="file"
          accept=".md,.markdown,.txt,text/markdown,text/plain"
          @change="handleMarkdownFileImport"
        />

        <el-divider content-position="left">关联软件</el-divider>
        <el-row :gutter="12" class="software-picker">
          <el-col :span="18">
            <el-form-item label="添加软件">
              <div class="software-actions">
                <el-button plain icon="Filter" @click="softwareFilterDrawerOpen = true">筛选选择</el-button>
              </div>
              <el-select
                v-model="softwarePick"
                filterable
                remote
                clearable
                :remote-method="searchSoftware"
                :loading="softwareSearchLoading"
                placeholder="输入关键字搜索软件，选择后添加"
                style="width: 100%"
                @change="onPickSoftware"
              >
                <el-option
                  v-for="o in softwareOptions"
                  :key="o.softwareId"
                  :label="o.softwareName"
                  :value="o.softwareId"
                >
                  <div class="soft-option">
                    <span class="soft-option__name">{{ o.softwareName }}</span>
                    <span class="soft-option__meta">{{ o.categoryName || '未分类' }}</span>
                  </div>
                </el-option>
              </el-select>
              <div class="hint">
                仅<strong>上架</strong>的软件会在 Portal 文章页显示（草稿/下线会被自动过滤）。
              </div>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="仅上架">
              <el-switch v-model="onlyPublishedSoftwares" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-table :data="selectedSoftwareRows" size="small" border>
          <el-table-column label="#" width="56" align="center">
            <template #default="scope">
              {{ scope.$index + 1 }}
            </template>
          </el-table-column>
          <el-table-column label="软件" min-width="240">
            <template #default="scope">
              <div class="soft-cell">
                <el-avatar class="soft-icon" shape="square" :size="28" :src="scope.row.iconUrl">
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
          <el-table-column label="发布" width="100" align="center">
            <template #default="scope">
              <el-tag effect="plain" :type="softwarePublishTagType(scope.row.publishStatus)">
                {{ softwarePublishLabel(scope.row.publishStatus) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="更新时间" width="180" align="center">
            <template #default="scope">
              <span>{{ parseTime(scope.row.updateTime) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" align="center">
            <template #default="scope">
              <el-button link type="primary" icon="ArrowUp" :disabled="scope.$index === 0" @click="moveSoftware(scope.$index, -1)">
                上移
              </el-button>
              <el-button
                link
                type="primary"
                icon="ArrowDown"
                :disabled="scope.$index === selectedSoftwareRows.length - 1"
                @click="moveSoftware(scope.$index, 1)"
              >
                下移
              </el-button>
              <el-button link type="primary" icon="Delete" @click="removeSoftware(scope.$index)">移除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <SoftwareFilterDrawer
          v-model="softwareFilterDrawerOpen"
          @pick="onDrawerPickSoftware"
          @view="onDrawerViewSoftware"
        />
      </el-form>
    </el-card>
  </div>
</template>

<script setup name="KbArticleEdit">
import { MarkdownRender } from 'markstream-vue'
import 'markstream-vue/index.css'

import { addKbArticle, getKbArticle, updateKbArticle } from '@/api/tool/kb/article'
import { listKbCategoryOptions } from '@/api/tool/kb/category'
import { listKbTagOptions } from '@/api/tool/kb/tag'
import { getSoftwareItem, listSoftwareItem } from '@/api/tool/software/item'
import { parseTime } from '@/utils/ruoyi'

import SoftwareFilterDrawer from './components/SoftwareFilterDrawer.vue'

const { proxy } = getCurrentInstance()
const { sys_normal_disable, kb_article_type } = proxy.useDict('sys_normal_disable', 'kb_article_type')

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const saving = ref(false)

const softwareFilterDrawerOpen = ref(false)

const onlyPublishedSoftwares = ref(true)
const softwarePick = ref()
const softwareOptions = ref([])
const softwareSearchLoading = ref(false)
const softwareMeta = ref({})
const categoryOptions = ref([])
const tagOptions = ref([])

const publishStatusOptions = [
  { label: '草稿', value: '0' },
  { label: '发布', value: '1' },
  { label: '下线', value: '2' }
]

function defaultForm() {
  return {
    articleId: undefined,
    categoryId: undefined,
    title: undefined,
    summary: undefined,
    coverUrl: undefined,
    contentMd: undefined,
    articleType: undefined,
    tags: undefined,
    attachments: undefined,
    publishStatus: '0',
    publishTime: undefined,
    articleSort: 0,
    status: '0',
    createTime: undefined,
    updateTime: undefined,
    remark: undefined,
    softwareIds: []
  }
}

const form = reactive(defaultForm())
const rules = {
  title: [{ required: true, message: '标题不能为空', trigger: 'blur' }]
}

const articleId = computed(() => {
  const raw = route.query?.articleId
  const val = Array.isArray(raw) ? raw[0] : raw
  const n = Number(val)
  return Number.isFinite(n) && n > 0 ? n : undefined
})

const formTagsList = computed({
  get: () => splitTags(form.tags || ''),
  set: (arr) => {
    const next = splitTags((arr || []).join(','))
    form.tags = next.length ? next.join(',') : ''
  }
})

const selectedSoftwareRows = computed(() => {
  const list = Array.isArray(form.softwareIds) ? form.softwareIds : []
  return list.map((id) => {
    const meta = softwareMeta.value?.[String(id)]
    return (
      meta || {
        softwareId: id,
        softwareName: `软件 #${id}`,
        categoryName: undefined,
        publishStatus: undefined,
        updateTime: undefined,
        iconUrl: undefined
      }
    )
  })
})



const attachmentsValue = computed({
  get: () => {
    try {
      const arr = JSON.parse(String(form.attachments || ''))
      return Array.isArray(arr) ? arr : ''
    } catch (e) {
      return ''
    }
  },
  set: (val) => {
    if (!val) {
      form.attachments = null
      return
    }
    try {
      form.attachments = JSON.stringify(val)
    } catch (e) {
      form.attachments = null
    }
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

function loadDetail() {
  if (!articleId.value) return
  loading.value = true
  getKbArticle(articleId.value)
    .then(async (res) => {
      const data = res.data || {}
      Object.assign(form, defaultForm(), data)
      form.softwareIds = Array.isArray(data.softwareIds) ? data.softwareIds : []
      await hydrateSoftwares(form.softwareIds)
    })
    .catch(() => {})
    .finally(() => {
      loading.value = false
    })
}

let softwareSearchSeq = 0
function searchSoftware(keyword) {
  const q = String(keyword || '').trim()
  if (!q) {
    softwareOptions.value = []
    return
  }
  const currentSeq = (softwareSearchSeq += 1)
  softwareSearchLoading.value = true
  listSoftwareItem({
    pageNum: 1,
    pageSize: 20,
    keyword: q,
    publishStatus: onlyPublishedSoftwares.value ? '1' : undefined
  })
    .then((res) => {
      if (currentSeq !== softwareSearchSeq) return
      softwareOptions.value = res.rows || []
    })
    .catch(() => {})
    .finally(() => {
      if (currentSeq === softwareSearchSeq) softwareSearchLoading.value = false
    })
}

function onPickSoftware(val) {
  const n = Number(val)
  if (!Number.isFinite(n) || n <= 0) return
  if (!Array.isArray(form.softwareIds)) form.softwareIds = []
  if (form.softwareIds.includes(n)) {
    softwarePick.value = undefined
    return
  }
  form.softwareIds.push(n)
  const meta = (softwareOptions.value || []).find((x) => Number(x.softwareId) === n)
  if (meta) {
    softwareMeta.value = { ...softwareMeta.value, [String(n)]: meta }
  } else {
    hydrateSoftwares([n])
  }
  softwarePick.value = undefined
}

function addSoftwareFromMeta(meta) {
  const n = Number(meta?.softwareId)
  if (!Number.isFinite(n) || n <= 0) return
  if (!Array.isArray(form.softwareIds)) form.softwareIds = []
  if (form.softwareIds.includes(n)) return
  form.softwareIds.push(n)
  softwareMeta.value = { ...softwareMeta.value, [String(n)]: meta }
}

function onDrawerPickSoftware(row) {
  addSoftwareFromMeta(row)
}

function onDrawerViewSoftware(row) {
  const softwareId = row?.softwareId
  if (!softwareId) return
  router.push({ path: '/software/detail', query: { softwareId } }).catch(() => {})
}

function moveSoftware(index, delta) {
  if (!Array.isArray(form.softwareIds)) return
  const nextIndex = index + delta
  if (nextIndex < 0 || nextIndex >= form.softwareIds.length) return
  const list = form.softwareIds.slice()
  const [item] = list.splice(index, 1)
  list.splice(nextIndex, 0, item)
  form.softwareIds = list
}

function removeSoftware(index) {
  if (!Array.isArray(form.softwareIds)) return
  form.softwareIds.splice(index, 1)
}

const ALLOWED_MD_EXTS = ['md', 'markdown', 'txt']
const MAX_MARKDOWN_FILE_SIZE = 1024 * 1024
const mdFileInputRef = ref()
const mdImportTarget = ref('contentMd')

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
  const current = String(form[target] || '').trim()
  if (current) {
    try {
      await proxy.$modal.confirm('当前正文不为空，导入将覆盖现有内容，是否继续？')
    } catch (e) {
      return
    }
  }

  try {
    const text = await readFileAsText(file)
    form[target] = text
    proxy.$modal.msgSuccess(`已导入「${file.name}」`)
  } catch (e) {
    proxy.$modal.msgError('读取文件失败，请确认文件编码为 UTF-8')
  }
}

function submit(backToList) {
  proxy.$refs['articleRef'].validate((valid) => {
    if (!valid) return
    saving.value = true
    const request = form.articleId ? updateKbArticle : addKbArticle
    const payload = {
      articleId: form.articleId,
      categoryId: form.categoryId ?? null,
      title: form.title,
      summary: form.summary ?? null,
      coverUrl: form.coverUrl ?? null,
      contentMd: form.contentMd ?? null,
      articleType: form.articleType ?? null,
      attachments: form.attachments ?? null,
      tags: form.tags ?? '',
      publishStatus: form.publishStatus,
      articleSort: form.articleSort,
      status: form.status,
      remark: form.remark ?? null,
      softwareIds: Array.isArray(form.softwareIds) ? form.softwareIds : []
    }
    request(payload)
      .then((res) => {
        if (backToList) {
          window.location.assign('/kb/article')
          return
        }
        proxy.$modal.msgSuccess(res?.msg || '保存成功')
        const nextId = form.articleId || res?.data?.articleId
        if (!form.articleId && nextId) {
          form.articleId = Number(nextId)
          router
            .replace({ path: '/kb/article/edit', query: { articleId: form.articleId } })
            .catch(() => {})
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

watch(
  () => articleId.value,
  () => {
    Object.assign(form, defaultForm(), { articleId: articleId.value })
    loadDetail()
  },
  { immediate: true }
)
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
  flex-wrap: wrap;
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
  min-height: 360px;
  max-height: 560px;
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

.hint {
  margin-top: 6px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.soft-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.soft-option__name {
  font-weight: 650;
}

.soft-option__meta {
  font-size: 12px;
  color: var(--el-text-color-secondary);
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
.software-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 8px;
}

</style>\r\n
