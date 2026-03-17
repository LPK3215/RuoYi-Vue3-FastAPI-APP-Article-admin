<template>
  <view class="min-h-full bg-[#0b0f14]">
    <view class="px-4 pt-4 pb-3">
      <view class="rounded-3xl bg-white p-4 shadow-sm">
        <view class="flex items-start justify-between">
          <view class="flex-1">
            <view class="flex items-center space-x-2">
              <view class="px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-600 text-[11px] font-semibold">
                {{ articleTypeLabel(detail.articleType) }}
              </view>
              <view class="text-[16px] font-bold text-gray-900 line-clamp-2">{{ detail.title || "教程详情" }}</view>
            </view>
            <view class="mt-2 text-xs text-gray-500">{{ detail.summary || "—" }}</view>
            <view class="mt-3 flex items-center justify-between text-[11px] text-gray-400">
              <view class="flex items-center space-x-1">
                <view class="i-mdi-calendar-clock text-base"></view>
                <text>{{ formatDateTime(detail.publishTime || detail.updateTime) }}</text>
              </view>
              <view class="flex items-center space-x-1">
                <view class="i-mdi-tag-outline text-base"></view>
                <text class="line-clamp-1">{{ detail.tags || "无标签" }}</text>
              </view>
            </view>
          </view>
          <image
            v-if="detail.coverUrl"
            :src="detail.coverUrl"
            mode="aspectFill"
            class="ml-3 h-16 w-16 rounded-2xl bg-gray-100"
          />
        </view>
      </view>
    </view>

    <view class="px-4 pb-24 space-y-3">
      <!-- Content -->
      <view class="rounded-3xl bg-white p-4 shadow-sm">
        <view class="flex items-center justify-between">
          <view class="text-sm font-bold text-gray-900">正文</view>
          <view class="text-[11px] text-gray-400">contentMd</view>
        </view>
        <view class="mt-3">
          <view v-if="htmlContent" class="prose" v-html="htmlContent"></view>
          <view v-else class="text-xs text-gray-500">暂无正文</view>
        </view>
      </view>

      <!-- Attachments -->
      <view class="rounded-3xl bg-white p-4 shadow-sm">
        <view class="flex items-center justify-between">
          <view class="text-sm font-bold text-gray-900">附件</view>
          <view class="text-[11px] text-gray-400">{{ attachments.length }} 个</view>
        </view>
        <view class="mt-3 space-y-2" v-if="attachments.length">
          <view
            v-for="a in attachments"
            :key="a.url + '-' + a.name"
            class="rounded-2xl border border-gray-100 p-3 active:opacity-80"
            @click="openUrl(a.url)"
          >
            <view class="flex items-start justify-between">
              <view class="flex-1">
                <view class="text-sm font-semibold text-gray-900 line-clamp-1">{{ a.name }}</view>
                <view class="mt-1 text-[11px] text-gray-500 line-clamp-1">{{ formatFileSize(a.size) || a.url }}</view>
              </view>
              <view class="ml-3 text-gray-400">
                <view class="i-mdi-open-in-new text-xl"></view>
              </view>
            </view>
          </view>
        </view>
        <view v-else class="mt-3 text-xs text-gray-500">暂无附件</view>
      </view>

      <!-- Related softwares -->
      <view class="rounded-3xl bg-white p-4 shadow-sm">
        <view class="flex items-center justify-between">
          <view class="text-sm font-bold text-gray-900">关联软件</view>
          <view class="text-[11px] text-gray-400">{{ softwares.length }} 个</view>
        </view>

        <view class="mt-3 space-y-2" v-if="softwares.length">
          <view
            v-for="s in softwares"
            :key="s.softwareId"
            class="rounded-2xl border border-gray-100 p-3 active:opacity-80"
            @click="goSoftware(s.softwareId)"
          >
            <view class="text-sm font-semibold text-gray-900 line-clamp-1">{{ s.softwareName || `软件 #${s.softwareId}` }}</view>
            <view class="mt-1 text-[11px] text-gray-500 line-clamp-1">{{ s.shortDesc || s.categoryName || "—" }}</view>
          </view>
        </view>
        <view v-else class="mt-3 text-xs text-gray-500">暂无关联软件</view>
      </view>

      <view v-if="loading" class="py-6 text-center text-white/60 text-xs">加载中...</view>
    </view>
  </view>
</template>

<script setup>
import { computed, ref } from "vue";
import { getPortalArticleDetail } from "@/api/article";
import { mdToHtml } from "@/utils/markdown";
import { useDict } from "@/utils/dict";

const { kb_article_type } = useDict("kb_article_type");

const loading = ref(false);
const articleId = ref(0);
const detail = ref({
  articleId: undefined,
  title: undefined,
  summary: undefined,
  coverUrl: undefined,
  contentMd: undefined,
  tags: undefined,
  articleType: undefined,
  publishTime: undefined,
  updateTime: undefined,
  softwares: [],
  attachments: [],
});

const htmlContent = computed(() => {
  return mdToHtml(detail.value?.contentMd || "");
});

const typeOptions = computed(() => {
  const list = kb_article_type?.value || [];
  if (list.length) return list;
  return [
    { label: "教程", value: "tutorial" },
    { label: "笔记", value: "note" },
    { label: "FAQ", value: "faq" },
  ];
});

function articleTypeLabel(value) {
  const v = String(value || "").trim();
  if (!v) return "教程";
  const hit = (typeOptions.value || []).find((x) => String(x.value) === v);
  return hit?.label || "教程";
}

const attachments = computed(() => {
  const list = detail.value?.attachments || [];
  if (!Array.isArray(list)) return [];
  return list
    .map((x) => ({
      name: String(x?.name || "").trim(),
      url: String(x?.url || "").trim(),
      size: x?.size,
    }))
    .filter((x) => x.name && x.url);
});

const softwares = computed(() => {
  const list = detail.value?.softwares || [];
  return Array.isArray(list) ? list : [];
});

function formatDateTime(iso) {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  const hh = String(d.getHours()).padStart(2, "0");
  const mi = String(d.getMinutes()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd} ${hh}:${mi}`;
}

function formatFileSize(size) {
  const n = Number(size);
  if (!Number.isFinite(n) || n <= 0) return "";
  const kb = n / 1024;
  if (kb < 1024) return `${kb.toFixed(kb < 10 ? 1 : 0)} KB`;
  const mb = kb / 1024;
  if (mb < 1024) return `${mb.toFixed(mb < 10 ? 1 : 0)} MB`;
  const gb = mb / 1024;
  return `${gb.toFixed(gb < 10 ? 1 : 0)} GB`;
}

function openUrl(url) {
  const u = String(url || "").trim();
  if (!u) return;
  // H5/小程序：用内置 webview；App：直接走系统浏览器下载更友好
  // #ifdef APP-PLUS
  plus.runtime.openURL(u);
  // #endif
  // #ifndef APP-PLUS
  uni.navigateTo({ url: `/pages/common/webview/index?url=${encodeURIComponent(u)}` });
  // #endif
}

function goSoftware(softwareId) {
  if (!softwareId) return;
  uni.navigateTo({ url: `/pages/software/detail?softwareId=${softwareId}` });
}

async function loadDetail() {
  if (!articleId.value) return;
  loading.value = true;
  try {
    const res = await getPortalArticleDetail(articleId.value);
    detail.value = res.data || {};
  } finally {
    loading.value = false;
  }
}

onLoad((query) => {
  const n = Number(query?.articleId);
  articleId.value = Number.isFinite(n) && n > 0 ? n : 0;
  loadDetail();
});
</script>
