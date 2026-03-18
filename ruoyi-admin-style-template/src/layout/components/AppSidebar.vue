<template>
  <aside class="sidebar-container">
    <button v-if="layoutStore.sidebarLogo" class="sidebar-logo" type="button" @click="router.push('/dashboard')">
      <span class="sidebar-logo-mark" />
      <div class="sidebar-logo-text">
        <strong>Admin Template</strong>
        <span>布局母版 · 样式参考</span>
      </div>
    </button>

    <div class="sidebar-scroll">
      <template v-if="layoutStore.navType === 1">
        <section v-for="group in navigationGroups" :key="group.key" class="sidebar-group">
          <header class="sidebar-group-title">
            <AppIcon :name="group.icon" />
            <span>{{ group.label }}</span>
          </header>

          <RouterLink
            v-for="item in group.items"
            :key="item.path"
            :to="item.path"
            class="sidebar-link"
            :class="{ active: route.path === item.path }"
            @click="handleNavigate"
          >
            <span class="sidebar-link-icon">
              <AppIcon :name="item.icon" />
            </span>
            <span class="sidebar-link-label">{{ item.title }}</span>
            <span class="sidebar-link-dot" />
          </RouterLink>
        </section>
      </template>

      <template v-else>
        <section v-for="group in mixSidebarGroups" :key="group.key" class="sidebar-group">
          <header class="sidebar-group-title sidebar-group-title--compact">
            <AppIcon :name="group.icon" />
            <span>{{ group.label }}</span>
            <small>{{ group.description }}</small>
          </header>

          <RouterLink
            v-for="item in group.items"
            :key="item.path"
            :to="item.path"
            class="sidebar-link"
            :class="{ active: route.path === item.path }"
            @click="handleNavigate"
          >
            <span class="sidebar-link-icon">
              <AppIcon :name="item.icon" />
            </span>
            <span class="sidebar-link-label">{{ item.title }}</span>
            <span class="sidebar-link-dot" />
          </RouterLink>
        </section>
      </template>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { navigationGroups } from '@/config/navigation'
import { useLayoutStore } from '@/stores/layout'
import AppIcon from '@/components/AppIcon.vue'

const route = useRoute()
const router = useRouter()
const layoutStore = useLayoutStore()

const mixSidebarGroups = computed(() =>
  navigationGroups.filter((group) => group.key === layoutStore.topGroup),
)

function handleNavigate() {
  if (layoutStore.device === 'mobile') {
    layoutStore.closeSidebar()
  }
}
</script>
