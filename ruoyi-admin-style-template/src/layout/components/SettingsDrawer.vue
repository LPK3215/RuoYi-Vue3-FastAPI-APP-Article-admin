<template>
  <el-drawer v-model="drawerVisible" :with-header="false" :lock-scroll="false" direction="rtl" size="320px">
    <div class="setting-drawer-title">
      <h3 class="drawer-title">菜单导航设置</h3>
    </div>

    <div class="nav-wrap">
      <el-tooltip content="左侧菜单" placement="bottom">
        <button
          type="button"
          class="layout-preview left"
          :class="{ activeItem: layoutStore.navType === 1 }"
          @click="layoutStore.setNavType(1)"
        >
          <b />
          <b />
        </button>
      </el-tooltip>

      <el-tooltip content="混合菜单" placement="bottom">
        <button
          type="button"
          class="layout-preview mix"
          :class="{ activeItem: layoutStore.navType === 2 }"
          @click="layoutStore.setNavType(2)"
        >
          <b />
          <b />
        </button>
      </el-tooltip>

      <el-tooltip content="顶部菜单" placement="bottom">
        <button
          type="button"
          class="layout-preview top"
          :class="{ activeItem: layoutStore.navType === 3 }"
          @click="layoutStore.setNavType(3)"
        >
          <b />
          <b />
        </button>
      </el-tooltip>
    </div>

    <div class="setting-drawer-title">
      <h3 class="drawer-title">主题风格设置</h3>
    </div>

    <div class="setting-drawer-block-checkbox">
      <button
        type="button"
        class="mode-preview theme-dark"
        :class="{ active: layoutStore.isDark }"
        @click="switchThemeMode(true, $event)"
      >
        <span class="mode-check">✓</span>
      </button>

      <button
        type="button"
        class="mode-preview theme-light"
        :class="{ active: !layoutStore.isDark }"
        @click="switchThemeMode(false, $event)"
      >
        <span class="mode-check">✓</span>
      </button>
    </div>

    <div class="drawer-item">
      <span>主题颜色</span>
      <span class="comp-style">
        <el-color-picker v-model="themeColor" :predefine="predefineColors" @change="layoutStore.setThemeColor" />
      </span>
    </div>

    <el-divider />

    <h3 class="drawer-title">系统布局配置</h3>

    <div class="drawer-item">
      <span>开启 Tags-Views</span>
      <span class="comp-style">
        <el-switch v-model="layoutStore.tagsView" />
      </span>
    </div>

    <div class="drawer-item">
      <span>显示页签图标</span>
      <span class="comp-style">
        <el-switch v-model="layoutStore.tagsIcon" :disabled="!layoutStore.tagsView" />
      </span>
    </div>

    <div class="drawer-item">
      <span>固定 Header</span>
      <span class="comp-style">
        <el-switch v-model="layoutStore.fixedHeader" />
      </span>
    </div>

    <div class="drawer-item">
      <span>显示 Logo</span>
      <span class="comp-style">
        <el-switch v-model="layoutStore.sidebarLogo" />
      </span>
    </div>

    <div class="drawer-item">
      <span>动态标题</span>
      <span class="comp-style">
        <el-switch v-model="layoutStore.dynamicTitle" @change="updateTitle" />
      </span>
    </div>

    <div class="drawer-item">
      <span>底部版权</span>
      <span class="comp-style">
        <el-switch v-model="layoutStore.footerVisible" />
      </span>
    </div>

    <el-divider />

    <div class="drawer-actions">
      <el-button type="primary" plain @click="saveSetting">保存配置</el-button>
      <el-button plain @click="resetSetting">重置配置</el-button>
    </div>
  </el-drawer>
</template>

<script setup>
import { computed, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { useRoute } from 'vue-router'
import { useLayoutStore } from '@/stores/layout'
import { runThemeModeTransition } from '@/utils/view-transition'

const route = useRoute()
const layoutStore = useLayoutStore()
const predefineColors = ['#0ea5e9', '#6366f1', '#22c55e', '#f97316', '#f59e0b', '#ef4444', '#14b8a6', '#a855f7']

const drawerVisible = computed({
  get: () => layoutStore.settingsVisible,
  set: (value) => {
    if (value) {
      layoutStore.openSettings()
    } else {
      layoutStore.closeSettings()
    }
  },
})

const themeColor = computed({
  get: () => layoutStore.themeColor,
  set: (value) => layoutStore.setThemeColor(value),
})

async function switchThemeMode(nextIsDark, event) {
  if (layoutStore.isDark === nextIsDark) return

  await runThemeModeTransition(event, layoutStore.isDark, async () => {
    layoutStore.setThemeMode(nextIsDark)
    await nextTick()
  })
}

function updateTitle() {
  layoutStore.applyRouteTitle(route.meta?.title)
}

function saveSetting() {
  layoutStore.persistLayout()
  ElMessage.success('布局配置已保存到本地。')
}

function resetSetting() {
  layoutStore.resetSettings()
  layoutStore.applyRouteTitle(route.meta?.title)
  ElMessage.success('模板配置已恢复默认值。')
}
</script>
