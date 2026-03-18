<template>
  <div class="page-stack">
    <el-card class="panel-card" shadow="never">
      <template #header>
        <div class="panel-header">
          <span>布局模式说明</span>
          <el-tag effect="plain">供后续项目复制</el-tag>
        </div>
      </template>

      <div class="layout-guide-grid">
        <article v-for="mode in modes" :key="mode.title" class="guide-card">
          <h3>{{ mode.title }}</h3>
          <p>{{ mode.description }}</p>
          <ul class="guide-points">
            <li v-for="point in mode.points" :key="point">{{ point }}</li>
          </ul>
        </article>
      </div>
    </el-card>

    <el-card class="panel-card" shadow="never">
      <template #header>
        <div class="panel-header">
          <span>布局设置能力</span>
          <el-tag type="primary" effect="plain">头像菜单可直达</el-tag>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="主题模式">深色 / 浅色</el-descriptions-item>
        <el-descriptions-item label="主题主色">Color Picker + 预设色</el-descriptions-item>
        <el-descriptions-item label="导航模式">左侧 / 混合 / 顶部</el-descriptions-item>
        <el-descriptions-item label="Header">固定开关</el-descriptions-item>
        <el-descriptions-item label="Tags View">开关 + 图标开关</el-descriptions-item>
        <el-descriptions-item label="页脚与标题">页脚显隐 + 动态标题</el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup>
const modes = [
  {
    title: '左侧菜单',
    description: '最接近传统后台布局，适合菜单层级比较深的系统。',
    points: ['侧边栏常驻', '顶部保留工具区', '适合表单和管理页面'],
  },
  {
    title: '混合菜单',
    description: '顶部切一级分组，左侧显示当前分组子菜单，适合中大型系统。',
    points: ['一级分类更清晰', '左右职责分离', '适合业务线较多时扩展'],
  },
  {
    title: '顶部菜单',
    description: '把导航收进顶部，适合内容更轻、展示感更强的后台。',
    points: ['视觉更开阔', '适合门户式后台', '便于品牌化设计'],
  },
]
</script>
