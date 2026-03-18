<template>
  <div class="tags-view-container">
    <div class="tags-view-wrapper">
      <RouterLink
        v-for="tag in layoutStore.visitedViews"
        :key="tag.path"
        :to="tag.path"
        class="tags-view-item"
        :class="{ active: route.path === tag.path, 'has-icon': layoutStore.tagsIcon }"
      >
        <AppIcon v-if="layoutStore.tagsIcon && tag.icon" :name="tag.icon" />
        <span>{{ tag.title }}</span>
        <button
          v-if="!tag.affix"
          type="button"
          class="tags-view-close"
          aria-label="关闭标签"
          @click.prevent.stop="closeTag(tag.path)"
        >
          ×
        </button>
      </RouterLink>
    </div>

    <button
      v-if="layoutStore.visitedViews.length > 1"
      type="button"
      class="tags-view-action"
      @click="closeOthers"
    >
      收起其他
    </button>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useLayoutStore } from '@/stores/layout'
import AppIcon from '@/components/AppIcon.vue'

const route = useRoute()
const router = useRouter()
const layoutStore = useLayoutStore()

function closeTag(path) {
  layoutStore.removeVisitedView(path)
  if (route.path === path) {
    const fallback = layoutStore.visitedViews.at(-1)?.path || '/dashboard'
    router.push(fallback)
  }
}

function closeOthers() {
  layoutStore.closeOtherViews(route.path)
}
</script>
