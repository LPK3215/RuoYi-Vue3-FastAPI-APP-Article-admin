<template>
  <view class="flex h-full flex-col bg-[#0b0f14]">
    <!-- Hero -->
    <view class="px-4 pt-4 pb-3">
      <view
        class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-950 via-slate-900 to-blue-900 p-5 shadow-xl shadow-black/40"
      >
        <view
          class="absolute -right-14 -top-16 size-40 rounded-full bg-blue-400/20 blur-2xl"
        ></view>
        <view
          class="absolute -left-10 -bottom-14 size-40 rounded-full bg-white/10 blur-2xl"
        ></view>

        <view class="relative z-10">
          <view class="flex items-start justify-between">
            <view>
              <view class="text-[22px] font-bold text-white tracking-wide"
                >软件库</view
              >
              <view class="mt-1 text-xs text-white/70"
                >精选 · 分类 · 多平台下载</view
              >
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
              <view class="i-mdi-fire text-base text-orange-300"></view>
              <text class="text-xs"
                >已上架：{{ total || softwareList.length }} 项</text
              >
            </view>
            <view class="text-xs text-white/60"
              >{{ selectedCategoryName || "全部分类" }}</view
            >
          </view>
        </view>
      </view>

      <!-- Search -->
      <view class="-mt-4 rounded-2xl bg-white p-4 shadow-lg shadow-black/20">
        <view class="flex items-center space-x-2">
          <view
            class="flex size-10 items-center justify-center rounded-2xl bg-slate-950 text-white"
          >
            <view class="i-mdi-magnify text-xl"></view>
          </view>
          <input
            v-model="keyword"
            class="h-10 flex-1 rounded-xl bg-gray-50 px-3 text-sm text-gray-900"
            placeholder="搜索软件名称 / 描述..."
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
              class="absolute -top-1 -right-1 flex size-5 items-center justify-center rounded-full bg-[#F97316] text-[10px] font-bold text-white"
            >
              {{ activeFilterCount }}
            </view>
          </view>
          <view
            class="px-3 py-2 rounded-xl bg-[#F97316] text-white text-xs font-semibold active:opacity-80"
            @click="handleSearch"
          >
            搜索
          </view>
        </view>

        <view v-if="activeFilterChips.length" class="mt-3 flex flex-wrap gap-2">
          <view
            v-for="chip in activeFilterChips"
            :key="chip.key"
            class="flex items-center rounded-full bg-gray-50 border border-gray-200 px-3 py-1 text-[11px] text-gray-700"
          >
            <text class="font-semibold">{{ chip.label }}</text>
            <view
              class="i-mdi-close ml-1 text-base text-gray-400 active:opacity-70"
              @click.stop="clearFilter(chip.key)"
            ></view>
          </view>
          <view
            class="flex items-center rounded-full bg-white border border-gray-200 px-3 py-1 text-[11px] text-gray-600 active:opacity-80"
            @click="clearAllFilters"
          >
            清空筛选
          </view>
        </view>
      </view>
    </view>

    <!-- Content -->
    <view class="flex-1 overflow-hidden rounded-t-3xl bg-gray-50">
      <!-- Categories -->
      <view class="px-4 pt-4">
        <scroll-view
          scroll-x
          class="whitespace-nowrap"
          :show-scrollbar="false"
        >
          <view
            class="inline-flex items-center space-x-2 pr-3"
            @click="selectCategory(null)"
          >
            <view
              class="rounded-full border px-3 py-1.5 text-xs font-semibold transition-all"
              :class="
                selectedCategoryId === null
                  ? 'bg-slate-950 text-white border-slate-950'
                  : 'bg-white text-gray-700 border-gray-200'
              "
              >全部</view
            >
          </view>

          <view
            v-for="c in categories"
            :key="c.categoryId"
            class="inline-flex items-center space-x-2 pr-3"
            @click="selectCategory(c)"
          >
            <view
              class="rounded-full border px-3 py-1.5 text-xs font-semibold transition-all"
              :class="
                selectedCategoryId === c.categoryId
                  ? 'bg-slate-950 text-white border-slate-950'
                  : 'bg-white text-gray-700 border-gray-200'
              "
            >
              <text>{{ c.categoryName }}</text>
              <text class="ml-1 opacity-70">({{ c.softwareCount }})</text>
            </view>
          </view>
        </scroll-view>
      </view>

      <!-- List -->
      <scroll-view scroll-y class="h-full" :show-scrollbar="false">
        <view class="p-4 pb-24">
          <view v-if="loading" class="space-y-3">
            <view
              v-for="i in 6"
              :key="i"
              class="h-20 rounded-2xl bg-white border border-gray-100 animate-pulse"
            ></view>
          </view>

          <view v-else-if="!softwareList.length" class="pt-12">
            <view class="flex flex-col items-center">
              <view
                class="flex size-14 items-center justify-center rounded-2xl bg-slate-950 text-white"
              >
                <view class="i-mdi-database-off text-2xl"></view>
              </view>
              <view class="mt-3 text-sm font-semibold text-gray-900"
                >暂无数据</view
              >
              <view class="mt-1 text-xs text-gray-500"
                >换个关键字或分类试试</view
              >
            </view>
          </view>

          <view v-else class="space-y-3">
            <view
              v-for="item in softwareList"
              :key="item.softwareId"
              class="group flex items-center rounded-2xl bg-white p-4 shadow-sm border border-gray-100 active:scale-[0.99] transition-transform"
              @click="toDetail(item)"
            >
              <view
                class="flex size-12 items-center justify-center overflow-hidden rounded-2xl bg-gradient-to-br from-slate-950 to-slate-700 text-white shadow-md shadow-black/10"
              >
                <image
                  v-if="item.iconUrl"
                  :src="item.iconUrl"
                  mode="aspectFill"
                  class="size-12"
                />
                <text v-else class="text-sm font-black">{{
                  (item.softwareName || "?").slice(0, 1).toUpperCase()
                }}</text>
              </view>

              <view class="ml-4 flex-1 overflow-hidden">
                <view class="flex items-center justify-between">
                  <view
                    class="text-sm font-bold text-gray-900 truncate pr-2"
                    >{{ item.softwareName }}</view
                  >
                  <view class="flex items-center gap-1">
                    <view
                      class="rounded-full bg-orange-50 px-2 py-0.5 text-[10px] font-semibold text-orange-700 border border-orange-100"
                      >上架</view
                    >
                    <view
                      v-if="item.openSource === '1'"
                      class="rounded-full bg-green-50 px-2 py-0.5 text-[10px] font-semibold text-green-700 border border-green-100"
                      >开源</view
                    >
                  </view>
                </view>
                <view class="mt-1 text-xs text-gray-500 truncate">
                  {{ item.shortDesc || "暂无描述" }}
                </view>
                <view v-if="tagList(item).length" class="mt-2 flex flex-wrap gap-1">
                  <view
                    v-for="t in tagList(item).slice(0, 3)"
                    :key="t"
                    class="rounded-full bg-slate-50 px-2 py-0.5 text-[10px] font-semibold text-slate-600 border border-slate-200"
                  >
                    {{ t }}
                  </view>
                </view>
                <view class="mt-2 flex items-center justify-between">
                  <view class="flex min-w-0 items-center gap-2">
                    <text class="text-[10px] text-gray-400 truncate">
                      {{ item.categoryName || "未分类" }}
                    </text>
                    <view
                      v-if="item.license"
                      class="shrink-0 rounded-full bg-slate-50 px-2 py-0.5 text-[10px] font-semibold text-slate-600 border border-slate-200"
                    >
                      {{ item.license }}
                    </view>
                  </view>
                  <text class="shrink-0 text-[10px] text-gray-400">
                    {{ formatDate(item.updateTime) }}
                  </text>
                </view>
              </view>

              <view class="ml-2 text-gray-300">
                <view class="i-mdi-chevron-right text-xl"></view>
              </view>
            </view>

            <view v-if="hasNext" class="pt-2 flex justify-center">
              <view
                class="rounded-full bg-white border border-gray-200 px-4 py-2 text-xs text-gray-600 active:opacity-80"
                @click.stop="loadMore"
                >加载更多</view
              >
            </view>
            <view v-else class="pt-2 flex justify-center">
              <view class="text-[10px] text-gray-400">— 已到底 —</view>
            </view>
          </view>
        </view>
      </scroll-view>
    </view>

    <!-- Filter Drawer -->
    <view v-show="filterOpen" class="fixed inset-0 z-50">
      <view class="absolute inset-0 bg-black/40" @click="closeFilter"></view>
      <view class="absolute bottom-0 left-0 right-0 rounded-t-3xl bg-white p-4">
        <view class="flex items-center justify-between">
          <view class="flex items-center space-x-2">
            <view class="i-mdi-tune-variant text-xl text-slate-900"></view>
            <text class="text-base font-extrabold text-gray-900">筛选</text>
            <view
              v-if="draftActiveCount"
              class="rounded-full bg-orange-50 px-2 py-0.5 text-[10px] font-semibold text-orange-700 border border-orange-100"
            >
              {{ draftActiveCount }} 项
            </view>
          </view>
          <view
            class="flex size-10 items-center justify-center rounded-2xl bg-gray-50 text-gray-600 border border-gray-100 active:opacity-70"
            @click="closeFilter"
          >
            <view class="i-mdi-close text-xl"></view>
          </view>
        </view>

        <scroll-view scroll-y style="max-height: 70vh" :show-scrollbar="false">
          <!-- Open Source -->
          <view class="mt-4">
            <view class="flex items-center justify-between">
              <text class="text-xs font-semibold text-gray-700">开源</text>
              <text class="text-[10px] text-gray-400">可选</text>
            </view>
            <view class="mt-2 flex flex-wrap gap-2">
              <view
                class="rounded-full border px-3 py-1.5 text-xs font-semibold"
                :class="
                  draftFilters.openSource === undefined
                    ? 'bg-slate-950 text-white border-slate-950'
                    : 'bg-gray-50 text-gray-700 border-gray-200'
                "
                @click="draftFilters.openSource = undefined"
              >
                全部
              </view>
              <view
                class="rounded-full border px-3 py-1.5 text-xs font-semibold"
                :class="
                  draftFilters.openSource === '1'
                    ? 'bg-slate-950 text-white border-slate-950'
                    : 'bg-gray-50 text-gray-700 border-gray-200'
                "
                @click="draftFilters.openSource = '1'"
              >
                开源
              </view>
              <view
                class="rounded-full border px-3 py-1.5 text-xs font-semibold"
                :class="
                  draftFilters.openSource === '0'
                    ? 'bg-slate-950 text-white border-slate-950'
                    : 'bg-gray-50 text-gray-700 border-gray-200'
                "
                @click="draftFilters.openSource = '0'"
              >
                闭源
              </view>
            </view>
          </view>

          <!-- Platform -->
          <view class="mt-4">
            <view class="flex items-center justify-between">
              <text class="text-xs font-semibold text-gray-700">平台</text>
              <text class="text-[10px] text-gray-400">基于下载配置聚合</text>
            </view>
            <view class="mt-2 flex flex-wrap gap-2">
              <view
                class="rounded-full border px-3 py-1.5 text-xs font-semibold"
                :class="
                  !draftFilters.platform
                    ? 'bg-slate-950 text-white border-slate-950'
                    : 'bg-gray-50 text-gray-700 border-gray-200'
                "
                @click="draftFilters.platform = ''"
              >
                全部
              </view>
              <view
                v-for="p in facets.platforms || []"
                :key="p.value"
                class="rounded-full border px-3 py-1.5 text-xs font-semibold"
                :class="
                  draftFilters.platform === p.value
                    ? 'bg-slate-950 text-white border-slate-950'
                    : 'bg-gray-50 text-gray-700 border-gray-200'
                "
                @click="draftFilters.platform = p.value"
              >
                {{ platformName(p.value) }}
                <text class="ml-1 opacity-70">({{ p.count }})</text>
              </view>
            </view>
          </view>

          <!-- License -->
          <view class="mt-4">
            <view class="flex items-center justify-between">
              <text class="text-xs font-semibold text-gray-700">许可证</text>
              <text class="text-[10px] text-gray-400">可输入或点选</text>
            </view>
            <input
              v-model="draftFilters.license"
              class="mt-2 h-10 w-full rounded-xl bg-gray-50 px-3 text-sm text-gray-900 border border-gray-200"
              placeholder="MIT / Apache-2.0 / GPL-3.0 ..."
              placeholder-class="text-gray-400"
              confirm-type="done"
            />
            <view class="mt-2 flex flex-wrap gap-2">
              <view
                v-for="l in (facets.licenses || []).slice(0, 18)"
                :key="l.value"
                class="rounded-full border px-3 py-1.5 text-xs font-semibold"
                :class="
                  draftFilters.license === l.value
                    ? 'bg-slate-950 text-white border-slate-950'
                    : 'bg-gray-50 text-gray-700 border-gray-200'
                "
                @click="draftFilters.license = l.value"
              >
                {{ l.value }}
                <text class="ml-1 opacity-70">({{ l.count }})</text>
              </view>
            </view>
          </view>

          <!-- Tag -->
          <view class="mt-4">
            <view class="flex items-center justify-between">
              <text class="text-xs font-semibold text-gray-700">标签</text>
              <text class="text-[10px] text-gray-400">单个标签过滤</text>
            </view>
            <view class="mt-2 flex flex-wrap gap-2">
              <view
                class="rounded-full border px-3 py-1.5 text-xs font-semibold"
                :class="
                  !draftFilters.tag ? 'bg-slate-950 text-white border-slate-950' : 'bg-gray-50 text-gray-700 border-gray-200'
                "
                @click="draftFilters.tag = ''"
              >
                全部
              </view>
              <view
                v-for="t in (facets.tags || []).slice(0, 24)"
                :key="t.value"
                class="rounded-full border px-3 py-1.5 text-xs font-semibold"
                :class="
                  draftFilters.tag === t.value
                    ? 'bg-slate-950 text-white border-slate-950'
                    : 'bg-gray-50 text-gray-700 border-gray-200'
                "
                @click="draftFilters.tag = t.value"
              >
                {{ t.value }}
                <text class="ml-1 opacity-70">({{ t.count }})</text>
              </view>
            </view>
          </view>

          <view class="h-4"></view>
        </scroll-view>

        <view class="mt-4 flex items-center space-x-3">
          <view
            class="flex-1 rounded-2xl bg-gray-50 border border-gray-200 px-4 py-3 text-center text-sm font-semibold text-gray-700 active:opacity-80"
            @click="resetDraft"
          >
            清空
          </view>
          <view
            class="flex-1 rounded-2xl bg-slate-950 px-4 py-3 text-center text-sm font-extrabold text-white active:opacity-90"
            @click="applyFilter"
          >
            应用
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, reactive, ref, watch } from "vue";
import { onLoad, onPullDownRefresh, onReachBottom } from "@dcloudio/uni-app";

import { getPortalSoftwareCategories, getPortalSoftwareFacets, listPortalSoftware } from "@/api/software";

const { proxy } = getCurrentInstance();

const loading = ref(true);
const categories = ref([]);
const softwareList = ref([]);
const facets = ref({
  tags: [],
  licenses: [],
  platforms: [],
  authors: [],
  teams: [],
});

const keyword = ref("");
const pageNum = ref(1);
const pageSize = ref(10);
const total = ref(0);
const hasNext = ref(false);

const selectedCategoryId = ref(null);

const filterStorageKey = "softwarehub:portal:filters";
const filterOpen = ref(false);

const filters = reactive({
  openSource: undefined,
  platform: "",
  license: "",
  tag: "",
});

const draftFilters = reactive({
  openSource: undefined,
  platform: "",
  license: "",
  tag: "",
});

const selectedCategoryName = computed(() => {
  if (selectedCategoryId.value === null) return "";
  const c = categories.value.find((x) => x.categoryId === selectedCategoryId.value);
  return c?.categoryName || "";
});

function platformName(p) {
  const map = {
    windows: "Windows",
    mac: "macOS",
    linux: "Linux",
    android: "Android",
    ios: "iOS",
    web: "Web",
    other: "Other",
  };
  return map[p] || (p ? String(p).toUpperCase() : "Unknown");
}

function tagList(row) {
  const raw = row?.tags;
  if (!raw) return [];
  return String(raw)
    .replace(/，/g, ",")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
}

const activeFilterCount = computed(() => {
  let count = 0;
  if (filters.openSource === "0" || filters.openSource === "1") count += 1;
  if (filters.platform) count += 1;
  if (filters.license) count += 1;
  if (filters.tag) count += 1;
  return count;
});

const activeFilterChips = computed(() => {
  const result = [];
  if (filters.openSource === "1") result.push({ key: "openSource", label: "开源：是" });
  if (filters.openSource === "0") result.push({ key: "openSource", label: "开源：否" });
  if (filters.platform) result.push({ key: "platform", label: `平台：${platformName(filters.platform)}` });
  if (filters.license) result.push({ key: "license", label: `许可证：${filters.license}` });
  if (filters.tag) result.push({ key: "tag", label: `标签：${filters.tag}` });
  return result;
});

const draftActiveCount = computed(() => {
  let count = 0;
  if (draftFilters.openSource === "0" || draftFilters.openSource === "1") count += 1;
  if (draftFilters.platform) count += 1;
  if (draftFilters.license) count += 1;
  if (draftFilters.tag) count += 1;
  return count;
});

function formatDate(v) {
  if (!v) return "";
  const d = new Date(v);
  if (Number.isNaN(d.getTime())) return "";
  const pad = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

async function fetchCategories() {
  const res = await getPortalSoftwareCategories();
  categories.value = res.data || [];
}

async function fetchFacets() {
  const res = await getPortalSoftwareFacets(80);
  facets.value = res.data || facets.value;
}

async function fetchList(reset = false) {
  if (reset) {
    pageNum.value = 1;
    softwareList.value = [];
  }
  loading.value = pageNum.value === 1;
  const res = await listPortalSoftware({
    pageNum: pageNum.value,
    pageSize: pageSize.value,
    categoryId: selectedCategoryId.value || undefined,
    keyword: keyword.value || undefined,
    openSource: filters.openSource || undefined,
    platform: filters.platform || undefined,
    license: filters.license || undefined,
    tag: filters.tag || undefined,
  });
  const rows = res.rows || [];
  softwareList.value = reset ? rows : softwareList.value.concat(rows);
  total.value = res.total || 0;
  hasNext.value = !!res.hasNext;
  loading.value = false;
}

function selectCategory(c) {
  selectedCategoryId.value = c ? c.categoryId : null;
  fetchList(true);
}

function handleSearch() {
  fetchList(true);
}

function openFilter() {
  Object.assign(draftFilters, filters);
  filterOpen.value = true;
}

function closeFilter() {
  filterOpen.value = false;
}

function resetDraft() {
  draftFilters.openSource = undefined;
  draftFilters.platform = "";
  draftFilters.license = "";
  draftFilters.tag = "";
}

function applyFilter() {
  Object.assign(filters, draftFilters);
  filterOpen.value = false;
  fetchList(true);
}

function clearFilter(key) {
  if (key === "openSource") filters.openSource = undefined;
  if (key === "platform") filters.platform = "";
  if (key === "license") filters.license = "";
  if (key === "tag") filters.tag = "";
  fetchList(true);
}

function resetFilters(withFetch = true) {
  filters.openSource = undefined;
  filters.platform = "";
  filters.license = "";
  filters.tag = "";
  if (withFetch) fetchList(true);
}

function clearAllFilters() {
  resetFilters(true);
}

function toDetail(item) {
  uni.navigateTo({
    url: `/pages/software/detail?softwareId=${item.softwareId}`,
  });
}

function loadMore() {
  if (!hasNext.value) return;
  pageNum.value += 1;
  fetchList(false);
}

function refreshAll() {
  keyword.value = "";
  selectedCategoryId.value = null;
  resetFilters(false);
  Promise.all([fetchCategories(), fetchFacets(), fetchList(true)]).catch(() => {});
}

function loadFilters() {
  try {
    const cached = uni.getStorageSync(filterStorageKey);
    if (cached && typeof cached === "object") {
      filters.openSource = cached.openSource === "0" || cached.openSource === "1" ? cached.openSource : undefined;
      filters.platform = typeof cached.platform === "string" ? cached.platform : "";
      filters.license = typeof cached.license === "string" ? cached.license : "";
      filters.tag = typeof cached.tag === "string" ? cached.tag : "";
    }
  } catch (e) {}
}

watch(
  filters,
  (val) => {
    try {
      uni.setStorageSync(filterStorageKey, {
        openSource: val.openSource,
        platform: val.platform,
        license: val.license,
        tag: val.tag,
      });
    } catch (e) {}
  },
  { deep: true },
);

onLoad(() => {
  loadFilters();
  Promise.all([fetchCategories(), fetchFacets(), fetchList(true)])
    .catch(() => {
      proxy.$modal?.msg?.("加载失败，请稍后重试");
    })
    .finally(() => {
      loading.value = false;
    });
});

onPullDownRefresh(() => {
  Promise.all([fetchCategories(), fetchFacets(), fetchList(true)])
    .catch(() => {})
    .finally(() => uni.stopPullDownRefresh());
});

onReachBottom(() => {
  loadMore();
});
</script>

<style>
page {
  height: 100%;
  background-color: #0b0f14;
}
</style>
