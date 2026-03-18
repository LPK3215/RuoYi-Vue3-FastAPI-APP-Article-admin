<template>
  <header class="navbar" :class="`nav${layoutStore.navType}`">
    <div class="navbar-left">
      <button
        v-if="layoutStore.navType !== 3"
        class="hamburger-container"
        type="button"
        aria-label="切换侧边栏"
        @click="layoutStore.toggleSidebar"
      >
        <AppIcon :name="layoutStore.sidebarOpened ? 'Fold' : 'Expand'" />
      </button>

      <div v-if="layoutStore.navType === 1" class="breadcrumb-container">
        <span class="crumb">布局模板</span>
        <span class="crumb-divider">/</span>
        <span class="crumb current">{{ route.meta?.title || '仪表盘' }}</span>
      </div>

      <nav v-else-if="layoutStore.navType === 2" class="topmenu-container" aria-label="顶层导航">
        <button
          v-for="group in navigationGroups"
          :key="group.key"
          type="button"
          class="topmenu-item"
          :class="{ active: layoutStore.topGroup === group.key }"
          @click="activateMixGroup(group.key)"
        >
          <AppIcon :name="group.icon" />
          <span>{{ group.label }}</span>
        </button>
      </nav>

      <div v-else class="topbar-container">
        <button class="navbar-brand" type="button" @click="router.push('/dashboard')">
          <span class="navbar-brand-mark" />
          <span>Admin Template</span>
        </button>

        <nav class="topbar-menu" aria-label="顶部菜单">
          <RouterLink
            v-for="item in flatNavigation"
            :key="item.path"
            :to="item.path"
            class="topmenu-item"
            :class="{ active: route.path === item.path }"
          >
            <AppIcon :name="item.icon" />
            <span>{{ item.title }}</span>
          </RouterLink>
        </nav>
      </div>
    </div>

    <div class="right-menu">
      <template v-if="layoutStore.device !== 'mobile'">
        <el-tooltip content="主题模式" effect="dark" placement="bottom">
          <button class="right-menu-item hover-effect theme-switch-wrapper" type="button" @click="toggleTheme">
            <AppIcon :name="layoutStore.isDark ? 'Sunny' : 'MoonNight'" />
          </button>
        </el-tooltip>
      </template>

      <el-dropdown class="avatar-container right-menu-item hover-effect" trigger="click" @command="handleCommand">
        <div class="avatar-wrapper">
          <el-avatar :size="30" class="user-avatar">管</el-avatar>
          <span class="user-nickname">管理员</span>
        </div>

        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">个人中心</el-dropdown-item>
            <el-dropdown-item command="setLayout">布局设置</el-dropdown-item>
            <el-dropdown-item divided command="logout">退出演示</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<script setup>
import { nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import { flatNavigation, getFirstRouteForGroup, navigationGroups } from '@/config/navigation'
import { useLayoutStore } from '@/stores/layout'
import { runThemeModeTransition } from '@/utils/view-transition'
import AppIcon from '@/components/AppIcon.vue'

const emit = defineEmits(['open-settings'])

const route = useRoute()
const router = useRouter()
const layoutStore = useLayoutStore()

async function toggleTheme(event) {
  const wasDark = layoutStore.isDark
  await runThemeModeTransition(event, wasDark, async () => {
    layoutStore.toggleTheme()
    await nextTick()
  })
}

function activateMixGroup(groupKey) {
  layoutStore.setTopGroup(groupKey)
  if (route.meta?.groupKey !== groupKey) {
    router.push(getFirstRouteForGroup(groupKey))
  }
}

function handleCommand(command) {
  if (command === 'profile') {
    router.push('/profile')
    return
  }

  if (command === 'setLayout') {
    emit('open-settings')
    return
  }

  if (command === 'logout') {
    ElMessage.success('这是样式模板项目，这里只做演示。')
  }
}
</script>
