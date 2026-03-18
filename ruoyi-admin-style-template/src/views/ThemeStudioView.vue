<template>
  <div class="page-stack">
    <section class="theme-lab-grid">
      <el-card class="panel-card" shadow="never">
        <template #header>
          <div class="panel-header">
            <span>主题控制台</span>
            <el-tag type="primary" effect="dark">{{ layoutStore.isDark ? '深色模式' : '浅色模式' }}</el-tag>
          </div>
        </template>

        <div class="theme-inspect">
          <div class="theme-chip-row">
            <span class="theme-swatch" :style="{ background: layoutStore.themeColor }" />
            <strong>{{ layoutStore.themeColor }}</strong>
          </div>

          <p class="panel-muted">
            在头像菜单里打开“布局设置”，或者直接用右上角月亮 / 太阳按钮，就能观察整套主题系统怎么联动。
          </p>

          <div class="theme-action-row">
            <el-button type="primary">主按钮</el-button>
            <el-button plain>次按钮</el-button>
            <el-button text>文字按钮</el-button>
          </div>

          <el-alert
            title="这个页面用来观察主题色、深浅模式和 Element Plus 组件变量的联动。"
            type="success"
            :closable="false"
            show-icon
          />
        </div>
      </el-card>

      <el-card class="panel-card" shadow="never">
        <template #header>
          <div class="panel-header">
            <span>色彩层级</span>
            <el-button link type="primary">自动根据主色生成</el-button>
          </div>
        </template>

        <div class="color-ramp">
          <div v-for="item in ramp" :key="item.label" class="color-ramp-item">
            <div class="color-ramp-bar" :style="{ background: item.color }" />
            <span>{{ item.label }}</span>
            <small>{{ item.color }}</small>
          </div>
        </div>
      </el-card>
    </section>

    <el-card class="panel-card" shadow="never">
      <template #header>
        <div class="panel-header">
          <span>组件状态预览</span>
          <el-tag effect="plain">用于校验主题覆盖面</el-tag>
        </div>
      </template>

      <div class="component-preview-grid">
        <div class="preview-block">
          <span class="preview-label">进度</span>
          <el-progress :percentage="78" />
        </div>

        <div class="preview-block">
          <span class="preview-label">标签</span>
          <div class="tag-row">
            <el-tag>默认</el-tag>
            <el-tag type="success">成功</el-tag>
            <el-tag type="warning">警告</el-tag>
            <el-tag type="danger">危险</el-tag>
          </div>
        </div>

        <div class="preview-block">
          <span class="preview-label">输入区</span>
          <el-input placeholder="观察输入框在深浅模式下的表面层级" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { getDarkColor, getLightColor } from '@/utils/theme'
import { useLayoutStore } from '@/stores/layout'

const layoutStore = useLayoutStore()

const ramp = computed(() => [
  { label: '主色', color: layoutStore.themeColor },
  { label: '浅一级', color: getLightColor(layoutStore.themeColor, 0.2) },
  { label: '浅二级', color: getLightColor(layoutStore.themeColor, 0.5) },
  { label: '深一级', color: getDarkColor(layoutStore.themeColor, 0.15) },
  { label: '深二级', color: getDarkColor(layoutStore.themeColor, 0.35) },
])
</script>
