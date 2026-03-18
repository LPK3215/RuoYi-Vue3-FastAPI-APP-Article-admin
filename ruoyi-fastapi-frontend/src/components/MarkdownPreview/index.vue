<template>
  <MarkdownRender
    :content="content"
    :is-dark="isDark"
    :render-code-blocks-as-pre="true"
    :show-tooltips="showTooltips"
  />
</template>

<script setup>
import { MarkdownRender, enableKatex, enableMermaid } from "markstream-vue";
import "markstream-vue/index.css";
import "katex/dist/katex.min.css";

let isRendererEnabled = false;

if (!isRendererEnabled) {
  enableMermaid();
  enableKatex();
  isRendererEnabled = true;
}

defineProps({
  content: {
    type: String,
    default: "",
  },
  isDark: {
    type: Boolean,
    default: undefined,
  },
  showTooltips: {
    type: Boolean,
    default: true,
  },
});
</script>
