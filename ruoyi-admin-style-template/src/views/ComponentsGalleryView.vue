<template>
  <div class="page-stack">
    <el-card class="panel-card" shadow="never">
      <template #header>
        <div class="panel-header">
          <span>表单与筛选区域</span>
          <el-tag type="info" effect="plain">后台常用组合</el-tag>
        </div>
      </template>

      <el-form label-width="90px" class="gallery-form">
        <div class="gallery-form-row">
          <el-form-item label="关键词">
            <el-input placeholder="请输入组件名 / 功能名" />
          </el-form-item>

          <el-form-item label="分类">
            <el-select placeholder="请选择">
              <el-option label="表单" value="form" />
              <el-option label="表格" value="table" />
              <el-option label="反馈" value="feedback" />
            </el-select>
          </el-form-item>

          <el-form-item label="状态">
            <el-select placeholder="请选择">
              <el-option label="可用" value="ready" />
              <el-option label="草稿" value="draft" />
            </el-select>
          </el-form-item>
        </div>

        <div class="gallery-actions">
          <el-button type="primary">查询</el-button>
          <el-button>重置</el-button>
        </div>
      </el-form>
    </el-card>

    <el-card class="panel-card" shadow="never">
      <template #header>
        <div class="panel-header">
          <span>组件表格</span>
          <el-button link type="primary">新建示例</el-button>
        </div>
      </template>

      <el-table :data="items">
        <el-table-column prop="name" label="名称" min-width="180" />
        <el-table-column prop="scene" label="适用场景" min-width="200" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="row.status === '已接入' ? 'success' : 'warning'" effect="plain">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="140">
          <template #default>
            <el-button link type="primary">查看</el-button>
            <el-button link>复制</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
const items = [
  { name: '主题切换按钮', scene: '右上角工具区 / 顶栏', status: '已接入' },
  { name: '布局设置抽屉', scene: '头像菜单 -> 布局设置', status: '已接入' },
  { name: 'Tags View', scene: '多页面切换时保持上下文', status: '已接入' },
  { name: '混合菜单模式', scene: '功能较多的中后台系统', status: '已接入' },
]
</script>
