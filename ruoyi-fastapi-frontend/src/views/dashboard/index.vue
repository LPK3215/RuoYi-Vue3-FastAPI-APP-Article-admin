<template>
  <div class="app-container dashboard">
    <section class="hero" aria-label="Dashboard header">
      <div class="hero__left">
        <div class="hero__identity">
          <el-avatar :src="userStore.avatar" :size="44" class="hero__avatar" />
          <div class="hero__text">
            <div class="hero__title">
              <span class="hero__greeting">{{ greeting }}</span>
              <span class="hero__name">{{ displayName }}</span>
            </div>
            <div class="hero__subtitle">
              <span class="hero__app">{{ APP_TITLE }}</span>
              <span class="hero__dot">•</span>
              <span class="hero__date">{{ todayText }}</span>
              <template v-if="envText">
                <span class="hero__dot">•</span>
                <span class="hero__env">{{ envText }}</span>
              </template>
            </div>
          </div>
        </div>

        <div class="hero__quick">
          <el-button type="primary" :icon="Box" @click="go('/software/item')">
            软件列表
          </el-button>
          <el-button :icon="Grid" @click="go('/software/category')">
            分类管理
          </el-button>
          <el-button :icon="RefreshRight" plain @click="loadAll">
            刷新数据
          </el-button>
        </div>
      </div>

      <div class="hero__right">
        <div class="hero__chips">
          <el-tag effect="plain" size="large" class="chip">
            <span class="chip__k">主题</span>
            <span class="chip__v">{{ settingsStore.isDark ? "暗色" : "亮色" }}</span>
          </el-tag>
          <el-tag effect="plain" size="large" class="chip">
            <span class="chip__k">状态</span>
            <span class="chip__v">{{ healthText }}</span>
          </el-tag>
        </div>
        <div class="hero__note">
          <span class="hero__noteLabel">提示</span>
          <span class="hero__noteText">
            点击 KPI / 维度分布 / 数据质量卡片，可直接跳转到「软件列表」并自动带筛选，快速定位并修复数据。
          </span>
        </div>
      </div>
    </section>

    <el-row :gutter="16" class="kpi">
      <el-col :xs="24" :sm="12" :lg="6">
        <div class="kpiCard kpiCard--total" role="button" tabindex="0" @click="go('/software/item')">
          <div class="kpiCard__icon">
            <el-icon><Box /></el-icon>
          </div>
          <div class="kpiCard__body">
            <div class="kpiCard__label">软件总数</div>
            <div class="kpiCard__value">
              <el-skeleton v-if="loading.kpi" animated :rows="0">
                <template #template>
                  <el-skeleton-item variant="text" style="width: 88px; height: 28px" />
                </template>
              </el-skeleton>
              <span v-else>{{ kpi.softwareTotal }}</span>
            </div>
            <div class="kpiCard__hint">草稿 / 上架 / 下架合计</div>
          </div>
        </div>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <div class="kpiCard kpiCard--published" role="button" tabindex="0" @click="go('/software/item')">
          <div class="kpiCard__icon">
            <el-icon><Promotion /></el-icon>
          </div>
          <div class="kpiCard__body">
            <div class="kpiCard__label">上架中</div>
            <div class="kpiCard__value">
              <el-skeleton v-if="loading.kpi" animated :rows="0">
                <template #template>
                  <el-skeleton-item variant="text" style="width: 72px; height: 28px" />
                </template>
              </el-skeleton>
              <span v-else>{{ kpi.published }}</span>
            </div>
            <div class="kpiCard__hint">用户可见内容</div>
          </div>
        </div>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <div class="kpiCard kpiCard--draft" role="button" tabindex="0" @click="go('/software/item')">
          <div class="kpiCard__icon">
            <el-icon><EditPen /></el-icon>
          </div>
          <div class="kpiCard__body">
            <div class="kpiCard__label">草稿待发布</div>
            <div class="kpiCard__value">
              <el-skeleton v-if="loading.kpi" animated :rows="0">
                <template #template>
                  <el-skeleton-item variant="text" style="width: 72px; height: 28px" />
                </template>
              </el-skeleton>
              <span v-else>{{ kpi.draft }}</span>
            </div>
            <div class="kpiCard__hint">建议优先处理</div>
          </div>
        </div>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <div class="kpiCard kpiCard--category" role="button" tabindex="0" @click="go('/software/category')">
          <div class="kpiCard__icon">
            <el-icon><Grid /></el-icon>
          </div>
          <div class="kpiCard__body">
            <div class="kpiCard__label">分类数</div>
            <div class="kpiCard__value">
              <el-skeleton v-if="loading.kpi" animated :rows="0">
                <template #template>
                  <el-skeleton-item variant="text" style="width: 72px; height: 28px" />
                </template>
              </el-skeleton>
              <span v-else>{{ kpi.categories }}</span>
            </div>
            <div class="kpiCard__hint">用于导航与聚合</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="grid">
      <el-col :xs="24" :lg="10">
        <el-card class="panel" shadow="never">
          <template #header>
            <div class="panel__header">
              <span class="panel__title">发布状态分布</span>
              <span class="panel__meta">上架 / 草稿 / 下架</span>
            </div>
          </template>
          <div class="panel__body">
            <div v-if="loading.kpi" class="panel__skeleton">
              <el-skeleton animated>
                <template #template>
                  <el-skeleton-item variant="rect" style="height: 240px" />
                </template>
              </el-skeleton>
            </div>
            <div v-else ref="statusChartEl" class="chart" />
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="14">
        <el-card class="panel" shadow="never">
          <template #header>
            <div class="panel__header">
              <span class="panel__title">最近更新</span>
              <span class="panel__meta">点击可进入详情</span>
            </div>
          </template>
          <div class="panel__body">
            <el-skeleton v-if="loading.recent" animated :rows="4" />
            <el-empty v-else-if="!recent.length" description="暂无数据" />
            <div v-else class="recent">
              <button
                v-for="item in recent"
                :key="String(item.softwareId)"
                class="recentItem"
                type="button"
                @click="goDetail(item)"
              >
                <div class="recentItem__main">
                  <div class="recentItem__title">
                    <span class="recentItem__name" :title="item.softwareName">
                      {{ item.softwareName || "-" }}
                    </span>
                    <el-tag :type="publishTagType(item.publishStatus)" size="small" effect="plain">
                      {{ publishStatusLabel(item.publishStatus) }}
                    </el-tag>
                  </div>
                  <div class="recentItem__desc">
                    {{ item.shortDesc || "—" }}
                  </div>
                </div>
                <div class="recentItem__meta">
                  <span class="recentItem__time">
                    {{ formatTime(item.updateTime) }}
                  </span>
                  <el-icon class="recentItem__arrow"><ArrowRight /></el-icon>
                </div>
              </button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="grid">
      <el-col :xs="24" :lg="14">
        <el-card class="panel" shadow="never">
          <template #header>
            <div class="panel__header">
              <span class="panel__title">草稿待处理</span>
              <span class="panel__meta">快速回到可发布状态</span>
            </div>
          </template>
          <div class="panel__body">
            <el-skeleton v-if="loading.drafts" animated :rows="4" />
            <el-empty v-else-if="!drafts.length" description="暂无草稿" />
            <div v-else class="drafts">
              <div class="draftItem" v-for="item in drafts" :key="String(item.softwareId)">
                <div class="draftItem__left">
                  <div class="draftItem__name" :title="item.softwareName">
                    {{ item.softwareName || "-" }}
                  </div>
                  <div class="draftItem__desc">{{ item.shortDesc || "—" }}</div>
                </div>
                <div class="draftItem__right">
                  <el-button size="small" type="primary" plain @click="goDetail(item)">
                    去完善
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="10">
        <el-card class="panel" shadow="never">
          <template #header>
            <div class="panel__header">
              <span class="panel__title">你的工作台</span>
              <span class="panel__meta">按你业务再扩展</span>
            </div>
          </template>
          <div class="panel__body">
            <div class="workbench">
              <div class="workbench__row">
                <div class="workbench__label">当前用户</div>
                <div class="workbench__value">{{ displayName }}</div>
              </div>
              <div class="workbench__row">
                <div class="workbench__label">权限角色</div>
                <div class="workbench__value">
                  <el-tag v-for="r in roles" :key="r" effect="plain" size="small" class="roleTag">
                    {{ r }}
                  </el-tag>
                  <span v-if="!roles.length" class="muted">—</span>
                </div>
              </div>
              <div class="workbench__row">
                <div class="workbench__label">快速入口</div>
                <div class="workbench__value workbench__links">
                  <button class="quickLink" type="button" @click="go('/software/item')">
                    软件列表
                  </button>
                  <button class="quickLink" type="button" @click="go('/software/category')">
                    分类管理
                  </button>
                  <button class="quickLink" type="button" @click="go('/system/user')">
                    用户管理
                  </button>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="grid">
      <el-col :xs="24" :lg="14">
        <el-card class="panel" shadow="never">
          <template #header>
            <div class="panel__header">
              <span class="panel__title">维度分布</span>
              <span class="panel__meta">点击任意项可跳转筛选</span>
            </div>
          </template>
          <div class="panel__body">
            <el-skeleton v-if="loading.kpi" animated :rows="4" />
            <el-empty
              v-else-if="
                !((facets.licenses || []).length || (facets.tags || []).length || (facets.platforms || []).length)
              "
              description="暂无统计"
            />
            <div v-else class="facetGrid">
              <div class="facetGroup">
                <div class="facetGroup__title">许可证</div>
                <button
                  v-for="item in (facets.licenses || []).slice(0, 6)"
                  :key="`lic_${item.value}`"
                  class="facetItem"
                  type="button"
                  :style="{ '--pct': facetPct(item.count, facetMax.licenses) }"
                  @click="goFacet('license', item.value)"
                >
                  <span class="facetItem__name" :title="item.value">{{ item.value }}</span>
                  <span class="facetItem__count">{{ item.count }}</span>
                </button>
              </div>

              <div class="facetGroup">
                <div class="facetGroup__title">标签</div>
                <button
                  v-for="item in (facets.tags || []).slice(0, 6)"
                  :key="`tag_${item.value}`"
                  class="facetItem facetItem--tag"
                  type="button"
                  :style="{ '--pct': facetPct(item.count, facetMax.tags) }"
                  @click="goFacet('tag', item.value)"
                >
                  <span class="facetItem__name" :title="item.value">{{ item.value }}</span>
                  <span class="facetItem__count">{{ item.count }}</span>
                </button>
              </div>

              <div class="facetGroup">
                <div class="facetGroup__title">平台</div>
                <button
                  v-for="item in (facets.platforms || []).slice(0, 6)"
                  :key="`plat_${item.value}`"
                  class="facetItem facetItem--platform"
                  type="button"
                  :style="{ '--pct': facetPct(item.count, facetMax.platforms) }"
                  @click="goFacet('platform', item.value)"
                >
                  <span class="facetItem__name" :title="item.value">{{ item.value }}</span>
                  <span class="facetItem__count">{{ item.count }}</span>
                </button>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="10">
        <el-card class="panel" shadow="never">
          <template #header>
            <div class="panel__header">
              <span class="panel__title">数据质量</span>
              <span class="panel__meta">点击可跳转到软件列表修复</span>
            </div>
          </template>
          <div class="panel__body">
            <el-skeleton v-if="loading.kpi" animated :rows="4" />
            <div v-else class="qualityGrid">
              <button
                class="qualityItem"
                :class="{ 'is-warn': quality.missingDownloads > 0 }"
                type="button"
                @click="goQuality('downloads')"
              >
                <span class="qualityItem__label">缺下载配置</span>
                <span class="qualityItem__value">{{ quality.missingDownloads }}</span>
              </button>
              <button
                class="qualityItem"
                :class="{ 'is-warn': quality.missingLicense > 0 }"
                type="button"
                @click="goQuality('license')"
              >
                <span class="qualityItem__label">缺许可证</span>
                <span class="qualityItem__value">{{ quality.missingLicense }}</span>
              </button>
              <button
                class="qualityItem"
                :class="{ 'is-warn': quality.missingIcon > 0 }"
                type="button"
                @click="goQuality('icon')"
              >
                <span class="qualityItem__label">缺图标</span>
                <span class="qualityItem__value">{{ quality.missingIcon }}</span>
              </button>
              <button
                class="qualityItem"
                :class="{ 'is-warn': quality.missingTags > 0 }"
                type="button"
                @click="goQuality('tags')"
              >
                <span class="qualityItem__label">缺标签</span>
                <span class="qualityItem__value">{{ quality.missingTags }}</span>
              </button>
              <button
                class="qualityItem"
                :class="{ 'is-warn': quality.missingShortDesc > 0 }"
                type="button"
                @click="goQuality('shortDesc')"
              >
                <span class="qualityItem__label">缺简述</span>
                <span class="qualityItem__value">{{ quality.missingShortDesc }}</span>
              </button>
              <button
                class="qualityItem"
                :class="{ 'is-warn': quality.missingOfficialUrl > 0 }"
                type="button"
                @click="goQuality('officialUrl')"
              >
                <span class="qualityItem__label">缺官网</span>
                <span class="qualityItem__value">{{ quality.missingOfficialUrl }}</span>
              </button>
              <button
                class="qualityItem qualityItem--full"
                :class="{ 'is-warn': quality.missingResources > 0 }"
                type="button"
                @click="goQuality('resources')"
              >
                <span class="qualityItem__label">缺资源（文档/截图/链接）</span>
                <span class="qualityItem__value">{{ quality.missingResources }}</span>
              </button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup name="Index">
import { APP_TITLE } from "@/config/brand";
import useUserStore from "@/store/modules/user";
import useSettingsStore from "@/store/modules/settings";
import { getSoftwareDashboardOverview } from "@/api/tool/software/dashboard";
import { parseTime } from "@/utils/ruoyi";
import * as echarts from "echarts";
import {
  ArrowRight,
  Box,
  EditPen,
  Grid,
  Promotion,
  RefreshRight,
} from "@element-plus/icons-vue";

const router = useRouter();
const userStore = useUserStore();
const settingsStore = useSettingsStore();

const displayName = computed(() => userStore.nickName || userStore.name || "你");

const roles = computed(() => {
  const raw = userStore.roles || [];
  return raw
    .map((r) => String(r || "").trim())
    .filter(Boolean)
    .slice(0, 6);
});

const greeting = computed(() => {
  const hour = new Date().getHours();
  if (hour < 6) return "凌晨好，";
  if (hour < 12) return "早上好，";
  if (hour < 14) return "中午好，";
  if (hour < 18) return "下午好，";
  return "晚上好，";
});

const todayText = computed(() => {
  const d = new Date();
  const dayMap = ["日", "一", "二", "三", "四", "五", "六"];
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd} 周${dayMap[d.getDay()]}`;
});

const envText = computed(() => {
  const env = import.meta.env.VITE_APP_ENV || import.meta.env.MODE;
  if (!env) return "";
  if (env === "production") return "生产环境";
  if (env === "development") return "开发环境";
  if (env === "staging") return "预发布";
  if (env === "docker") return "Docker";
  return env;
});

const loading = reactive({
  kpi: true,
  recent: true,
  drafts: true,
});

const kpi = reactive({
  softwareTotal: 0,
  published: 0,
  draft: 0,
  offline: 0,
  categories: 0,
});

const recent = ref([]);
const drafts = ref([]);
const facets = reactive({
  tags: [],
  licenses: [],
  authors: [],
  teams: [],
  platforms: [],
});
const quality = reactive({
  missingIcon: 0,
  missingLicense: 0,
  missingOfficialUrl: 0,
  missingShortDesc: 0,
  missingTags: 0,
  missingDownloads: 0,
  missingResources: 0,
});
const overviewError = ref("");

const healthText = computed(() => {
  if (loading.kpi || loading.recent || loading.drafts) return "同步中…";
  if (overviewError.value) return "异常";
  return "运行中";
});

function formatTime(val) {
  if (!val) return "-";
  try {
    return parseTime(val);
  } catch (e) {
    return String(val);
  }
}

function publishStatusLabel(value) {
  if (value === "1") return "上架";
  if (value === "2") return "下架";
  return "草稿";
}

function publishTagType(value) {
  if (value === "1") return "success";
  if (value === "2") return "info";
  return "warning";
}

function go(path, query) {
  if (!path) return;
  if (query && typeof query === "object") {
    router.push({ path, query });
    return;
  }
  router.push(path);
}

function goDetail(row) {
  const softwareId = row?.softwareId;
  if (!softwareId) return;
  router.push({ path: "/software/detail", query: { softwareId } });
}

const facetMax = computed(() => {
  const maxOf = (list) =>
    Math.max(
      1,
      ...(Array.isArray(list) ? list : []).map((x) => Number(x?.count || 0))
    );
  return {
    tags: maxOf(facets.tags),
    licenses: maxOf(facets.licenses),
    platforms: maxOf(facets.platforms),
  };
});

function facetPct(count, max) {
  const n = Number(count || 0);
  const m = Number(max || 1);
  return `${Math.round((n / m) * 100)}%`;
}

function goFacet(kind, value) {
  if (!value) return;
  if (kind === "tag") return go("/software/item", { tag: value });
  if (kind === "license") return go("/software/item", { license: value });
  if (kind === "platform") return go("/software/item", { platform: value });
}

function goQuality(kind) {
  if (kind === "downloads") return go("/software/item", { hasDownloads: "0" });
  if (kind === "license") return go("/software/item", { hasLicense: "0" });
  if (kind === "icon") return go("/software/item", { hasIcon: "0" });
  if (kind === "officialUrl") return go("/software/item", { hasOfficialUrl: "0" });
  if (kind === "shortDesc") return go("/software/item", { hasShortDesc: "0" });
  if (kind === "tags") return go("/software/item", { hasTags: "0" });
  if (kind === "resources") return go("/software/item", { hasResources: "0" });
}

async function loadOverview() {
  loading.kpi = true;
  loading.recent = true;
  loading.drafts = true;
  overviewError.value = "";
  try {
    const res = await getSoftwareDashboardOverview({ limit: 12, recentLimit: 6 });
    const data = res?.data || {};
    const nextKpi = data?.kpi || {};

    kpi.softwareTotal = Number(nextKpi?.softwareTotal || 0);
    kpi.published = Number(nextKpi?.published || 0);
    kpi.draft = Number(nextKpi?.draft || 0);
    kpi.offline = Number(nextKpi?.offline || 0);
    kpi.categories = Number(nextKpi?.categories || 0);

    recent.value = data?.recent || [];
    drafts.value = data?.drafts || [];

    Object.assign(facets, data?.facets || {});
    Object.assign(quality, data?.quality || {});
  } catch (e) {
    overviewError.value = "加载失败";
    recent.value = [];
    drafts.value = [];
  } finally {
    loading.kpi = false;
    loading.recent = false;
    loading.drafts = false;
  }
}

async function loadAll() {
  await loadOverview();
  await nextTick();
  renderStatusChart();
}

const statusChartEl = ref(null);
let statusChart;

function statusColors() {
  return settingsStore.isDark
    ? {
        published: "#22c55e",
        draft: "#f59e0b",
        offline: "#94a3b8",
        text: "#e2e8f0",
        muted: "rgba(226, 232, 240, 0.66)",
      }
    : {
        published: "#16a34a",
        draft: "#f59e0b",
        offline: "#64748b",
        text: "#0f172a",
        muted: "rgba(15, 23, 42, 0.60)",
      };
}

function buildStatusOption() {
  const c = statusColors();
  const total = Number(kpi.softwareTotal || 0);
  return {
    backgroundColor: "transparent",
    tooltip: {
      trigger: "item",
      formatter: "{b}<br/>{c}（{d}%）",
    },
    series: [
      {
        name: "发布状态",
        type: "pie",
        radius: ["58%", "82%"],
        center: ["50%", "46%"],
        avoidLabelOverlap: true,
        label: { show: false },
        labelLine: { show: false },
        itemStyle: {
          borderRadius: 10,
          borderColor: "rgba(0,0,0,0)",
          borderWidth: 2,
        },
        data: [
          {
            value: Number(kpi.published || 0),
            name: "上架",
            itemStyle: { color: c.published },
          },
          {
            value: Number(kpi.draft || 0),
            name: "草稿",
            itemStyle: { color: c.draft },
          },
          {
            value: Number(kpi.offline || 0),
            name: "下架",
            itemStyle: { color: c.offline },
          },
        ],
      },
    ],
    graphic: [
      {
        type: "text",
        left: "center",
        top: "40%",
        style: {
          text: String(total),
          fontSize: 30,
          fontWeight: 700,
          fill: c.text,
          fontFamily: "var(--app-font-sans)",
        },
      },
      {
        type: "text",
        left: "center",
        top: "52%",
        style: {
          text: "总量",
          fontSize: 12,
          fill: c.muted,
          fontFamily: "var(--app-font-sans)",
        },
      },
    ],
  };
}

function renderStatusChart() {
  if (!statusChartEl.value) return;
  const theme = settingsStore.isDark ? "dark" : undefined;

  try {
    if (statusChart) {
      statusChart.dispose();
      statusChart = undefined;
    }
    statusChart = echarts.init(statusChartEl.value, theme, {
      renderer: "canvas",
    });
    statusChart.setOption(buildStatusOption(), true);
  } catch (e) {
    // keep dashboard usable even if chart init fails
    console.warn("ECharts init failed:", e);
  }
}

const handleResize = () => statusChart?.resize?.();

watch(
  () => settingsStore.isDark,
  async () => {
    await nextTick();
    renderStatusChart();
  }
);

onMounted(async () => {
  window.addEventListener("resize", handleResize);
  await loadAll();
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
  statusChart?.dispose?.();
});
</script>

<style scoped lang="scss">
.dashboard {
  padding: 18px;
}

.hero {
  position: relative;
  display: grid;
  grid-template-columns: 1.3fr 0.7fr;
  gap: 16px;
  padding: 18px 18px 16px;
  border-radius: var(--app-radius-lg);
  border: 1px solid var(--app-border);
  background:
    radial-gradient(900px 260px at 8% 10%, rgba(14, 165, 233, 0.22) 0%, rgba(14, 165, 233, 0) 60%),
    radial-gradient(860px 260px at 92% 0%, rgba(99, 102, 241, 0.14) 0%, rgba(99, 102, 241, 0) 62%),
    linear-gradient(180deg, var(--app-surface-2), var(--app-surface));
  box-shadow: var(--app-shadow);
  overflow: hidden;
}

.hero::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image: linear-gradient(
      rgba(15, 23, 42, 0.05) 1px,
      transparent 1px
    ),
    linear-gradient(90deg, rgba(15, 23, 42, 0.05) 1px, transparent 1px);
  background-size: 18px 18px;
  opacity: 0.5;
  pointer-events: none;
  mask-image: radial-gradient(closest-side, rgba(0, 0, 0, 0.66), rgba(0, 0, 0, 0));
}

html.dark .hero::before {
  background-image: linear-gradient(
      rgba(226, 232, 240, 0.08) 1px,
      transparent 1px
    ),
    linear-gradient(90deg, rgba(226, 232, 240, 0.08) 1px, transparent 1px);
  opacity: 0.35;
}

.hero__left,
.hero__right {
  position: relative;
  z-index: 1;
}

.hero__identity {
  display: flex;
  align-items: center;
  gap: 12px;
}

.hero__text {
  min-width: 0;
}

.hero__title {
  display: flex;
  align-items: baseline;
  gap: 4px;
  font-size: 18px;
  font-weight: 750;
  letter-spacing: 0.2px;
}

.hero__name {
  max-width: 260px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.hero__subtitle {
  margin-top: 6px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  color: var(--el-text-color-regular);
  font-size: 13px;
}

.hero__dot {
  opacity: 0.5;
}

.hero__quick {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.hero__chips {
  display: flex;
  justify-content: flex-end;
  flex-wrap: wrap;
  gap: 10px;
}

.chip {
  border-color: var(--app-border) !important;
  background: rgba(255, 255, 255, 0.55);
}

html.dark .chip {
  background: rgba(11, 18, 32, 0.55);
}

.chip__k {
  opacity: 0.7;
  margin-right: 8px;
}

.chip__v {
  font-weight: 650;
}

.hero__note {
  margin-top: 12px;
  padding: 12px 12px;
  border-radius: 12px;
  border: 1px dashed var(--app-border);
  background: rgba(255, 255, 255, 0.42);
  color: var(--el-text-color-regular);
  line-height: 1.5;
}

html.dark .hero__note {
  background: rgba(11, 18, 32, 0.42);
}

.hero__noteLabel {
  font-weight: 700;
  margin-right: 8px;
  color: var(--el-text-color-primary);
}

.kpi {
  margin-top: 16px;
}

.kpiCard {
  border: 1px solid var(--app-border);
  border-radius: var(--app-radius-md);
  background: var(--app-surface);
  padding: 14px 14px;
  display: flex;
  gap: 12px;
  align-items: center;
  cursor: pointer;
  transition: box-shadow 220ms ease, border-color 220ms ease, background 220ms ease;
  user-select: none;
}

.kpiCard:focus {
  outline: 3px solid color-mix(in srgb, var(--el-color-primary) 22%, transparent);
  outline-offset: 2px;
}

.kpiCard:hover {
  box-shadow: 0 14px 30px rgba(15, 23, 42, 0.08);
  border-color: color-mix(in srgb, var(--el-color-primary) 20%, var(--app-border));
}

html.dark .kpiCard:hover {
  box-shadow: 0 18px 44px rgba(0, 0, 0, 0.55);
}

.kpiCard__icon {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  color: #ffffff;
  flex: 0 0 auto;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.18);
}

.kpiCard__body {
  min-width: 0;
}

.kpiCard__label {
  font-size: 13px;
  color: var(--el-text-color-regular);
}

.kpiCard__value {
  margin-top: 6px;
  font-size: 24px;
  font-weight: 800;
  letter-spacing: 0.2px;
  color: var(--el-text-color-primary);
  line-height: 1.1;
}

.kpiCard__hint {
  margin-top: 8px;
  font-size: 12px;
  color: var(--el-text-color-regular);
  opacity: 0.85;
}

.kpiCard--total .kpiCard__icon {
  background: linear-gradient(135deg, #0ea5e9, #6366f1);
}

.kpiCard--published .kpiCard__icon {
  background: linear-gradient(135deg, #22c55e, #16a34a);
}

.kpiCard--draft .kpiCard__icon {
  background: linear-gradient(135deg, #f59e0b, #f97316);
}

.kpiCard--category .kpiCard__icon {
  background: linear-gradient(135deg, #a855f7, #6366f1);
}

.grid {
  margin-top: 16px;
}

.panel {
  border-radius: var(--app-radius-md);
  background: var(--app-surface);
}

.panel__header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
}

.panel__title {
  font-weight: 800;
  letter-spacing: 0.2px;
}

.panel__meta {
  font-size: 12px;
  color: var(--el-text-color-regular);
}

.chart {
  height: 260px;
  width: 100%;
}

.recent {
  display: grid;
  gap: 10px;
}

.recentItem {
  width: 100%;
  display: flex;
  justify-content: space-between;
  gap: 12px;
  border: 1px solid var(--app-border);
  border-radius: 14px;
  padding: 12px 12px;
  background: color-mix(in srgb, var(--app-surface) 92%, var(--app-bg));
  cursor: pointer;
  transition: border-color 220ms ease, box-shadow 220ms ease;
  text-align: left;
}

.recentItem:hover {
  border-color: color-mix(in srgb, var(--el-color-primary) 22%, var(--app-border));
  box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08);
}

.recentItem__main {
  min-width: 0;
}

.recentItem__title {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.recentItem__name {
  font-weight: 750;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recentItem__desc {
  margin-top: 6px;
  color: var(--el-text-color-regular);
  font-size: 12px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.recentItem__meta {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 0 0 auto;
  color: var(--el-text-color-regular);
  font-size: 12px;
}

.recentItem__arrow {
  opacity: 0.7;
}

.drafts {
  display: grid;
  gap: 10px;
}

.draftItem {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 12px;
  border: 1px solid var(--app-border);
  border-radius: 14px;
  background: color-mix(in srgb, var(--app-surface) 92%, var(--app-bg));
}

.draftItem__left {
  min-width: 0;
}

.draftItem__name {
  font-weight: 750;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.draftItem__desc {
  margin-top: 6px;
  font-size: 12px;
  color: var(--el-text-color-regular);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.workbench {
  display: grid;
  gap: 12px;
}

.workbench__row {
  display: grid;
  grid-template-columns: 96px 1fr;
  gap: 12px;
  align-items: start;
}

.workbench__label {
  color: var(--el-text-color-regular);
  font-size: 12px;
}

.workbench__value {
  font-weight: 650;
  color: var(--el-text-color-primary);
  min-width: 0;
}

.workbench__links {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.quickLink {
  border: 1px solid var(--app-border);
  background: transparent;
  border-radius: 999px;
  padding: 6px 10px;
  cursor: pointer;
  color: var(--el-text-color-primary);
  transition: border-color 220ms ease, background 220ms ease;
}

.quickLink:hover {
  border-color: color-mix(in srgb, var(--el-color-primary) 30%, var(--app-border));
  background: color-mix(in srgb, var(--el-color-primary) 10%, transparent);
}

.roleTag {
  margin-right: 8px;
  margin-bottom: 8px;
}

.muted {
  color: var(--el-text-color-regular);
  opacity: 0.8;
}

.facetGrid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.facetGroup__title {
  margin-bottom: 8px;
  font-size: 12px;
  color: var(--el-text-color-regular);
}

.facetItem {
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 10px 10px 18px;
  border: 1px solid var(--app-border);
  border-radius: 14px;
  background: color-mix(in srgb, var(--app-surface) 92%, var(--app-bg));
  cursor: pointer;
  text-align: left;
  transition: box-shadow 200ms ease, border-color 200ms ease, transform 200ms ease;
}

.facetItem::before {
  content: "";
  position: absolute;
  left: 10px;
  right: 10px;
  bottom: 9px;
  height: 6px;
  border-radius: 999px;
  background: rgba(15, 23, 42, 0.06);
}

html.dark .facetItem::before {
  background: rgba(255, 255, 255, 0.1);
}

.facetItem::after {
  content: "";
  position: absolute;
  left: 10px;
  bottom: 9px;
  height: 6px;
  width: var(--pct, 0%);
  border-radius: 999px;
  background: linear-gradient(
    90deg,
    color-mix(in srgb, var(--el-color-primary) 70%, #22c55e),
    var(--el-color-primary)
  );
}

.facetItem--tag::after {
  background: linear-gradient(90deg, #22c55e, color-mix(in srgb, #22c55e 35%, var(--el-color-primary)));
}

.facetItem--platform::after {
  background: linear-gradient(90deg, #6366f1, color-mix(in srgb, #6366f1 35%, var(--el-color-primary)));
}

.facetItem:hover {
  transform: translateY(-1px);
  border-color: color-mix(in srgb, var(--el-color-primary) 22%, var(--app-border));
  box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08);
}

html.dark .facetItem:hover {
  box-shadow: 0 18px 44px rgba(0, 0, 0, 0.55);
}

.facetItem:focus {
  outline: 3px solid color-mix(in srgb, var(--el-color-primary) 18%, transparent);
  outline-offset: 2px;
}

.facetItem__name {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 650;
}

.facetItem__count {
  flex: 0 0 auto;
  font-family: var(--app-font-mono);
  font-size: 12px;
  color: var(--el-text-color-regular);
}

.qualityGrid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.qualityItem {
  border: 1px solid var(--app-border);
  border-radius: 14px;
  padding: 12px 12px;
  background: color-mix(in srgb, var(--app-surface) 92%, var(--app-bg));
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  cursor: pointer;
  transition: border-color 200ms ease, box-shadow 200ms ease, transform 200ms ease, background 200ms ease;
  text-align: left;
}

.qualityItem:hover {
  transform: translateY(-1px);
  border-color: color-mix(in srgb, var(--el-color-primary) 20%, var(--app-border));
  box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08);
}

html.dark .qualityItem:hover {
  box-shadow: 0 18px 44px rgba(0, 0, 0, 0.55);
}

.qualityItem.is-warn {
  border-color: color-mix(in srgb, var(--el-color-warning) 40%, var(--app-border));
  background: linear-gradient(
    180deg,
    color-mix(in srgb, var(--el-color-warning) 10%, transparent),
    color-mix(in srgb, var(--app-surface) 92%, var(--app-bg))
  );
}

.qualityItem__label {
  font-size: 12px;
  color: var(--el-text-color-regular);
}

.qualityItem__value {
  font-size: 20px;
  font-weight: 850;
  letter-spacing: 0.2px;
}

.qualityItem--full {
  grid-column: 1 / -1;
}

@media (max-width: 992px) {
  .hero {
    grid-template-columns: 1fr;
  }
  .hero__chips {
    justify-content: flex-start;
  }
  .facetGrid {
    grid-template-columns: 1fr;
  }
}
</style>
