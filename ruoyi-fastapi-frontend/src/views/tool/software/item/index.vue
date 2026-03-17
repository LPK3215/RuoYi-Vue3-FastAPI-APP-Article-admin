<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
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
        <el-select
          v-model="queryParams.license"
          placeholder="MIT / Apache-2.0 ..."
          clearable
          filterable
          allow-create
          default-first-option
          style="width: 200px"
        >
          <el-option
            v-for="o in facets.licenses"
            :key="o.value"
            :label="`${o.value} (${o.count})`"
            :value="o.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="标签" prop="tag">
        <el-select
          v-model="queryParams.tag"
          placeholder="选择/输入 tag"
          clearable
          filterable
          allow-create
          default-first-option
          style="width: 200px"
        >
          <el-option
            v-for="o in facets.tags"
            :key="o.value"
            :label="`${o.value} (${o.count})`"
            :value="o.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="官网" prop="officialUrl">
        <el-input
          v-model="queryParams.officialUrl"
          placeholder="example.com / https://..."
          clearable
          style="width: 200px"
        />
      </el-form-item>
      <el-form-item label="仓库" prop="repoUrl">
        <el-input
          v-model="queryParams.repoUrl"
          placeholder="github.com / gitee.com ..."
          clearable
          style="width: 200px"
        />
      </el-form-item>
      <el-form-item label="平台" prop="platform">
        <el-select v-model="queryParams.platform" placeholder="存在下载配置" clearable style="width: 200px">
          <el-option v-for="p in platformOptions" :key="p.value" :label="p.label" :value="p.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="作者" prop="author">
        <el-input v-model="queryParams.author" placeholder="作者/团队关键词" clearable style="width: 200px" />
      </el-form-item>
      <el-form-item label="数据质量" prop="qualityPreset">
        <el-select
          v-model="qualityPreset"
          placeholder="快速筛选"
          clearable
          style="width: 200px"
          @change="applyQualityPreset"
        >
          <el-option v-for="o in qualityPresetOptions" :key="o.value" :label="o.label" :value="o.value" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8 software-toolbar">
      <el-col :span="1.5">
        <el-button type="primary" plain icon="Plus" @click="handleAdd" v-hasPermi="['tool:software:item:add']">
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
          v-hasPermi="['tool:software:item:edit']"
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
          v-hasPermi="['tool:software:item:remove']"
        >
          删除
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="info"
          plain
          icon="Upload"
          @click="handleImport"
          v-hasPermi="['tool:software:item:edit']"
        >
          导入
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="primary" plain icon="Monitor" @click="openLocalScan" v-hasPermi="['tool:software:item:edit']">
          扫描本机
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-dropdown
          :disabled="multiple || viewMode !== 'table'"
          @command="handleBatchPublishCommand"
          v-hasPermi="['tool:software:item:publish']"
        >
          <el-button type="primary" plain icon="Upload" :disabled="multiple || viewMode !== 'table'">
            批量状态
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="1">批量上架</el-dropdown-item>
              <el-dropdown-item command="2">批量下架</el-dropdown-item>
              <el-dropdown-item command="0">设为草稿</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="Folder"
          :disabled="multiple || viewMode !== 'table'"
          @click="openBatchMoveCategoryDialog"
          v-hasPermi="['tool:software:item:edit']"
        >
          批量分类
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-dropdown
          :disabled="multiple || viewMode !== 'table'"
          @command="openBatchTagsDialog"
          v-hasPermi="['tool:software:item:edit']"
        >
          <el-button type="primary" plain icon="PriceTag" :disabled="multiple || viewMode !== 'table'">
            标签治理
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="append">追加标签</el-dropdown-item>
              <el-dropdown-item command="remove">移除标签</el-dropdown-item>
              <el-dropdown-item command="replace">覆盖标签</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['tool:software:item:list']"
        >
          导出
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="info" plain icon="DataAnalysis" @click="openQualityDrawer" v-hasPermi="['tool:software:item:list']">
          质量中心
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

    <el-card shadow="never" class="software-list-card">
      <template #header>
        <div class="card-header">
          <div class="title">
            <span>软件列表</span>
            <el-tag type="info" effect="plain" class="count-tag">{{ total }} 条</el-tag>
          </div>
          <div class="actions">
            <el-button v-if="viewMode === 'card'" icon="Refresh" @click="getList">刷新</el-button>
          </div>
        </div>
      </template>

      <el-table
        v-if="viewMode === 'table'"
        v-loading="loading"
        :data="softwareList"
        @sort-change="handleSortChange"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column label="软件ID" align="center" prop="softwareId" width="90" sortable="custom" />
        <el-table-column label="软件名称" align="center" prop="softwareName" min-width="180" show-overflow-tooltip />
        <el-table-column label="分类" align="center" prop="categoryName" min-width="120" show-overflow-tooltip />
        <el-table-column label="开源" align="center" prop="openSource" width="90">
          <template #default="scope">
            <el-tag :type="scope.row.openSource === '1' ? 'success' : 'info'">
              {{ scope.row.openSource === '1' ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="许可证" align="center" prop="license" min-width="120" show-overflow-tooltip />
        <el-table-column label="标签" align="center" prop="tags" min-width="160">
          <template #default="scope">
            <div v-if="tagList(scope.row).length" class="table-tag-list">
              <el-tag v-for="t in tagList(scope.row).slice(0, 3)" :key="t" size="small" effect="plain">{{ t }}</el-tag>
              <el-tag v-if="tagList(scope.row).length > 3" size="small" type="info" effect="plain">
                +{{ tagList(scope.row).length - 3 }}
              </el-tag>
            </div>
            <span v-else class="muted">-</span>
          </template>
        </el-table-column>
        <el-table-column label="作者/团队" align="center" min-width="140" show-overflow-tooltip>
          <template #default="scope">
            <span>{{ scope.row.author || scope.row.team || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="发布状态" align="center" prop="publishStatus" width="100">
          <template #default="scope">
            <el-tag :type="publishStatusTagType(scope.row.publishStatus)">
              {{ publishStatusLabel(scope.row.publishStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" align="center" prop="status" width="90">
          <template #default="scope">
            <dict-tag :options="sys_normal_disable" :value="scope.row.status" />
          </template>
        </el-table-column>
        <el-table-column label="排序" align="center" prop="softwareSort" width="90" sortable="custom" />
        <el-table-column label="更新时间" align="center" prop="updateTime" width="180" sortable="custom">
          <template #default="scope">
            <span>{{ parseTime(scope.row.updateTime) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="320" align="center" class-name="small-padding fixed-width">
          <template #default="scope">
            <el-button link type="primary" icon="View" @click="goDetail(scope.row)">详情</el-button>
            <el-button
              link
              type="primary"
              icon="Edit"
              @click="handleUpdate(scope.row)"
              v-hasPermi="['tool:software:item:edit']"
            >
              修改
            </el-button>
            <el-button
              link
              type="primary"
              icon="Delete"
              @click="handleDelete(scope.row)"
              v-hasPermi="['tool:software:item:remove']"
            >
              删除
            </el-button>
            <el-button
              link
              type="primary"
              icon="Upload"
              v-hasPermi="['tool:software:item:publish']"
              @click="handlePublish(scope.row)"
            >
              {{ scope.row.publishStatus === '1' ? '下架' : '上架' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-else v-loading="loading" class="card-view">
        <el-empty v-if="!softwareList.length" description="暂无数据" />
        <div v-else class="card-grid">
          <el-card
            v-for="item in softwareList"
            :key="item.softwareId"
            class="software-card"
            shadow="hover"
            role="button"
            tabindex="0"
            @click="goDetail(item)"
            @keydown.enter.prevent="goDetail(item)"
            @keydown.space.prevent="goDetail(item)"
          >
            <template #header>
              <div class="software-card-header">
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

            <div class="software-card-body">
              <div class="desc">
                <span v-if="item.shortDesc">{{ item.shortDesc }}</span>
                <span v-else class="muted">暂无简短描述</span>
              </div>

              <div class="kv">
                <div class="kv-item">
                  <span class="k">许可证</span>
                  <span class="v">{{ item.license || '-' }}</span>
                </div>
                <div class="kv-item">
                  <span class="k">作者/团队</span>
                  <span class="v">{{ item.author || item.team || '-' }}</span>
                </div>
              </div>

              <div v-if="tagList(item).length" class="tag-list">
                <el-tag v-for="t in tagList(item).slice(0, 6)" :key="t" size="small" effect="plain">{{ t }}</el-tag>
                <el-tag v-if="tagList(item).length > 6" size="small" type="info" effect="plain">
                  +{{ tagList(item).length - 6 }}
                </el-tag>
              </div>

              <div class="links" v-if="item.officialUrl || item.repoUrl">
                <el-link
                  v-if="item.officialUrl"
                  :href="item.officialUrl"
                  target="_blank"
                  rel="noopener noreferrer"
                  underline="never"
                  @click.stop
                >
                  官网
                </el-link>
                <el-link
                  v-if="item.repoUrl"
                  :href="item.repoUrl"
                  target="_blank"
                  rel="noopener noreferrer"
                  underline="never"
                  @click.stop
                >
                  仓库
                </el-link>
              </div>
            </div>

            <div class="software-card-actions">
              <el-button link type="primary" icon="View" @click.stop="goDetail(item)">详情</el-button>
              <el-button
                link
                type="primary"
                icon="Edit"
                @click.stop="handleUpdate(item)"
                v-hasPermi="['tool:software:item:edit']"
              >
                编辑
              </el-button>
              <el-button
                link
                type="primary"
                icon="Upload"
                v-hasPermi="['tool:software:item:publish']"
                @click.stop="handlePublish(item)"
              >
                {{ item.publishStatus === '1' ? '下架' : '上架' }}
              </el-button>
              <el-button
                link
                type="danger"
                icon="Delete"
                @click.stop="handleDelete(item)"
                v-hasPermi="['tool:software:item:remove']"
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

    <!-- 添加或修改软件对话框 -->
    <el-dialog :title="title" v-model="open" width="980px" append-to-body>
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
          <el-input v-model="form.shortDesc" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="可选：一句话描述" />
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
                  <MarkdownRender :content="form.descriptionMd || ''" />
                </div>
              </el-col>
            </el-row>
          </el-tab-pane>
          <el-tab-pane label="使用说明（Markdown）" name="usage">
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
                  <MarkdownRender :content="form.usageMd || ''" />
                </div>
              </el-col>
            </el-row>
          </el-tab-pane>
        </el-tabs>

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

      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 软件导入对话框 -->
    <el-dialog :title="upload.title" v-model="upload.open" width="420px" append-to-body>
      <el-upload
        ref="uploadRef"
        :limit="1"
        accept=".xlsx, .xls"
        :headers="upload.headers"
        :action="upload.url + '?updateSupport=' + upload.updateSupport"
        :disabled="upload.isUploading"
        :on-progress="handleFileUploadProgress"
        :on-success="handleFileSuccess"
        :on-change="handleFileChange"
        :on-remove="handleFileRemove"
        :auto-upload="false"
        drag
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <template #tip>
          <div class="el-upload__tip text-center">
            <div class="el-upload__tip">
              <el-checkbox v-model="upload.updateSupport" />是否更新已存在的软件（按软件ID匹配）
            </div>
            <span>仅允许导入 xls、xlsx 格式文件。</span>
            <el-link
              type="primary"
              :underline="false"
              style="font-size: 12px; vertical-align: baseline"
              @click="importTemplate"
            >
              下载模板
            </el-link>
          </div>
        </template>
      </el-upload>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitFileForm">确 定</el-button>
          <el-button @click="upload.open = false">取 消</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 批量移动分类 -->
    <el-dialog title="批量移动分类" v-model="batchCategory.open" width="440px" append-to-body>
      <el-form label-width="90px">
        <el-form-item label="目标分类">
          <el-select
            v-model="batchCategory.categoryId"
            placeholder="请选择分类"
            filterable
            clearable
            style="width: 100%"
          >
            <el-option v-for="c in categoryOptions" :key="c.categoryId" :label="c.categoryName" :value="c.categoryId" />
          </el-select>
        </el-form-item>
        <el-alert type="info" :closable="false" show-icon>
          将把选中的 {{ ids.length }} 条软件移动到目标分类
        </el-alert>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" :loading="batchCategory.loading" @click="submitBatchMoveCategory">确 定</el-button>
          <el-button @click="batchCategory.open = false">取 消</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 批量标签治理 -->
    <el-dialog title="批量标签治理" v-model="batchTags.open" width="560px" append-to-body>
      <el-form label-width="90px">
        <el-form-item label="操作">
          <el-radio-group v-model="batchTags.action">
            <el-radio-button label="append">追加</el-radio-button>
            <el-radio-button label="remove">移除</el-radio-button>
            <el-radio-button label="replace">覆盖</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="标签">
          <el-input
            v-model="batchTags.tags"
            type="textarea"
            :rows="4"
            placeholder="例如：cli, dev, note（支持逗号 / 换行 / 分号；自动去重与规范化）"
          />
        </el-form-item>
        <el-alert v-if="batchTags.action === 'replace'" type="warning" :closable="false" show-icon>
          覆盖模式允许留空，留空将清空选中软件的标签
        </el-alert>
        <el-alert v-else type="info" :closable="false" show-icon>
          将对选中的 {{ ids.length }} 条软件执行标签治理
        </el-alert>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" :loading="batchTags.loading" @click="submitBatchTags">确 定</el-button>
          <el-button @click="batchTags.open = false">取 消</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 数据质量中心（不改库：仅聚合统计 + 一键带筛选跳转） -->
    <el-drawer v-model="qualityDrawer.open" size="520px" append-to-body>
      <template #header>
        <div class="drawer-header">
          <div class="drawer-title">
            <span>数据质量中心</span>
            <el-tag effect="plain" type="info" size="small" class="drawer-tag">DeskOps</el-tag>
          </div>
          <el-button text icon="Refresh" :loading="qualityDrawer.loading" @click="loadQualityOverview">刷新</el-button>
        </div>
      </template>

      <div class="quality-drawer">
        <div class="quality-tip">
          点击卡片即可自动应用「数据质量筛选」，快速定位缺项并修复（可配合批量治理）。
        </div>

        <div class="quality-grid">
          <div
            v-for="item in qualityItems"
            :key="item.preset"
            class="quality-card"
            :class="{ 'is-zero': item.count === 0 }"
            role="button"
            tabindex="0"
            @click="item.count ? filterByQualityPreset(item.preset) : null"
            @keydown.enter.prevent="item.count ? filterByQualityPreset(item.preset) : null"
            @keydown.space.prevent="item.count ? filterByQualityPreset(item.preset) : null"
          >
            <div class="quality-card__label">{{ item.label }}</div>
            <div class="quality-card__count">
              <span v-if="qualityDrawer.loading">…</span>
              <span v-else>{{ item.count }}</span>
            </div>
            <div class="quality-card__hint">{{ item.count ? '点击筛选' : '已全部补齐' }}</div>
          </div>
        </div>
      </div>
    </el-drawer>
  </div>


    <!-- 本机软件扫描导入 -->
    <el-dialog title="本机软件扫描" v-model="localScan.open" width="920px" append-to-body>
      <div class="local-scan-toolbar">
        <el-input v-model="localScan.keyword" placeholder="搜索名称/发布者/版本" clearable style="width: 320px" @keyup.enter="runLocalScan" />
        <el-button type="primary" icon="Search" :loading="localScan.loading" @click="runLocalScan">扫描</el-button>
        <el-button icon="Refresh" :disabled="localScan.loading" @click="resetLocalScan">重置</el-button>
        <div class="local-scan-right">
          <el-select v-model="localScan.categoryId" placeholder="导入到分类" clearable filterable style="width: 220px">
            <el-option v-for="c in categoryOptions" :key="c.categoryId" :label="c.categoryName" :value="c.categoryId" />
          </el-select>
          <el-checkbox v-model="localScan.updateSupport">同名更新</el-checkbox>
          <el-checkbox v-model="localScan.overwrite">覆盖字段</el-checkbox>
          <el-button type="success" icon="Plus" :disabled="!localScan.selectedIds.length" :loading="localScan.importing" @click="submitLocalImport">
            导入选中（{{ localScan.selectedIds.length }}）
          </el-button>
        </div>
      </div>

      <el-alert
        type="info"
        show-icon
        :closable="false"
        title="说明"
        description="从 Windows 注册表读取已安装软件，导入时按‘软件名称’匹配：同名存在则跳过或更新；默认导入到‘本机导入’分类。"
        style="margin-bottom: 10px"
      />

      <el-table
        v-loading="localScan.loading"
        :data="localScan.rows"
        height="520"
        border
        @selection-change="onLocalScanSelection"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column label="名称" prop="name" min-width="240" show-overflow-tooltip />
        <el-table-column label="版本" prop="version" width="140" show-overflow-tooltip />
        <el-table-column label="发布者" prop="publisher" min-width="180" show-overflow-tooltip />
        <el-table-column label="安装路径" prop="installLocation" min-width="240" show-overflow-tooltip />
        <el-table-column label="链接" prop="url" min-width="220" show-overflow-tooltip />
      </el-table>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="localScan.open=false">关 闭</el-button>
        </div>
      </template>
    </el-dialog>

</template>

<script setup name="SoftwareItem">
import { MarkdownRender } from 'markstream-vue'
import 'markstream-vue/index.css'

import { getToken } from '@/utils/auth'
import { listSoftwareCategoryOptions } from '@/api/tool/software/category'
import {
  addSoftwareItem,
  batchChangeSoftwarePublishStatus,
  getSoftwareItemFacets,
  batchManageSoftwareTags,
  batchMoveSoftwareCategory,
  changeSoftwarePublishStatus,
  delSoftwareItem,
  getSoftwareItem,
  listSoftwareItem,
  updateSoftwareItem
} from '@/api/tool/software/item'
import { scanLocalSoftware, importLocalSoftware } from '@/api/tool/software/scan'
import { getSoftwareDashboardOverview } from '@/api/tool/software/dashboard'

const { proxy } = getCurrentInstance()
const { sys_normal_disable } = proxy.useDict('sys_normal_disable')

const softwareList = ref([])
const categoryOptions = ref([])
const open = ref(false)
const loading = ref(true)
const showSearch = ref(true)
const ids = ref([])
const single = ref(true)
const multiple = ref(true)
const total = ref(0)
const title = ref('')
const activeMdTab = ref('desc')

const router = useRouter()
const route = useRoute()

const viewModeStorageKey = 'tool:software:item:viewMode'
const viewMode = ref('table')

const facets = reactive({
  tags: [],
  licenses: [],
  authors: [],
  teams: [],
  platforms: []
})

const qualityPreset = ref(undefined)
const qualityPresetOptions = [
  { label: '缺下载配置', value: 'missingDownloads' },
  { label: '缺许可证', value: 'missingLicense' },
  { label: '缺图标', value: 'missingIcon' },
  { label: '缺官网地址', value: 'missingOfficialUrl' },
  { label: '缺简短描述', value: 'missingShortDesc' },
  { label: '缺标签', value: 'missingTags' },
  { label: '缺资源配置', value: 'missingResources' }
]

function loadViewMode() {
  try {
    const cached = localStorage.getItem(viewModeStorageKey)
    viewMode.value = cached === 'card' ? 'card' : 'table'
  } catch (e) {
    viewMode.value = 'table'
  }
}

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

/*** 软件导入参数 */
const upload = reactive({
  open: false,
  title: '',
  isUploading: false,
  updateSupport: 0,
  selectedFile: null,
  headers: { Authorization: 'Bearer ' + getToken() },
  url: import.meta.env.VITE_APP_BASE_API + '/tool/software/item/importData'
})



const localScan = reactive({
  open: false,
  loading: false,
  importing: false,
  keyword: '',
  rows: [],
  selectedIds: [],
  categoryId: undefined,
  updateSupport: false,
  overwrite: false
})

function openLocalScan() {
  localScan.open = true
  if (!localScan.rows.length) {
    runLocalScan()
  }
}

function resetLocalScan() {
  localScan.keyword = ''
  localScan.rows = []
  localScan.selectedIds = []
}

function onLocalScanSelection(selection) {
  localScan.selectedIds = (selection || []).map((x) => x.id)
}

function runLocalScan() {
  localScan.loading = true
  scanLocalSoftware({ keyword: localScan.keyword || undefined, limit: 1000 })
    .then((res) => {
      localScan.rows = res.data || []
      localScan.selectedIds = []
    })
    .catch(() => {})
    .finally(() => {
      localScan.loading = false
    })
}

function submitLocalImport() {
  if (!localScan.selectedIds.length) return
  localScan.importing = true
  importLocalSoftware({
    ids: localScan.selectedIds,
    categoryId: localScan.categoryId,
    updateSupport: Boolean(localScan.updateSupport),
    overwrite: Boolean(localScan.overwrite)
  })
    .then((res) => {
      const r = res.data || {}
      proxy.$modal.msgSuccess(`导入完成：新增 ${r.created || 0}，更新 ${r.updated || 0}，跳过 ${r.skipped || 0}，失败 ${r.errors || 0}`)
      localScan.open = false
      getList()
    })
    .catch(() => {})
    .finally(() => {
      localScan.importing = false
    })
}
const batchCategory = reactive({
  open: false,
  loading: false,
  categoryId: undefined
})

const batchTags = reactive({
  open: false,
  loading: false,
  action: 'append',
  tags: ''
})

const qualityDrawer = reactive({
  open: false,
  loading: false
})

const qualityStats = reactive({
  missingIcon: 0,
  missingLicense: 0,
  missingOfficialUrl: 0,
  missingShortDesc: 0,
  missingTags: 0,
  missingDownloads: 0,
  missingResources: 0
})

const qualityItems = computed(() => [
  { label: '缺下载配置', preset: 'missingDownloads', count: Number(qualityStats.missingDownloads || 0) },
  { label: '缺许可证', preset: 'missingLicense', count: Number(qualityStats.missingLicense || 0) },
  { label: '缺图标', preset: 'missingIcon', count: Number(qualityStats.missingIcon || 0) },
  { label: '缺官网地址', preset: 'missingOfficialUrl', count: Number(qualityStats.missingOfficialUrl || 0) },
  { label: '缺简短描述', preset: 'missingShortDesc', count: Number(qualityStats.missingShortDesc || 0) },
  { label: '缺标签', preset: 'missingTags', count: Number(qualityStats.missingTags || 0) },
  { label: '缺资源配置', preset: 'missingResources', count: Number(qualityStats.missingResources || 0) }
])

const formTagsList = computed({
  get: () => splitTags(form.value?.tags || ''),
  set: (arr) => {
    const next = splitTags((arr || []).join(','))
    form.value.tags = next.length ? next.join(',') : undefined
  }
})

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    orderByColumn: undefined,
    isAsc: undefined,
    softwareName: undefined,
    categoryId: undefined,
    publishStatus: undefined,
    status: undefined,
    openSource: undefined,
    license: undefined,
    tag: undefined,
    officialUrl: undefined,
    repoUrl: undefined,
    platform: undefined,
    author: undefined,
    hasIcon: undefined,
    hasLicense: undefined,
    hasOfficialUrl: undefined,
    hasShortDesc: undefined,
    hasTags: undefined,
    hasDownloads: undefined,
    hasResources: undefined
  },
  rules: {
    softwareName: [{ required: true, message: '软件名称不能为空', trigger: 'blur' }],
    categoryId: [{ required: true, message: '分类不能为空', trigger: 'change' }],
    softwareSort: [{ required: true, message: '排序不能为空', trigger: 'blur' }]
  }
})

const { queryParams, form, rules } = toRefs(data)

function clearQualityFlags() {
  queryParams.value.hasDownloads = undefined
  queryParams.value.hasLicense = undefined
  queryParams.value.hasIcon = undefined
  queryParams.value.hasOfficialUrl = undefined
  queryParams.value.hasShortDesc = undefined
  queryParams.value.hasTags = undefined
  queryParams.value.hasResources = undefined
}

function applyQualityPreset(val) {
  clearQualityFlags()
  if (!val) return
  if (val === 'missingDownloads') queryParams.value.hasDownloads = '0'
  if (val === 'missingLicense') queryParams.value.hasLicense = '0'
  if (val === 'missingIcon') queryParams.value.hasIcon = '0'
  if (val === 'missingOfficialUrl') queryParams.value.hasOfficialUrl = '0'
  if (val === 'missingShortDesc') queryParams.value.hasShortDesc = '0'
  if (val === 'missingTags') queryParams.value.hasTags = '0'
  if (val === 'missingResources') queryParams.value.hasResources = '0'
}

function filterByQualityPreset(preset) {
  if (!preset) return
  qualityPreset.value = preset
  applyQualityPreset(preset)
  qualityDrawer.open = false
  handleQuery()
}

function syncQualityPresetFromQuery() {
  const miss = []
  if (queryParams.value.hasDownloads === '0') miss.push('missingDownloads')
  if (queryParams.value.hasLicense === '0') miss.push('missingLicense')
  if (queryParams.value.hasIcon === '0') miss.push('missingIcon')
  if (queryParams.value.hasOfficialUrl === '0') miss.push('missingOfficialUrl')
  if (queryParams.value.hasShortDesc === '0') miss.push('missingShortDesc')
  if (queryParams.value.hasTags === '0') miss.push('missingTags')
  if (queryParams.value.hasResources === '0') miss.push('missingResources')
  qualityPreset.value = miss.length === 1 ? miss[0] : undefined
}

function applyRouteQuery() {
  const q = route.query || {}
  const keys = [
    'softwareName',
    'categoryId',
    'publishStatus',
    'status',
    'openSource',
    'license',
    'tag',
    'officialUrl',
    'repoUrl',
    'platform',
    'author',
    'hasIcon',
    'hasLicense',
    'hasOfficialUrl',
    'hasShortDesc',
    'hasTags',
    'hasDownloads',
    'hasResources'
  ]

  let touched = false
  for (const key of keys) {
    if (q[key] === undefined) continue
    const raw = q[key]
    queryParams.value[key] = Array.isArray(raw) ? raw[0] : raw
    touched = true
  }

  if (touched) {
    syncQualityPresetFromQuery()
  }
}

function publishStatusLabel(value) {
  return publishStatusOptions.find((o) => o.value === value)?.label || '-'
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
  batchCategory.open = false
  batchCategory.categoryId = undefined
  batchTags.open = false
  batchTags.tags = ''
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

function goDetail(row) {
  const softwareId = row?.softwareId
  if (!softwareId) return
  router.push({ path: '/software/detail', query: { softwareId } })
}

function tagList(row) {
  return splitTags(row?.tags || '')
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

function getList() {
  loading.value = true
  listSoftwareItem(queryParams.value).then((response) => {
    softwareList.value = response.rows || []
    total.value = response.total || 0
    loading.value = false
  })
}

function openQualityDrawer() {
  qualityDrawer.open = true
  loadQualityOverview()
}

function loadQualityOverview() {
  qualityDrawer.loading = true
  getSoftwareDashboardOverview({ limit: 12, recentLimit: 6 })
    .then((res) => {
      const q = res.data?.quality || {}
      qualityStats.missingDownloads = q.missingDownloads || 0
      qualityStats.missingLicense = q.missingLicense || 0
      qualityStats.missingIcon = q.missingIcon || 0
      qualityStats.missingOfficialUrl = q.missingOfficialUrl || 0
      qualityStats.missingShortDesc = q.missingShortDesc || 0
      qualityStats.missingTags = q.missingTags || 0
      qualityStats.missingResources = q.missingResources || 0
    })
    .catch(() => {})
    .finally(() => {
      qualityDrawer.loading = false
    })
}

function handleSortChange({ prop, order }) {
  if (!prop || !order) {
    queryParams.value.orderByColumn = undefined
    queryParams.value.isAsc = undefined
  } else {
    queryParams.value.orderByColumn = prop
    queryParams.value.isAsc = order
  }
  handleQuery()
}

function cancel() {
  open.value = false
  reset()
}

function reset() {
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
  activeMdTab.value = 'desc'
  proxy.resetForm('softwareRef')
}

function handleQuery() {
  queryParams.value.pageNum = 1
  getList()
}

function resetQuery() {
  qualityPreset.value = undefined
  proxy.resetForm('queryRef')
  handleQuery()
}

function handleSelectionChange(selection) {
  ids.value = selection.map((item) => item.softwareId)
  single.value = selection.length !== 1
  multiple.value = !selection.length
}

function handleAdd() {
  reset()
  open.value = true
  title.value = '新增软件'
}

function handleUpdate(row) {
  reset()
  const softwareId = row?.softwareId || ids.value[0]
  getSoftwareItem(softwareId).then((response) => {
    form.value = {
      ...form.value,
      ...response.data,
      downloads: response.data?.downloads || [],
      resources: response.data?.resources || []
    }
    open.value = true
    title.value = '修改软件'
  })
}

function handleDelete(row) {
  const softwareIds = row?.softwareId || ids.value.join(',')
  proxy.$modal
    .confirm('是否确认删除软件编号为 "' + softwareIds + '" 的数据项？')
    .then(() => delSoftwareItem(softwareIds))
    .then(() => {
      getList()
      proxy.$modal.msgSuccess('删除成功')
    })
    .catch(() => {})
}

function handleBatchPublishCommand(command) {
  if (!ids.value?.length) return
  const label = command === '1' ? '上架' : command === '2' ? '下架' : '草稿'
  proxy.$modal
    .confirm(`是否确认将选中的 ${ids.value.length} 条软件设置为「${label}」？`)
    .then(() => batchChangeSoftwarePublishStatus({ softwareIds: ids.value, publishStatus: command }))
    .then(() => {
      proxy.$modal.msgSuccess('操作成功')
      clearSelection()
      getList()
    })
    .catch(() => {})
}

function openBatchMoveCategoryDialog() {
  if (!ids.value?.length) return
  batchCategory.categoryId = undefined
  batchCategory.open = true
}

function submitBatchMoveCategory() {
  if (!ids.value?.length) return
  if (!batchCategory.categoryId) {
    proxy.$modal.msgError('请选择目标分类')
    return
  }
  batchCategory.loading = true
  batchMoveSoftwareCategory({ softwareIds: ids.value, categoryId: batchCategory.categoryId })
    .then((res) => {
      proxy.$modal.msgSuccess(res?.msg || '操作成功')
      batchCategory.open = false
      clearSelection()
      getList()
    })
    .catch(() => {})
    .finally(() => {
      batchCategory.loading = false
    })
}

function openBatchTagsDialog(command) {
  if (!ids.value?.length) return
  batchTags.action = command || 'append'
  batchTags.tags = ''
  batchTags.open = true
}

function submitBatchTags() {
  if (!ids.value?.length) return
  const raw = String(batchTags.tags || '').trim()
  if ((batchTags.action === 'append' || batchTags.action === 'remove') && !raw) {
    proxy.$modal.msgError('请输入标签')
    return
  }
  batchTags.loading = true
  batchManageSoftwareTags({ softwareIds: ids.value, action: batchTags.action, tags: raw })
    .then((res) => {
      proxy.$modal.msgSuccess(res?.msg || '操作成功')
      batchTags.open = false
      clearSelection()
      getList()
    })
    .catch(() => {})
    .finally(() => {
      batchTags.loading = false
    })
}

function handleImport() {
  upload.title = '软件导入'
  upload.open = true
  upload.selectedFile = null
}

function importTemplate() {
  proxy.download(
    'tool/software/item/importTemplate',
    {},
    `software_import_template_${new Date().getTime()}.xlsx`
  )
}

const handleFileUploadProgress = () => {
  upload.isUploading = true
}

const handleFileChange = (file) => {
  upload.selectedFile = file
}

const handleFileRemove = () => {
  upload.selectedFile = null
}

const handleFileSuccess = (response, file) => {
  upload.open = false
  upload.isUploading = false
  proxy.$refs['uploadRef'].handleRemove(file)
  proxy.$alert(
    "<div style='overflow:auto;overflow-x:hidden;max-height:70vh;padding:10px 20px 0;'>" +
      response.msg +
      '</div>',
    '导入结果',
    { dangerouslyUseHTMLString: true }
  )
  getList()
}

function submitFileForm() {
  const file = upload.selectedFile
  if (
    !file ||
    file.length === 0 ||
    (!file.name.toLowerCase().endsWith('.xls') && !file.name.toLowerCase().endsWith('.xlsx'))
  ) {
    proxy.$modal.msgError('请选择后缀为 “xls”或“xlsx”的文件。')
    return
  }
  proxy.$refs['uploadRef'].submit()
}

function handleExport() {
  proxy.download(
    'tool/software/item/export',
    {
      ...queryParams.value
    },
    `software_items_${new Date().getTime()}.xlsx`
  )
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

function submitForm() {
  proxy.$refs['softwareRef'].validate((valid) => {
    if (!valid) return
    if (!validateDownloads()) return
    if (!validateResources()) return
    const request = form.value.softwareId ? updateSoftwareItem : addSoftwareItem
    request(form.value).then(() => {
      proxy.$modal.msgSuccess('操作成功')
      open.value = false
      getList()
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

function handlePublish(row) {
  const next = row.publishStatus === '1' ? '2' : '1'
  const text = next === '1' ? '上架' : '下架'
  proxy.$modal
    .confirm(`确认要${text}【${row.softwareName}】吗？`)
    .then(() => changeSoftwarePublishStatus({ softwareId: row.softwareId, publishStatus: next }))
    .then(() => {
      proxy.$modal.msgSuccess('操作成功')
      getList()
    })
    .catch(() => {})
}

getCategoryOptions()
getFacets()
loadViewMode()
applyRouteQuery()
getList()
</script>

<style scoped>
.software-toolbar {
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

.software-list-card :deep(.el-card__body) {
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

.actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.card-view {
  min-height: 240px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 12px;
}

.software-card {
  cursor: pointer;
  transition: box-shadow 200ms ease, transform 200ms ease;
}

.software-card:hover {
  transform: translateY(-2px);
}

.software-card:focus {
  outline: 2px solid var(--el-color-primary);
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  .software-card {
    transition: none;
  }
  .software-card:hover {
    transform: none;
  }
}

.software-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.software-card-header .left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.software-card-header .heading {
  min-width: 0;
}

.software-card-header .name {
  font-weight: 600;
  line-height: 20px;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.software-card-header .meta {
  margin-top: 6px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.software-card-body {
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

.kv {
  margin-top: 10px;
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
}

.kv-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
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

.tag-list {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.table-tag-list {
  display: inline-flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 6px;
}

.links {
  margin-top: 10px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.drawer-header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.drawer-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
}

.drawer-tag {
  font-weight: 600;
}

.quality-drawer {
  padding: 6px 4px 10px;
}

.quality-tip {
  color: var(--el-text-color-secondary);
  line-height: 20px;
}

.quality-grid {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.quality-card {
  border: 1px solid var(--app-border);
  background: color-mix(in srgb, var(--app-surface) 86%, transparent);
  border-radius: 16px;
  padding: 12px 12px 10px;
  cursor: pointer;
  transition: transform 140ms ease, box-shadow 140ms ease, border-color 140ms ease, background 140ms ease;
}

.quality-card:hover,
.quality-card:focus {
  transform: translateY(-1px);
  box-shadow: var(--app-shadow);
  border-color: color-mix(in srgb, var(--el-color-primary) 30%, var(--app-border));
  background: color-mix(in srgb, var(--app-surface) 92%, transparent);
  outline: none;
}

.quality-card.is-zero {
  opacity: 0.55;
  cursor: default;
  box-shadow: none;
  transform: none;
}

.quality-card__label {
  font-weight: 650;
  color: var(--el-text-color-primary);
}

.quality-card__count {
  margin-top: 6px;
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.quality-card__hint {
  margin-top: 2px;
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

.software-card-actions {
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid var(--el-border-color-lighter);
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.md-preview {
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
  padding: 10px 12px;
  min-height: 320px;
  max-height: 520px;
  overflow: auto;
}


.local-scan-toolbar {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.local-scan-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}


</style>


