<template>
  <div class="app-container">
    <el-card shadow="never" class="mb12 filter-card">
      <template #header>
        <div class="card-header">
          <div class="title">
            <span>筛选条件</span>
            <el-tag type="info" effect="plain" class="count-tag">{{ activeFilterCount }} 项</el-tag>
          </div>
          <div class="actions">
            <el-button text @click="toggleFilter">
              <el-icon>
                <ArrowUp v-if="showSearch" />
                <ArrowDown v-else />
              </el-icon>
              {{ showSearch ? '收起' : '展开' }}
            </el-button>
          </div>
        </div>
      </template>

      <el-collapse-transition>
        <div v-show="showSearch" class="filter-body">
          <el-form :model="queryParams" ref="queryRef" :inline="true">
            <el-form-item label="关键词" prop="softwareName">
              <el-input
                v-model="queryParams.softwareName"
                placeholder="名称 / 描述 / 作者 / 标签..."
                clearable
                style="width: 200px"
                @keyup.enter="handleQuery"
              />
            </el-form-item>
            <el-form-item label="分类" prop="categoryId">
              <el-select v-model="queryParams.categoryId" placeholder="请选择分类" clearable style="width: 200px">
                <el-option v-for="c in categoryOptions" :key="c.categoryId" :label="c.categoryName" :value="c.categoryId" />
              </el-select>
            </el-form-item>
            <el-form-item label="发布状态" prop="publishStatus">
              <el-select v-model="queryParams.publishStatus" placeholder="请选择发布状态" clearable style="width: 200px">
                <el-option v-for="o in publishStatusOptions" :key="o.value" :label="o.label" :value="o.value" />
              </el-select>
            </el-form-item>
            <el-form-item label="状态" prop="status">
              <el-select v-model="queryParams.status" placeholder="软件状态" clearable style="width: 200px">
                <el-option v-for="dict in sys_normal_disable" :key="dict.value" :label="dict.label" :value="dict.value" />
              </el-select>
            </el-form-item>
            <el-form-item label="开源" prop="openSource">
              <el-select v-model="queryParams.openSource" placeholder="是否开源" clearable style="width: 200px">
                <el-option label="是" value="1" />
                <el-option label="否" value="0" />
              </el-select>
            </el-form-item>
            <el-form-item label="许可证" prop="license">
              <el-input v-model="queryParams.license" placeholder="MIT / Apache-2.0 ..." clearable style="width: 200px" />
            </el-form-item>
            <el-form-item label="标签" prop="tag">
              <el-input v-model="queryParams.tag" placeholder="例如：dev / note / cli" clearable style="width: 200px" />
            </el-form-item>
            <el-form-item label="平台" prop="platform">
              <el-select v-model="queryParams.platform" placeholder="存在下载配置" clearable style="width: 200px">
                <el-option v-for="p in platformOptions" :key="p.value" :label="p.label" :value="p.value" />
              </el-select>
            </el-form-item>
            <el-form-item label="作者" prop="author">
              <el-input v-model="queryParams.author" placeholder="作者/团队关键词" clearable style="width: 200px" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
              <el-button icon="Refresh" @click="resetQuery">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-collapse-transition>
    </el-card>

    <el-card shadow="never" class="mb12">
      <template #header>
        <div class="card-header">
          <div class="title">
            <span>软件列表</span>
            <el-tag type="info" effect="plain" class="count-tag">{{ total }} 条</el-tag>
            <span class="hint">选择一个软件后，下方展示详情</span>
            <el-tag v-if="!showListPanel" type="info" effect="plain">已收起</el-tag>
          </div>
          <div class="actions">
            <el-radio-group v-model="listViewMode" class="view-toggle">
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
            <el-button text @click="toggleListPanel">
              <el-icon>
                <ArrowUp v-if="showListPanel" />
                <ArrowDown v-else />
              </el-icon>
              {{ showListPanel ? '收起列表' : '展开列表' }}
            </el-button>
          </div>
        </div>
      </template>

      <el-collapse-transition>
        <div v-show="showListPanel">
          <el-table
            v-if="listViewMode === 'table'"
            ref="tableRef"
            v-loading="listLoading"
            :data="softwareList"
            highlight-current-row
            @row-click="handleRowClick"
          >
            <el-table-column label="软件ID" align="center" prop="softwareId" width="90" />
            <el-table-column label="软件名称" align="center" prop="softwareName" min-width="180" show-overflow-tooltip />
            <el-table-column label="分类" align="center" prop="categoryName" min-width="120" show-overflow-tooltip />
            <el-table-column label="开源" align="center" prop="openSource" width="90">
              <template #default="scope">
                <el-tag :type="scope.row.openSource === '1' ? 'success' : 'info'">
                  {{ scope.row.openSource === '1' ? '是' : '否' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="发布状态" align="center" prop="publishStatus" width="100">
              <template #default="scope">
                <el-tag :type="publishStatusTagType(scope.row.publishStatus)">
                  {{ publishStatusLabel(scope.row.publishStatus) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="许可证" align="center" prop="license" min-width="120" show-overflow-tooltip />
            <el-table-column label="标签" align="center" prop="tags" min-width="140" show-overflow-tooltip />
            <el-table-column label="作者/团队" align="center" min-width="140" show-overflow-tooltip>
              <template #default="scope">
                <span>{{ scope.row.author || scope.row.team || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column label="更新时间" align="center" prop="updateTime" width="160" />
          </el-table>

          <div v-else v-loading="listLoading" class="card-view">
            <el-empty v-if="!softwareList.length" description="暂无数据" />
            <div v-else class="card-grid">
              <el-card
                v-for="item in softwareList"
                :key="item.softwareId"
                class="software-pick-card"
                :class="{ 'is-active': String(selectedSoftwareId) === String(item.softwareId) }"
                shadow="hover"
                role="button"
                tabindex="0"
                @click="handleRowClick(item)"
                @keydown.enter.prevent="handleRowClick(item)"
                @keydown.space.prevent="handleRowClick(item)"
              >
                <template #header>
                  <div class="software-pick-header">
                    <div class="left">
                      <el-avatar class="icon" shape="square" :size="40" :src="item.iconUrl">
                        {{ (item.softwareName || '').slice(0, 1) }}
                      </el-avatar>
                      <div class="heading">
                        <div class="name" :title="item.softwareName">{{ item.softwareName || '-' }}</div>
                        <div class="meta">
                          <el-tag v-if="item.categoryName" size="small" effect="plain">{{ item.categoryName }}</el-tag>
                          <el-tag size="small" :type="item.openSource === '1' ? 'success' : 'info'" effect="plain">
                            {{ item.openSource === '1' ? '开源' : '闭源' }}
                          </el-tag>
                          <el-tag size="small" :type="publishStatusTagType(item.publishStatus)" effect="plain">
                            {{ publishStatusLabel(item.publishStatus) }}
                          </el-tag>
                        </div>
                      </div>
                    </div>
                    <div class="right">
                      <dict-tag :options="sys_normal_disable" :value="item.status" />
                    </div>
                  </div>
                </template>

                <div class="software-pick-body">
                  <div class="desc">
                    <span v-if="item.shortDesc">{{ item.shortDesc }}</span>
                    <span v-else class="muted">暂无简短描述</span>
                  </div>

                  <div v-if="tagList(item).length" class="tag-list">
                    <el-tag v-for="t in tagList(item).slice(0, 6)" :key="t" size="small" effect="plain">{{ t }}</el-tag>
                    <el-tag v-if="tagList(item).length > 6" size="small" type="info" effect="plain">
                      +{{ tagList(item).length - 6 }}
                    </el-tag>
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
        </div>
      </el-collapse-transition>
    </el-card>

    <el-card shadow="never" v-loading="detailLoading">
      <template #header>
        <div class="card-header">
          <span>软件详情</span>
          <div class="actions">
            <el-tag v-if="selectedSoftwareId" type="info" effect="plain">
              #{{ selectedSoftwareId }} {{ form.softwareName || '' }}
            </el-tag>
            <el-button icon="Refresh" :disabled="!selectedSoftwareId" @click="refreshDetail">刷新</el-button>
            <el-button
              v-if="!editMode"
              type="primary"
              icon="Edit"
              :disabled="!selectedSoftwareId"
              @click="startEdit"
              v-hasPermi="['tool:software:item:edit']"
            >
              编辑
            </el-button>
            <el-button
              v-if="editMode"
              type="success"
              icon="Check"
              :disabled="!selectedSoftwareId"
              @click="saveEdit"
              v-hasPermi="['tool:software:item:edit']"
            >
              保存
            </el-button>
            <el-button v-if="editMode" icon="Close" :disabled="!selectedSoftwareId" @click="cancelEdit">
              取消
            </el-button>
          </div>
        </div>
      </template>

      <el-empty v-if="!selectedSoftwareId" description="请先在上方列表选择一个软件" />

      <el-form v-else ref="softwareRef" :model="form" :rules="rules" label-width="110px">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="基本信息" name="basic">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="软件名称" prop="softwareName">
                  <el-input v-model="form.softwareName" placeholder="请输入软件名称" :disabled="!editMode" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="分类" prop="categoryId">
                  <el-select v-model="form.categoryId" placeholder="请选择分类" style="width: 100%" :disabled="!editMode">
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
                  <el-select v-model="form.publishStatus" placeholder="请选择发布状态" style="width: 100%" :disabled="!editMode">
                    <el-option v-for="o in publishStatusOptions" :key="o.value" :label="o.label" :value="o.value" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="状态" prop="status">
                  <el-radio-group v-model="form.status" :disabled="!editMode">
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
                  <el-input-number v-model="form.softwareSort" :min="0" controls-position="right" :disabled="!editMode" />
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item label="图标" prop="iconUrl">
              <ImageUpload v-model="form.iconUrl" :limit="1" :drag="false" :disabled="!editMode" />
            </el-form-item>
            <el-form-item label="简短描述" prop="shortDesc">
              <el-input
                v-model="form.shortDesc"
                type="textarea"
                :rows="3"
                placeholder="可选"
                :disabled="!editMode"
              />
            </el-form-item>
          </el-tab-pane>

          <el-tab-pane label="元信息" name="meta">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="开源" prop="openSource">
                  <el-switch v-model="form.openSource" active-value="1" inactive-value="0" :disabled="!editMode" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="许可证" prop="license">
                  <el-input v-model="form.license" placeholder="例如：MIT / Apache-2.0 / GPL-3.0" :disabled="!editMode" />
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item label="标签" prop="tags">
              <el-input v-model="form.tags" placeholder="逗号分隔，例如：dev,cli,tool" :disabled="!editMode" />
            </el-form-item>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="官网" prop="officialUrl">
                  <el-input v-model="form.officialUrl" placeholder="可选" :disabled="!editMode" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="仓库" prop="repoUrl">
                  <el-input v-model="form.repoUrl" placeholder="可选" :disabled="!editMode" />
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="作者" prop="author">
                  <el-input v-model="form.author" placeholder="可选" :disabled="!editMode" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="团队" prop="team">
                  <el-input v-model="form.team" placeholder="可选" :disabled="!editMode" />
                </el-form-item>
              </el-col>
            </el-row>
          </el-tab-pane>

          <el-tab-pane label="介绍（Markdown）" name="desc">
            <div v-if="editMode" class="md-editor">
              <el-row :gutter="12">
                <el-col :span="12">
                  <el-input
                    v-model="form.descriptionMd"
                    type="textarea"
                    :rows="18"
                    placeholder="支持 Markdown，左侧编辑，右侧预览"
                  />
                </el-col>
                <el-col :span="12">
                  <div class="md-preview">
                    <MarkdownPreview :content="form.descriptionMd || ''" />
                  </div>
                </el-col>
              </el-row>
            </div>
            <div v-else class="md-preview">
              <MarkdownPreview :content="form.descriptionMd || ''" />
            </div>
          </el-tab-pane>

          <el-tab-pane label="使用说明（Markdown）" name="usage">
            <div v-if="editMode" class="md-editor">
              <el-row :gutter="12">
                <el-col :span="12">
                  <el-input
                    v-model="form.usageMd"
                    type="textarea"
                    :rows="18"
                    placeholder="支持 Markdown，左侧编辑，右侧预览"
                  />
                </el-col>
                <el-col :span="12">
                  <div class="md-preview">
                    <MarkdownPreview :content="form.usageMd || ''" />
                  </div>
                </el-col>
              </el-row>
            </div>
            <div v-else class="md-preview">
              <MarkdownPreview :content="form.usageMd || ''" />
            </div>
          </el-tab-pane>

          <el-tab-pane label="多平台下载配置" name="downloads">
            <el-row class="mb8" v-if="editMode">
              <el-button type="primary" plain icon="Plus" @click="handleAddDownloadRow">新增下载</el-button>
            </el-row>
            <el-table :data="form.downloads || []" border>
              <el-table-column label="平台" prop="platform" width="140">
                <template #default="scope">
                  <el-select
                    v-model="scope.row.platform"
                    placeholder="平台"
                    clearable
                    style="width: 120px"
                    :disabled="!editMode"
                  >
                    <el-option v-for="p in platformOptions" :key="p.value" :label="p.label" :value="p.value" />
                  </el-select>
                </template>
              </el-table-column>
              <el-table-column label="下载地址" prop="downloadUrl" min-width="260">
                <template #default="scope">
                  <el-input v-model="scope.row.downloadUrl" placeholder="https://..." :disabled="!editMode" />
                </template>
              </el-table-column>
              <el-table-column label="版本" prop="version" width="120">
                <template #default="scope">
                  <el-input v-model="scope.row.version" placeholder="可选" :disabled="!editMode" />
                </template>
              </el-table-column>
              <el-table-column label="校验值" prop="checksum" width="160">
                <template #default="scope">
                  <el-input v-model="scope.row.checksum" placeholder="可选" :disabled="!editMode" />
                </template>
              </el-table-column>
              <el-table-column label="排序" prop="sort" width="110">
                <template #default="scope">
                  <el-input-number v-model="scope.row.sort" :min="0" controls-position="right" :disabled="!editMode" />
                </template>
              </el-table-column>
              <el-table-column label="备注" prop="remark" width="180">
                <template #default="scope">
                  <el-input v-model="scope.row.remark" placeholder="可选" :disabled="!editMode" />
                </template>
              </el-table-column>
              <el-table-column v-if="editMode" label="操作" width="90" align="center">
                <template #default="scope">
                  <el-button type="danger" link icon="Delete" @click="handleRemoveDownloadRow(scope.$index)">
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>

          <el-tab-pane label="资源（仅 URL）" name="resources">
            <el-row class="mb8" v-if="editMode">
              <el-button type="primary" plain icon="Plus" @click="handleAddResourceRow">新增资源</el-button>
            </el-row>
            <el-table :data="form.resources || []" border>
              <el-table-column label="类型" prop="resourceType" width="140">
                <template #default="scope">
                  <el-select
                    v-model="scope.row.resourceType"
                    placeholder="类型"
                    clearable
                    style="width: 120px"
                    :disabled="!editMode"
                  >
                    <el-option v-for="t in resourceTypeOptions" :key="t.value" :label="t.label" :value="t.value" />
                  </el-select>
                </template>
              </el-table-column>
              <el-table-column label="标题" prop="title" width="180">
                <template #default="scope">
                  <el-input v-model="scope.row.title" placeholder="可选" :disabled="!editMode" />
                </template>
              </el-table-column>
              <el-table-column label="URL" prop="resourceUrl" min-width="260">
                <template #default="scope">
                  <el-input v-model="scope.row.resourceUrl" placeholder="https://..." :disabled="!editMode" />
                </template>
              </el-table-column>
              <el-table-column label="排序" prop="sort" width="110">
                <template #default="scope">
                  <el-input-number v-model="scope.row.sort" :min="0" controls-position="right" :disabled="!editMode" />
                </template>
              </el-table-column>
              <el-table-column label="备注" prop="remark" width="180">
                <template #default="scope">
                  <el-input v-model="scope.row.remark" placeholder="可选" :disabled="!editMode" />
                </template>
              </el-table-column>
              <el-table-column v-if="editMode" label="操作" width="90" align="center">
                <template #default="scope">
                  <el-button type="danger" link icon="Delete" @click="handleRemoveResourceRow(scope.$index)">
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { listSoftwareCategoryOptions } from '@/api/tool/software/category'
import { getSoftwareItem, listSoftwareItem, updateSoftwareItem } from '@/api/tool/software/item'
import MarkdownPreview from '@/components/MarkdownPreview'

const { proxy } = getCurrentInstance()
const { sys_normal_disable } = proxy.useDict('sys_normal_disable')

const route = useRoute()

const showSearch = ref(true)

const queryRef = ref()
const softwareRef = ref()
const tableRef = ref()

const listLoading = ref(false)
const detailLoading = ref(false)

const listViewModeStorageKey = 'tool:software:detail:listViewMode'
const listPanelStorageKey = 'tool:software:detail:listPanelExpanded'
const listViewMode = ref('table')
const showListPanel = ref(true)

const softwareList = ref([])
const total = ref(0)
const categoryOptions = ref([])

const selectedSoftwareId = ref(undefined)
const editMode = ref(false)
const originalJson = ref('')

const routeSoftwareId = computed(() => {
  const raw = route.query?.softwareId
  const value = Array.isArray(raw) ? raw[0] : raw
  if (value === undefined || value === null) return undefined
  const str = String(value).trim()
  if (!str) return undefined
  if (/^\d+$/.test(str)) return Number(str)
  return str
})

function loadListViewMode() {
  try {
    const cached = localStorage.getItem(listViewModeStorageKey)
    listViewMode.value = cached === 'card' ? 'card' : 'table'
  } catch (e) {
    listViewMode.value = 'table'
  }
}

function loadListPanelExpanded() {
  try {
    const cached = localStorage.getItem(listPanelStorageKey)
    showListPanel.value = cached === '0' ? false : true
  } catch (e) {
    showListPanel.value = true
  }
}

watch(
  () => listViewMode.value,
  (val) => {
    try {
      localStorage.setItem(listViewModeStorageKey, val)
    } catch (e) {}
  }
)

watch(
  () => showListPanel.value,
  (val) => {
    try {
      localStorage.setItem(listPanelStorageKey, val ? '1' : '0')
    } catch (e) {}
  }
)

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

const activeTab = ref('basic')

const data = reactive({
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    softwareName: undefined,
    categoryId: undefined,
    publishStatus: undefined,
    status: undefined,
    openSource: undefined,
    license: undefined,
    tag: undefined,
    platform: undefined,
    author: undefined
  },
  form: {},
  rules: {
    softwareName: [{ required: true, message: '软件名称不能为空', trigger: 'blur' }],
    categoryId: [{ required: true, message: '分类不能为空', trigger: 'change' }],
    softwareSort: [{ required: true, message: '排序不能为空', trigger: 'blur' }]
  }
})

const { queryParams, form, rules } = toRefs(data)

const activeFilterCount = computed(() => {
  const q = queryParams.value
  const keys = ['softwareName', 'categoryId', 'publishStatus', 'status', 'openSource', 'license', 'tag', 'platform', 'author']
  return keys.filter((k) => {
    const v = q?.[k]
    if (v === undefined || v === null) return false
    const s = String(v).trim()
    return s.length > 0
  }).length
})

function toggleFilter() {
  showSearch.value = !showSearch.value
}

function toggleListPanel() {
  showListPanel.value = !showListPanel.value
}

function publishStatusLabel(value) {
  return publishStatusOptions.find((o) => o.value === value)?.label || '-'
}

function publishStatusTagType(value) {
  if (value === '1') return 'success'
  if (value === '2') return 'warning'
  return 'info'
}

function tagList(row) {
  const raw = row?.tags
  if (!raw) return []
  return String(raw)
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
}

function resetForm() {
  form.value = {
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

function isDirty() {
  if (!originalJson.value) return false
  try {
    return JSON.stringify(form.value) !== originalJson.value
  } catch (e) {
    return true
  }
}

function getCategoryOptions() {
  listSoftwareCategoryOptions().then((res) => {
    categoryOptions.value = res.data || []
  })
}

function getList() {
  listLoading.value = true
  listSoftwareItem(queryParams.value)
    .then((response) => {
      softwareList.value = response.rows || []
      total.value = response.total || 0
      listLoading.value = false

      if (selectedSoftwareId.value) return

      const rid = routeSoftwareId.value
      if (rid !== undefined) {
        const matched = softwareList.value.find((r) => String(r.softwareId) === String(rid))
        if (matched) {
          handleRowClick(matched)
          return
        }
        loadDetail(rid)
        return
      }

      if (softwareList.value.length) handleRowClick(softwareList.value[0])
    })
    .catch(() => {
      listLoading.value = false
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

function loadDetail(softwareId) {
  if (!softwareId) return
  detailLoading.value = true
  getSoftwareItem(softwareId)
    .then((response) => {
      resetForm()
      form.value = {
        ...form.value,
        ...response.data,
        downloads: response.data?.downloads || [],
        resources: response.data?.resources || []
      }
      selectedSoftwareId.value = softwareId
      editMode.value = false
      activeTab.value = 'basic'
      originalJson.value = JSON.stringify(form.value)
      detailLoading.value = false
    })
    .catch(() => {
      detailLoading.value = false
    })
}

function handleRowClick(row) {
  const nextId = row?.softwareId
  if (!nextId) return
  if (selectedSoftwareId.value === nextId) return

  const doSwitch = () => {
    selectedSoftwareId.value = nextId
    loadDetail(nextId)
    showSearch.value = false
    showListPanel.value = false
    nextTick(() => {
      try {
        tableRef.value?.setCurrentRow?.(row)
      } catch (e) {}
    })
  }

  if (editMode.value && isDirty()) {
    proxy.$modal
      .confirm('当前有未保存的修改，确定切换软件并放弃这些修改吗？')
      .then(() => doSwitch())
      .catch(() => {})
    return
  }

  doSwitch()
}

function refreshDetail() {
  if (!selectedSoftwareId.value) return
  if (editMode.value && isDirty()) {
    proxy.$modal
      .confirm('当前有未保存的修改，确定刷新并放弃这些修改吗？')
      .then(() => loadDetail(selectedSoftwareId.value))
      .catch(() => {})
    return
  }
  loadDetail(selectedSoftwareId.value)
}

function startEdit() {
  editMode.value = true
}

function cancelEdit() {
  if (!selectedSoftwareId.value) return
  if (!isDirty()) {
    editMode.value = false
    return
  }
  proxy.$modal
    .confirm('确认取消编辑并还原未保存的修改吗？')
    .then(() => loadDetail(selectedSoftwareId.value))
    .catch(() => {})
}

function validateDownloads() {
  if (!form.value.downloads || !form.value.downloads.length) return true
  for (const [index, d] of form.value.downloads.entries()) {
    if (!d.platform || !d.downloadUrl) {
      proxy.$modal.msgError(`第 ${index + 1} 行下载配置未填写完整（平台/下载地址必填）`)
      return false
    }
  }
  return true
}

function validateResources() {
  if (!form.value.resources || !form.value.resources.length) return true
  for (const [index, r] of form.value.resources.entries()) {
    if (!r.resourceType || !r.resourceUrl) {
      proxy.$modal.msgError(`第 ${index + 1} 行资源未填写完整（类型/URL必填）`)
      return false
    }
  }
  return true
}

function saveEdit() {
  if (!selectedSoftwareId.value) return
  softwareRef.value?.validate((valid) => {
    if (!valid) return
    if (!validateDownloads()) return
    if (!validateResources()) return

    updateSoftwareItem(form.value).then(() => {
      proxy.$modal.msgSuccess('更新成功')
      editMode.value = false
      getList()
      loadDetail(selectedSoftwareId.value)
    })
  })
}

function handleAddDownloadRow() {
  if (!form.value.downloads) form.value.downloads = []
  form.value.downloads.push({
    platform: undefined,
    downloadUrl: undefined,
    version: undefined,
    checksum: undefined,
    sort: 0,
    remark: undefined
  })
}

function handleRemoveDownloadRow(index) {
  form.value.downloads.splice(index, 1)
}

function handleAddResourceRow() {
  if (!form.value.resources) form.value.resources = []
  form.value.resources.push({
    resourceType: undefined,
    title: undefined,
    resourceUrl: undefined,
    sort: 0,
    remark: undefined
  })
}

function handleRemoveResourceRow(index) {
  form.value.resources.splice(index, 1)
}

resetForm()
loadListPanelExpanded()
loadListViewMode()
getCategoryOptions()
getList()
</script>

<style scoped>
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

.hint {
  color: var(--el-text-color-secondary);
  font-weight: 400;
}

.actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-card :deep(.el-card__body) {
  padding-top: 10px;
}

.filter-body {
  overflow: hidden;
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
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 12px;
}

.software-pick-card {
  cursor: pointer;
  transition: box-shadow 200ms ease, transform 200ms ease, border-color 200ms ease;
}

.software-pick-card:hover {
  transform: translateY(-2px);
}

.software-pick-card.is-active {
  border-color: var(--el-color-primary);
  box-shadow: var(--el-box-shadow-light);
}

.software-pick-card:focus {
  outline: 2px solid var(--el-color-primary);
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  .software-pick-card {
    transition: none;
  }
  .software-pick-card:hover {
    transform: none;
  }
}

.software-pick-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.software-pick-header .left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.software-pick-header .heading {
  min-width: 0;
}

.software-pick-header .name {
  font-weight: 600;
  line-height: 20px;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.software-pick-header .meta {
  margin-top: 6px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.software-pick-body {
  padding: 2px 2px 0;
}

.desc {
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

.tag-list {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.md-preview {
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
  padding: 10px 12px;
  min-height: 320px;
  max-height: 680px;
  overflow: auto;
}
</style>
