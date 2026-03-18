<template>
  <div :class="wrapperClasses" class="app-wrapper" :style="{ '--current-color': layoutStore.themeColor }">
    <div
      v-if="layoutStore.device === 'mobile' && layoutStore.sidebarOpened && !layoutStore.sidebarHidden"
      class="drawer-bg"
      @click="layoutStore.closeSidebar"
    />

    <AppSidebar v-if="!layoutStore.sidebarHidden" />

    <div :class="{ hasTagsView: layoutStore.tagsView, sidebarHide: layoutStore.sidebarHidden }" class="main-container">
      <div :class="{ 'fixed-header': layoutStore.fixedHeader }">
        <AppNavbar @open-settings="layoutStore.openSettings" />
        <AppTagsView v-if="layoutStore.tagsView" />
      </div>

      <main class="app-main">
        <section class="app-page">
          <router-view />
        </section>

        <footer v-if="layoutStore.footerVisible" class="app-footer">
          {{ layoutStore.footerContent }}
        </footer>
      </main>

      <SettingsDrawer />
    </div>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useWindowSize } from '@vueuse/core'
import { useRoute } from 'vue-router'
import { useLayoutStore } from '@/stores/layout'
import AppNavbar from './components/AppNavbar.vue'
import AppSidebar from './components/AppSidebar.vue'
import AppTagsView from './components/AppTagsView.vue'
import SettingsDrawer from './components/SettingsDrawer.vue'

const WIDTH = 992

const route = useRoute()
const layoutStore = useLayoutStore()
const { width } = useWindowSize()

const wrapperClasses = computed(() => ({
  hideSidebar: !layoutStore.sidebarOpened,
  openSidebar: layoutStore.sidebarOpened,
  mobile: layoutStore.device === 'mobile',
}))

watch(
  width,
  (currentWidth) => {
    layoutStore.setDevice(currentWidth < WIDTH ? 'mobile' : 'desktop')
  },
  { immediate: true },
)

watch(
  () => route.fullPath,
  () => {
    layoutStore.addVisitedView(route)
    layoutStore.applyRouteTitle(route.meta?.title)
    if (route.meta?.groupKey) {
      layoutStore.setTopGroup(route.meta.groupKey)
    }
    if (layoutStore.device === 'mobile') {
      layoutStore.closeSidebar()
    }
  },
  { immediate: true },
)
</script>
