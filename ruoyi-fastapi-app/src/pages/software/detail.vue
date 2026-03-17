<template>
  <view class="flex h-full flex-col bg-[#0b0f14]">
    <!-- Hero -->
    <view class="px-4 pt-4 pb-3">
      <view
        class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-blue-600 via-slate-950 to-black p-5 shadow-xl shadow-black/40"
      >
        <view
          class="absolute -right-10 -top-10 size-40 rounded-full bg-white/10 blur-2xl"
        ></view>
        <view
          class="absolute -left-16 -bottom-16 size-48 rounded-full bg-blue-300/15 blur-3xl"
        ></view>

        <view class="relative z-10 flex items-start space-x-4">
          <view
            class="flex size-14 items-center justify-center overflow-hidden rounded-3xl bg-white/10 text-white backdrop-blur-sm shadow-md shadow-black/20"
          >
            <image
              v-if="detail.iconUrl"
              :src="detail.iconUrl"
              mode="aspectFill"
              class="size-14"
            />
            <text v-else class="text-base font-black">{{
              (detail.softwareName || "?").slice(0, 1).toUpperCase()
            }}</text>
          </view>

          <view class="flex-1 overflow-hidden">
            <view class="text-lg font-extrabold text-white truncate">
              {{ detail.softwareName || "软件详情" }}
            </view>
            <view class="mt-1 text-xs text-white/70 truncate">
              {{ detail.shortDesc || "暂无描述" }}
            </view>
            <view class="mt-3 flex flex-wrap items-center gap-2">
              <view
                class="rounded-full bg-white/10 px-3 py-1 text-[10px] font-semibold text-white/80 border border-white/10"
              >
                {{ detail.categoryName || "未分类" }}
              </view>
              <view
                v-if="detail.openSource === '1'"
                class="rounded-full bg-emerald-400/15 px-3 py-1 text-[10px] font-semibold text-emerald-100 border border-emerald-400/20"
              >
                开源
              </view>
              <view
                v-if="detail.license"
                class="rounded-full bg-white/10 px-3 py-1 text-[10px] font-semibold text-white/80 border border-white/10"
              >
                {{ detail.license }}
              </view>
              <view
                v-for="t in detailTags"
                :key="t"
                class="rounded-full bg-white/10 px-3 py-1 text-[10px] font-semibold text-white/70 border border-white/10"
              >
                {{ t }}
              </view>
              <view
                class="rounded-full bg-white/10 px-3 py-1 text-[10px] font-semibold text-white/80 border border-white/10"
              >
                更新：{{ formatDate(detail.updateTime) || "—" }}
              </view>
            </view>
          </view>
        </view>

        <view class="mt-4 flex items-center justify-between">
          <view class="text-xs text-white/60">
            <text class="opacity-90">下载配置：</text>
            <text class="font-semibold text-white/90"
              >{{ (detail.downloads || []).length }}</text
            >
          </view>
          <view
            class="flex items-center space-x-2 rounded-full bg-white/10 px-3 py-1 text-[10px] font-semibold text-white/80 border border-white/10 active:opacity-80"
            @click="reload"
          >
            <view class="i-mdi-refresh text-sm"></view>
            <text>刷新</text>
          </view>
        </view>
      </view>
    </view>

    <!-- Content -->
    <view class="flex-1 overflow-hidden rounded-t-3xl bg-gray-50">
      <scroll-view scroll-y class="h-full" :show-scrollbar="false">
        <view class="p-4 pb-24 space-y-4">
          <!-- Meta -->
          <view class="rounded-2xl bg-white p-4 shadow-sm border border-gray-100">
            <view class="flex items-center justify-between">
              <view class="flex items-center space-x-2">
                <view class="i-mdi-information-outline text-lg text-slate-900"></view>
                <text class="text-sm font-bold text-gray-900">基础信息</text>
              </view>
              <view class="text-[10px] text-gray-400">只读展示</view>
            </view>

            <view class="mt-3 flex flex-wrap gap-2">
              <view
                v-if="detail.openSource === '1'"
                class="rounded-full bg-emerald-50 px-3 py-1 text-[10px] font-semibold text-emerald-700 border border-emerald-100"
              >
                开源
              </view>
              <view
                v-else
                class="rounded-full bg-gray-50 px-3 py-1 text-[10px] font-semibold text-gray-600 border border-gray-200"
              >
                闭源
              </view>
              <view
                v-if="detail.license"
                class="rounded-full bg-slate-50 px-3 py-1 text-[10px] font-semibold text-slate-600 border border-slate-200"
              >
                许可证：{{ detail.license }}
              </view>
              <view
                v-if="detail.author || detail.team"
                class="rounded-full bg-slate-50 px-3 py-1 text-[10px] font-semibold text-slate-600 border border-slate-200"
              >
                作者/团队：{{ detail.author || detail.team }}
              </view>
              <view
                v-if="(detail.resources || []).length"
                class="rounded-full bg-slate-50 px-3 py-1 text-[10px] font-semibold text-slate-600 border border-slate-200"
              >
                资源：{{ (detail.resources || []).length }}
              </view>
            </view>

            <view v-if="detailTagsAll.length" class="mt-3">
              <view class="text-[10px] text-gray-500">标签</view>
              <view class="mt-2 flex flex-wrap gap-2">
                <view
                  v-for="t in detailTagsAll"
                  :key="t"
                  class="rounded-full bg-gray-50 px-3 py-1 text-[10px] font-semibold text-gray-700 border border-gray-200"
                >
                  {{ t }}
                </view>
              </view>
            </view>

            <view class="mt-3 space-y-2">
              <view
                v-if="detail.officialUrl"
                class="flex items-center justify-between rounded-2xl border border-gray-100 bg-gray-50 p-3"
              >
                <view class="flex min-w-0 items-center space-x-2">
                  <view class="i-mdi-web text-lg text-slate-800"></view>
                  <view class="min-w-0">
                    <view class="text-xs font-bold text-gray-900">官网</view>
                    <view class="mt-1 text-[10px] text-gray-500 truncate">{{ detail.officialUrl }}</view>
                  </view>
                </view>
                <view class="ml-3 flex items-center space-x-2">
                  <view
                    class="rounded-xl bg-white px-3 py-2 text-[10px] font-bold text-slate-900 border border-gray-200 active:opacity-70"
                    @click.stop="copyLink(detail.officialUrl)"
                    >复制</view
                  >
                  <view
                    class="rounded-xl bg-[#F97316] px-3 py-2 text-[10px] font-bold text-white active:opacity-80"
                    @click.stop="openLink(detail.officialUrl, '官网')"
                    >打开</view
                  >
                </view>
              </view>

              <view
                v-if="detail.repoUrl"
                class="flex items-center justify-between rounded-2xl border border-gray-100 bg-gray-50 p-3"
              >
                <view class="flex min-w-0 items-center space-x-2">
                  <view class="i-mdi-source-repository text-lg text-slate-800"></view>
                  <view class="min-w-0">
                    <view class="text-xs font-bold text-gray-900">仓库</view>
                    <view class="mt-1 text-[10px] text-gray-500 truncate">{{ detail.repoUrl }}</view>
                  </view>
                </view>
                <view class="ml-3 flex items-center space-x-2">
                  <view
                    class="rounded-xl bg-white px-3 py-2 text-[10px] font-bold text-slate-900 border border-gray-200 active:opacity-70"
                    @click.stop="copyLink(detail.repoUrl)"
                    >复制</view
                  >
                  <view
                    class="rounded-xl bg-[#F97316] px-3 py-2 text-[10px] font-bold text-white active:opacity-80"
                    @click.stop="openLink(detail.repoUrl, '仓库')"
                    >打开</view
                  >
                </view>
              </view>
            </view>
          </view>

          <!-- Downloads -->
          <view class="rounded-2xl bg-white p-4 shadow-sm border border-gray-100">
            <view class="flex items-center justify-between">
              <view class="flex items-center space-x-2">
                <view class="i-mdi-download text-lg text-slate-900"></view>
                <text class="text-sm font-bold text-gray-900">多平台下载</text>
              </view>
              <view class="text-[10px] text-gray-400">点击打开或复制链接</view>
            </view>

            <view v-if="!detail.downloads?.length" class="pt-3 text-xs text-gray-500">
              暂无下载配置
            </view>

            <view v-else class="mt-3 space-y-2">
              <view
                v-for="d in detail.downloads"
                :key="`${d.platform}-${d.downloadUrl}`"
                class="flex items-center rounded-2xl border border-gray-100 bg-gray-50 p-3"
              >
                <view
                  class="flex size-10 items-center justify-center rounded-2xl bg-slate-950 text-white"
                >
                  <view :class="platformIcon(d.platform)" class="text-xl"></view>
                </view>

                <view class="ml-3 flex-1 overflow-hidden">
                  <view class="flex items-center justify-between">
                    <view class="text-xs font-bold text-gray-900 truncate pr-2">
                      {{ platformName(d.platform) }}
                      <text v-if="d.version" class="ml-1 text-[10px] text-gray-500 font-medium"
                        >v{{ d.version }}</text
                      >
                    </view>
                    <view class="text-[10px] text-gray-400">{{ d.remark || "" }}</view>
                  </view>
                  <view class="mt-1 text-[10px] text-gray-500 truncate">
                    {{ d.downloadUrl }}
                  </view>
                </view>

                <view class="ml-3 flex items-center space-x-2">
                  <view
                    class="rounded-xl bg-white px-3 py-2 text-[10px] font-bold text-slate-900 border border-gray-200 active:opacity-70"
                    @click.stop="copyLink(d.downloadUrl)"
                    >复制</view
                  >
                  <view
                    class="rounded-xl bg-[#F97316] px-3 py-2 text-[10px] font-bold text-white active:opacity-80"
                    @click.stop="openLink(d.downloadUrl, platformName(d.platform))"
                    >打开</view
                  >
                </view>
              </view>
            </view>
          </view>

          <!-- Resources -->
          <view class="rounded-2xl bg-white p-4 shadow-sm border border-gray-100">
            <view class="flex items-center justify-between">
              <view class="flex items-center space-x-2">
                <view class="i-mdi-link-variant text-lg text-slate-900"></view>
                <text class="text-sm font-bold text-gray-900">相关资源</text>
              </view>
              <view class="text-[10px] text-gray-400">仅 URL</view>
            </view>

            <view v-if="!detail.resources?.length" class="pt-3 text-xs text-gray-500">
              暂无资源
            </view>

            <view v-else class="mt-3 space-y-2">
              <view
                v-for="r in detail.resources"
                :key="`${r.resourceType}-${r.resourceUrl}`"
                class="flex items-center rounded-2xl border border-gray-100 bg-gray-50 p-3"
              >
                <view class="flex size-10 items-center justify-center rounded-2xl bg-slate-950 text-white">
                  <view :class="resourceIcon(r.resourceType)" class="text-xl"></view>
                </view>

                <view class="ml-3 flex-1 overflow-hidden">
                  <view class="flex items-center justify-between">
                    <view class="text-xs font-bold text-gray-900 truncate pr-2">
                      {{ r.title || resourceTypeName(r.resourceType) }}
                    </view>
                    <view class="text-[10px] text-gray-400">
                      {{ r.remark || "" }}
                    </view>
                  </view>
                  <view class="mt-1 text-[10px] text-gray-500 truncate">
                    {{ r.resourceUrl }}
                  </view>
                </view>

                <view class="ml-3 flex items-center space-x-2">
                  <view
                    class="rounded-xl bg-white px-3 py-2 text-[10px] font-bold text-slate-900 border border-gray-200 active:opacity-70"
                    @click.stop="copyLink(r.resourceUrl)"
                    >复制</view
                  >
                  <view
                    class="rounded-xl bg-[#F97316] px-3 py-2 text-[10px] font-bold text-white active:opacity-80"
                    @click.stop="openLink(r.resourceUrl, r.title || resourceTypeName(r.resourceType))"
                    >打开</view
                  >
                </view>
              </view>
            </view>
          </view>

          <!-- Tabs -->
          <view class="flex items-center space-x-2">
            <view
              class="flex-1 rounded-2xl px-4 py-3 text-center text-xs font-extrabold border transition-all"
              :class="
                activeTab === 'desc'
                  ? 'bg-slate-950 text-white border-slate-950'
                  : 'bg-white text-gray-700 border-gray-200'
              "
              @click="activeTab = 'desc'"
              >介绍</view
            >
            <view
              class="flex-1 rounded-2xl px-4 py-3 text-center text-xs font-extrabold border transition-all"
              :class="
                activeTab === 'usage'
                  ? 'bg-slate-950 text-white border-slate-950'
                  : 'bg-white text-gray-700 border-gray-200'
              "
              @click="activeTab = 'usage'"
              >使用说明</view
            >
          </view>

          <!-- Markdown -->
          <view class="rounded-2xl bg-white p-4 shadow-sm border border-gray-100">
            <view v-if="loading" class="h-40 rounded-xl bg-gray-50 animate-pulse"></view>
            <view v-else class="markdown">
              <rich-text :nodes="activeHtml"></rich-text>
            </view>
          </view>
        </view>
      </scroll-view>
    </view>
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";

import { getPortalSoftwareDetail } from "@/api/software";
import { mdToHtml } from "@/utils/markdown";

const { proxy } = getCurrentInstance();

const loading = ref(true);
const activeTab = ref("desc");
const softwareId = ref(null);

const detail = ref({
  softwareId: undefined,
  categoryId: undefined,
  categoryName: "",
  softwareName: "",
  shortDesc: "",
  iconUrl: "",
  officialUrl: "",
  repoUrl: "",
  author: "",
  team: "",
  license: "",
  openSource: "0",
  tags: "",
  descriptionMd: "",
  usageMd: "",
  updateTime: "",
  downloads: [],
  resources: [],
});

const activeHtml = computed(() => {
  const md = activeTab.value === "usage" ? detail.value.usageMd : detail.value.descriptionMd;
  return mdToHtml(md || "");
});

function tagList(row) {
  const raw = row?.tags;
  if (!raw) return [];
  return String(raw)
    .replace(/，/g, ",")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
}

const detailTags = computed(() => tagList(detail.value).slice(0, 2));
const detailTagsAll = computed(() => tagList(detail.value));

function formatDate(v) {
  if (!v) return "";
  const d = new Date(v);
  if (Number.isNaN(d.getTime())) return "";
  const pad = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

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

function platformIcon(p) {
  const map = {
    windows: "i-mdi-microsoft-windows",
    mac: "i-mdi-apple",
    linux: "i-mdi-linux",
    android: "i-mdi-android",
    ios: "i-mdi-apple-ios",
    web: "i-mdi-web",
    other: "i-mdi-package-variant-closed",
  };
  return map[p] || "i-mdi-download";
}

function resourceTypeName(t) {
  const map = {
    screenshot: "截图",
    doc: "文档",
    link: "链接",
    video: "视频",
    other: "其他",
  };
  return map[t] || "资源";
}

function resourceIcon(t) {
  const map = {
    screenshot: "i-mdi-image-outline",
    doc: "i-mdi-file-document-outline",
    link: "i-mdi-link-variant",
    video: "i-mdi-video-outline",
    other: "i-mdi-package-variant",
  };
  return map[t] || "i-mdi-link-variant";
}

function copyLink(url) {
  if (!url) return;
  uni.setClipboardData({
    data: url,
    success: () => proxy.$modal?.msgSuccess?.("已复制链接"),
  });
}

function openLink(url, title) {
  if (!url) return;
  const t = title || detail.value.softwareName || "链接";
  uni.navigateTo({
    url: `/pages/common/webview/index?url=${encodeURIComponent(url)}&title=${encodeURIComponent(t)}`,
  });
}

async function fetchDetail() {
  if (!softwareId.value) return;
  loading.value = true;
  const res = await getPortalSoftwareDetail(softwareId.value);
  detail.value = res.data || detail.value;
  loading.value = false;
}

function reload() {
  fetchDetail().catch(() => {});
}

onLoad((options) => {
  softwareId.value = options.softwareId ? Number(options.softwareId) : null;
  fetchDetail()
    .catch(() => {
      proxy.$modal?.msg?.("加载失败，请稍后重试");
    })
    .finally(() => {
      loading.value = false;
    });
});
</script>

<style>
page {
  height: 100%;
  background-color: #0b0f14;
}

.markdown {
  font-size: 14px;
  color: #111827;
  line-height: 1.75;
}

.markdown h1,
.markdown h2,
.markdown h3 {
  font-weight: 800;
  line-height: 1.25;
  margin: 12px 0 8px;
}

.markdown h1 {
  font-size: 18px;
}

.markdown h2 {
  font-size: 16px;
}

.markdown h3 {
  font-size: 15px;
}

.markdown p {
  margin: 8px 0;
  color: #374151;
}

.markdown ul {
  padding-left: 18px;
  margin: 8px 0;
}

.markdown li {
  margin: 4px 0;
  color: #374151;
}

.markdown code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
    "Liberation Mono", "Courier New", monospace;
  font-size: 12px;
  padding: 0 6px;
  border-radius: 8px;
  background: #f3f4f6;
  color: #0f172a;
}
</style>
