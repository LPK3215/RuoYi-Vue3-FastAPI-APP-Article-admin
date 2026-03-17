<template>
  <view class="flex h-full flex-col bg-[#0b0f14]">
    <!-- Hero -->
    <view class="px-4 pt-4 pb-3">
      <view
        class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-900 p-5 shadow-xl shadow-black/40"
      >
        <view class="absolute -right-14 -top-16 size-40 rounded-full bg-indigo-400/20 blur-2xl"></view>
        <view class="absolute -left-10 -bottom-14 size-40 rounded-full bg-white/10 blur-2xl"></view>

        <view class="relative z-10">
          <view class="flex items-start justify-between">
            <view>
              <view class="text-[22px] font-bold text-white tracking-wide">教程</view>
              <view class="mt-1 text-xs text-white/70">Markdown · 分类/标签/类型筛选 · 附件下载</view>
            </view>
            <view
              class="flex size-10 items-center justify-center rounded-2xl bg-white/10 text-white/90 backdrop-blur-sm"
              @click="refreshAll"
            >
              <view class="i-mdi-refresh text-xl"></view>
            </view>
          </view>

          <view class="mt-4 flex items-center justify-between">
            <view class="flex items-center space-x-2 text-white/80">
              <view class="i-mdi-book-open-page-variant text-base text-indigo-200"></view>
              <text class="text-xs">共 {{ total || articleList.length }} 篇</text>
            </view>
            <view class="text-xs text-white/60">{{ selectedCategoryName || "全部分类" }}</view>
          </view>
        </view>
      </view>

      <!-- Search -->
      <view class="-mt-4 rounded-2xl bg-white p-4 shadow-lg shadow-black/20">
        <view class="flex items-center space-x-2">
          <view class="flex size-10 items-center justify-center rounded-2xl bg-slate-950 text-white">
            <view class="i-mdi-magnify text-xl"></view>
          </view>
          <input
            v-model="keyword"
            class="h-10 flex-1 rounded-xl bg-gray-50 px-3 text-sm text-gray-900"
            placeholder="搜索标题 / 摘要..."
            placeholder-class="text-gray-400"
            confirm-type="search"
            @confirm="handleSearch"
          />
          <view
            class="relative flex size-10 items-center justify-center rounded-xl bg-gray-50 text-gray-700 border border-gray-200 active:opacity-70"
            @click="openFilter"
          >
            <view class="i-mdi-filter-variant text-xl"></view>
            <view
              v-if="activeFilterCount"
              class="absolute -top-1 -right-1 flex size-5 items-center justify-center rounded-full bg-[#6366F1] text-[10px] font-bold text-white"
            >
              {{ activeFilterCount }}
            </view>
          </view>
          <view
            class="px-3 py-2 rounded-xl bg-[#6366F1] text-white text-xs font-semibold active:opacity-80"
            @click="handleSearch"
          >
            搜索
          </view>
        </view>
      </view>
    </view>

    <!-- List -->
    <scroll-view scroll-y class="flex-1 overflow-hidden" :show-scrollbar="false" @scrolltolower="loadMore">
      <view class="px-4 pb-24">
        <view v-if="loading && pageNum === 1" class="py-10 text-center text-white/70 text-sm">加载中...</view>
        <view v-else-if="!articleList.length" class="py-10 text-center text-white/70 text-sm">暂无数据</view>

        <view v-else class="space-y-3">
          <view
            v-for="item in articleList"
            :key="item.articleId"
            class="rounded-2xl bg-white p-4 shadow-sm border border-gray-100 active:opacity-80"
            @click="goDetail(item.articleId)"
          >
            <view class="flex items-start justify-between">
              <view class="flex-1">
                <view class="flex items-center space-x-2">
                  <view class="px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-600 text-[11px] font-semibold">
                    {{ articleTypeLabel(item.articleType) }}
                  </view>
                  <view class="text-[15px] font-bold text-gray-900 line-clamp-1">{{ item.title || "未命名" }}</view>
                </view>
                <view class="mt-2 text-xs text-gray-500 line-clamp-2">{{ item.summary || "暂无摘要" }}</view>

                <view class="mt-3 flex items-center justify-between">
                  <view class="flex items-center space-x-2">
                    <view class="i-mdi-tag-outline text-base text-gray-400"></view>
                    <view class="text-xs text-gray-500 line-clamp-1">{{ item.tags || "无标签" }}</view>
                  </view>
                  <view class="text-[11px] text-gray-400">{{ formatDate(item.publishTime || item.updateTime) }}</view>
                </view>
              </view>
              <image
                v-if="item.coverUrl"
                :src="item.coverUrl"
                mode="aspectFill"
                class="ml-3 h-16 w-16 rounded-xl bg-gray-100"
              />
            </view>
          </view>
        </view>

        <view v-if="loading && pageNum > 1" class="py-4 text-center text-white/60 text-xs">加载更多...</view>
        <view v-if="!hasMore && articleList.length" class="py-6 text-center text-white/50 text-xs">没有更多了</view>
      </view>
    </scroll-view>

    <!-- Filter Popup -->
    <view v-if="filterOpen" class="fixed inset-0 z-50">
      <view class="absolute inset-0 bg-black/45" @click="closeFilter"></view>
      <view class="absolute bottom-0 left-0 right-0 rounded-t-3xl bg-white p-4">
        <view class="flex items-center justify-between">
          <view class="text-base font-bold text-gray-900">筛选</view>
          <view class="text-xs text-gray-500" @click="resetFilter">清空</view>
        </view>

        <view class="mt-4 space-y-4">
          <view>
            <view class="text-xs text-gray-500 mb-2">分类</view>
            <scroll-view scroll-x class="whitespace-nowrap">
              <view class="inline-flex items-center space-x-2">
                <view
                  class="px-3 py-2 rounded-full text-xs border"
                  :class="selectedCategoryId === '' ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-gray-700 border-gray-200'"
                  @click="selectCategory('')"
                >
                  全部
                </view>
                <view
                  v-for="c in categories"
                  :key="c.categoryId"
                  class="px-3 py-2 rounded-full text-xs border"
                  :class="selectedCategoryId === String(c.categoryId) ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-gray-700 border-gray-200'"
                  @click="selectCategory(String(c.categoryId))"
                >
                  {{ c.categoryName }}
                </view>
              </view>
            </scroll-view>
          </view>

          <view>
            <view class="text-xs text-gray-500 mb-2">类型</view>
            <view class="flex flex-wrap gap-2">
              <view
                class="px-3 py-2 rounded-full text-xs border"
                :class="selectedType === '' ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-gray-700 border-gray-200'"
                @click="selectType('')"
              >
                全部
              </view>
              <view
                v-for="t in typeOptions"
                :key="t.value"
                class="px-3 py-2 rounded-full text-xs border"
                :class="selectedType === t.value ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-gray-700 border-gray-200'"
                @click="selectType(t.value)"
              >
                {{ t.label }}
              </view>
            </view>
          </view>

          <view>
            <view class="text-xs text-gray-500 mb-2">标签（单个）</view>
            <input
              v-model="tag"
              class="h-10 w-full rounded-xl bg-gray-50 px-3 text-sm text-gray-900"
              placeholder="输入标签，如：安装"
              placeholder-class="text-gray-400"
              confirm-type="done"
            />
          </view>
        </view>

        <view class="mt-5 flex space-x-3">
          <view class="flex-1 h-11 rounded-xl border border-gray-200 flex items-center justify-center text-sm text-gray-700" @click="closeFilter">
            取消
          </view>
          <view class="flex-1 h-11 rounded-xl bg-indigo-600 flex items-center justify-center text-sm font-semibold text-white" @click="applyFilter">
            应用
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, ref } from "vue";
import { getPortalArticleCategories, listPortalArticle } from "@/api/article";
import { useDict } from "@/utils/dict";

const { kb_article_type } = useDict("kb_article_type");

const keyword = ref("");
const tag = ref("");
const filterOpen = ref(false);

const categories = ref([]);
const selectedCategoryId = ref("");
const selectedType = ref("");

const pageNum = ref(1);
const pageSize = ref(10);
const total = ref(0);
const hasMore = ref(true);
const loading = ref(false);
const articleList = ref([]);

const typeOptions = computed(() => {
  const list = kb_article_type?.value || [];
  if (list.length) return list;
  return [
    { label: "教程", value: "tutorial" },
    { label: "笔记", value: "note" },
    { label: "FAQ", value: "faq" },
  ];
});

const activeFilterCount = computed(() => {
  let c = 0;
  if (selectedCategoryId.value) c += 1;
  if (selectedType.value) c += 1;
  if ((tag.value || "").trim()) c += 1;
  return c;
});

const selectedCategoryName = computed(() => {
  const id = selectedCategoryId.value;
  if (!id) return "";
  const hit = (categories.value || []).find((x) => String(x.categoryId) === id);
  return hit?.categoryName || "";
});

function articleTypeLabel(value) {
  const v = String(value || "").trim();
  if (!v) return "教程";
  const hit = (typeOptions.value || []).find((x) => String(x.value) === v);
  return hit?.label || "教程";
}

function formatDate(iso) {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

function openFilter() {
  filterOpen.value = true;
}
function closeFilter() {
  filterOpen.value = false;
}
function resetFilter() {
  selectedCategoryId.value = "";
  selectedType.value = "";
  tag.value = "";
}
function selectCategory(id) {
  selectedCategoryId.value = id;
}
function selectType(v) {
  selectedType.value = v;
}
function applyFilter() {
  closeFilter();
  handleSearch();
}

function goDetail(articleId) {
  if (!articleId) return;
  uni.navigateTo({ url: `/pages/article/detail?articleId=${articleId}` });
}

async function loadCategories() {
  const res = await getPortalArticleCategories();
  categories.value = res.data || [];
}

function buildQuery(nextPageNum) {
  const q = { pageNum: nextPageNum, pageSize: pageSize.value };
  if ((keyword.value || "").trim()) q.keyword = keyword.value.trim();
  if ((tag.value || "").trim()) q.tag = tag.value.trim();
  if ((selectedCategoryId.value || "").trim()) q.categoryId = Number(selectedCategoryId.value);
  if ((selectedType.value || "").trim()) q.articleType = selectedType.value.trim();
  return q;
}

async function fetchList(nextPageNum, append = false) {
  if (loading.value) return;
  loading.value = true;
  try {
    const res = await listPortalArticle(buildQuery(nextPageNum));
    const rows = res.rows || [];
    total.value = res.total || 0;
    if (append) {
      articleList.value = [...articleList.value, ...rows];
    } else {
      articleList.value = rows;
    }
    pageNum.value = nextPageNum;
    hasMore.value = articleList.value.length < (total.value || 0);
  } finally {
    loading.value = false;
  }
}

function refreshAll() {
  fetchList(1, false);
}

function handleSearch() {
  fetchList(1, false);
}

function loadMore() {
  if (!hasMore.value || loading.value) return;
  fetchList(pageNum.value + 1, true);
}

onLoad(async () => {
  await loadCategories();
  await fetchList(1, false);
});
</script>

