<template>
  <div class="page-grid">
    <section class="hero-panel">
      <div class="hero-copy">
        <span class="hero-eyebrow">RuoYi Admin Style Template</span>
        <h1>后台布局、主题与切换动画的独立母版</h1>
        <p>
          这里保留了你喜欢的那套后台气质：清爽的白色主题、克制的深色主题、点击触发的圆形切换动画，
          以及头像菜单里的布局设置能力。后续新项目可以直接从这里继续长。
        </p>

        <div class="hero-actions">
          <el-button type="primary" @click="$router.push('/theme-studio')">打开主题实验室</el-button>
          <el-button plain @click="$router.push('/layout-guide')">查看布局导览</el-button>
        </div>
      </div>

      <div class="hero-preview">
        <div v-for="card in quickCards" :key="card.title" class="mini-metric">
          <span>{{ card.title }}</span>
          <strong>{{ card.value }}</strong>
          <small>{{ card.detail }}</small>
        </div>
      </div>
    </section>

    <section class="stats-grid">
      <article v-for="item in stats" :key="item.label" class="metric-card">
        <div class="metric-card-top">
          <span class="metric-label">{{ item.label }}</span>
          <el-tag :type="item.tagType" effect="dark">{{ item.badge }}</el-tag>
        </div>
        <strong class="metric-value">{{ item.value }}</strong>
        <span class="metric-trend">{{ item.trend }}</span>
      </article>
    </section>

    <section class="content-grid">
      <el-card class="panel-card" shadow="never">
        <template #header>
          <div class="panel-header">
            <span>最近活动</span>
            <el-tag type="primary" effect="plain">模板演示</el-tag>
          </div>
        </template>

        <el-timeline>
          <el-timeline-item
            v-for="item in timelines"
            :key="item.title"
            :timestamp="item.time"
            :type="item.type"
          >
            <strong>{{ item.title }}</strong>
            <div class="panel-muted">{{ item.text }}</div>
          </el-timeline-item>
        </el-timeline>
      </el-card>

      <el-card class="panel-card" shadow="never">
        <template #header>
          <div class="panel-header">
            <span>示例数据表格</span>
            <el-button link type="primary">更多</el-button>
          </div>
        </template>

        <el-table :data="tableData" stripe>
          <el-table-column prop="name" label="页面" min-width="150" />
          <el-table-column prop="owner" label="负责人" width="120" />
          <el-table-column prop="status" label="状态" width="120">
            <template #default="{ row }">
              <el-tag :type="row.status === '完成' ? 'success' : 'warning'" effect="plain">
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="updatedAt" label="更新时间" width="150" />
        </el-table>
      </el-card>
    </section>
  </div>
</template>

<script setup>
const quickCards = [
  { title: '主题模式', value: '2 套', detail: '深色 / 浅色' },
  { title: '布局模式', value: '3 套', detail: '左侧 / 混合 / 顶部' },
  { title: '设置维度', value: '7 项', detail: '可本地持久化' },
]

const stats = [
  { label: '布局抽象度', value: '高', trend: '主题、颜色、菜单模式都已解耦', badge: 'Ready', tagType: 'success' },
  { label: '动画完成度', value: '100%', trend: '点击式 view transition 已接入', badge: 'Smooth', tagType: 'primary' },
  { label: '组件示例', value: '丰富', trend: '表格、表单、卡片和标签均可参考', badge: 'Showcase', tagType: 'info' },
]

const timelines = [
  { title: '布局模板拆分完成', text: '后端管理系统里好用的布局层已经抽成独立项目。', time: '今天 09:30', type: 'primary' },
  { title: '主题色联动可用', text: '主色切换会同时更新卡片、按钮和焦点状态。', time: '今天 10:10', type: 'success' },
  { title: '切换动画接入', text: '主题切换采用点击位置扩散的圆形遮罩动画。', time: '今天 10:40', type: 'warning' },
]

const tableData = [
  { name: '仪表盘', owner: '系统', status: '完成', updatedAt: '2026-03-18' },
  { name: '布局导览', owner: '设计', status: '完成', updatedAt: '2026-03-18' },
  { name: '组件展示', owner: '前端', status: '进行中', updatedAt: '2026-03-18' },
]
</script>
