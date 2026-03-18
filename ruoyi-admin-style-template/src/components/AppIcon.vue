<template>
  <el-icon>
    <component :is="resolvedIcon" />
  </el-icon>
</template>

<script setup>
import { computed } from 'vue'
import * as icons from '@element-plus/icons-vue'

const props = defineProps({
  name: {
    type: String,
    default: 'Grid',
  },
})

const resolvedIcon = computed(() => icons[props.name] || icons.Grid)
</script>
