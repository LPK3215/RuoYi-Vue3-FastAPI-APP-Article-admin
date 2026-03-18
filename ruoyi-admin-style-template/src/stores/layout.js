import { computed, ref, watch } from 'vue'
import { defineStore } from 'pinia'
import { handleThemeStyle } from '@/utils/theme'

const STORAGE_KEY = 'ruoyi-admin-style-template.layout'
const APP_TITLE = 'RuoYi Admin Style Template'

function getSystemDarkMode() {
  return typeof window !== 'undefined' &&
    typeof window.matchMedia === 'function' &&
    window.matchMedia('(prefers-color-scheme: dark)').matches
}

function getDefaultState() {
  return {
    themeColor: '#0ea5e9',
    isDark: getSystemDarkMode(),
    navType: 1,
    tagsView: true,
    tagsIcon: true,
    fixedHeader: true,
    sidebarLogo: true,
    dynamicTitle: false,
    footerVisible: true,
    footerContent: 'RuoYi Admin Style Template · 后台布局主题母版',
    topGroup: 'workspace',
  }
}

function loadStoredState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : {}
  } catch {
    return {}
  }
}

export const useLayoutStore = defineStore('layout', () => {
  const initial = {
    ...getDefaultState(),
    ...loadStoredState(),
  }

  const themeColor = ref(initial.themeColor)
  const isDark = ref(Boolean(initial.isDark))
  const navType = ref(initial.navType)
  const tagsView = ref(Boolean(initial.tagsView))
  const tagsIcon = ref(Boolean(initial.tagsIcon))
  const fixedHeader = ref(Boolean(initial.fixedHeader))
  const sidebarLogo = ref(Boolean(initial.sidebarLogo))
  const dynamicTitle = ref(Boolean(initial.dynamicTitle))
  const footerVisible = ref(Boolean(initial.footerVisible))
  const footerContent = ref(initial.footerContent)
  const topGroup = ref(initial.topGroup)

  const device = ref('desktop')
  const sidebarOpened = ref(navType.value !== 3)
  const settingsVisible = ref(false)
  const visitedViews = ref([])

  const sidebarHidden = computed(() => navType.value === 3)

  function persistLayout() {
    const payload = {
      themeColor: themeColor.value,
      isDark: isDark.value,
      navType: navType.value,
      tagsView: tagsView.value,
      tagsIcon: tagsIcon.value,
      fixedHeader: fixedHeader.value,
      sidebarLogo: sidebarLogo.value,
      dynamicTitle: dynamicTitle.value,
      footerVisible: footerVisible.value,
      footerContent: footerContent.value,
      topGroup: topGroup.value,
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload))
  }

  function applyAppearance() {
    document.documentElement.classList.toggle('dark', isDark.value)
    document.documentElement.style.colorScheme = isDark.value ? 'dark' : 'light'
    handleThemeStyle(themeColor.value)
  }

  function syncSidebarByLayout() {
    if (device.value === 'mobile') {
      sidebarOpened.value = false
      return
    }

    if (navType.value === 3) {
      sidebarOpened.value = false
      return
    }

    sidebarOpened.value = true
  }

  function setDevice(nextDevice) {
    device.value = nextDevice
    syncSidebarByLayout()
  }

  function toggleSidebar() {
    if (navType.value === 3) return
    sidebarOpened.value = !sidebarOpened.value
  }

  function closeSidebar() {
    sidebarOpened.value = false
  }

  function setThemeMode(nextIsDark) {
    isDark.value = Boolean(nextIsDark)
  }

  function toggleTheme() {
    isDark.value = !isDark.value
  }

  function setThemeColor(nextColor) {
    if (!nextColor) return
    themeColor.value = nextColor.toLowerCase()
  }

  function setNavType(nextType) {
    navType.value = nextType
    syncSidebarByLayout()
  }

  function setTopGroup(groupKey) {
    topGroup.value = groupKey
  }

  function openSettings() {
    settingsVisible.value = true
  }

  function closeSettings() {
    settingsVisible.value = false
  }

  function addVisitedView(route) {
    if (!route?.meta?.title) return
    if (visitedViews.value.some((item) => item.path === route.path)) return
    visitedViews.value.push({
      path: route.path,
      title: route.meta.title,
      icon: route.meta.icon || '',
      affix: Boolean(route.meta.affix),
    })
  }

  function removeVisitedView(path) {
    visitedViews.value = visitedViews.value.filter((item) => item.affix || item.path !== path)
  }

  function closeOtherViews(path) {
    visitedViews.value = visitedViews.value.filter((item) => item.affix || item.path === path)
  }

  function applyRouteTitle(routeTitle) {
    document.title = dynamicTitle.value && routeTitle ? `${routeTitle} · ${APP_TITLE}` : APP_TITLE
  }

  function resetSettings() {
    const defaults = getDefaultState()
    themeColor.value = defaults.themeColor
    isDark.value = defaults.isDark
    navType.value = defaults.navType
    tagsView.value = defaults.tagsView
    tagsIcon.value = defaults.tagsIcon
    fixedHeader.value = defaults.fixedHeader
    sidebarLogo.value = defaults.sidebarLogo
    dynamicTitle.value = defaults.dynamicTitle
    footerVisible.value = defaults.footerVisible
    footerContent.value = defaults.footerContent
    topGroup.value = defaults.topGroup
    syncSidebarByLayout()
  }

  watch(
    [themeColor, isDark, navType, tagsView, tagsIcon, fixedHeader, sidebarLogo, dynamicTitle, footerVisible, footerContent, topGroup],
    () => {
      applyAppearance()
      persistLayout()
    },
    { immediate: true },
  )

  return {
    themeColor,
    isDark,
    navType,
    tagsView,
    tagsIcon,
    fixedHeader,
    sidebarLogo,
    dynamicTitle,
    footerVisible,
    footerContent,
    topGroup,
    device,
    sidebarOpened,
    sidebarHidden,
    settingsVisible,
    visitedViews,
    setDevice,
    toggleSidebar,
    closeSidebar,
    setThemeMode,
    toggleTheme,
    setThemeColor,
    setNavType,
    setTopGroup,
    openSettings,
    closeSettings,
    addVisitedView,
    removeVisitedView,
    closeOtherViews,
    applyRouteTitle,
    persistLayout,
    resetSettings,
  }
})
