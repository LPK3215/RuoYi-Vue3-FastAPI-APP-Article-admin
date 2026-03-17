import defaultSettings from '@/settings'
import { useDark, useToggle } from '@vueuse/core'
import { useDynamicTitle } from '@/utils/dynamicTitle'

const isDark = useDark()
const toggleDark = useToggle(isDark)

const { sideTheme, showSettings, navType, tagsView, tagsIcon, fixedHeader, sidebarLogo, dynamicTitle, footerVisible, footerContent } = defaultSettings

const storageSetting = JSON.parse(localStorage.getItem('layout-setting')) || ''
const themeLinkedSideTheme = isDark.value ? 'theme-dark' : 'theme-light'

const useSettingsStore = defineStore(
  'settings',
  {
    state: () => ({
      title: '',
      theme: storageSetting.theme || '#0ea5e9',
      // 侧边栏主题：默认跟随“主题模式”（暗黑/亮色），避免出现“页面亮色但菜单一直黑”的割裂感
      sideTheme: themeLinkedSideTheme,
      showSettings: showSettings,
      navType: storageSetting.navType === undefined ? navType : storageSetting.navType,
      tagsView: storageSetting.tagsView === undefined ? tagsView : storageSetting.tagsView,
      tagsIcon: storageSetting.tagsIcon === undefined ? tagsIcon : storageSetting.tagsIcon,
      fixedHeader: storageSetting.fixedHeader === undefined ? fixedHeader : storageSetting.fixedHeader,
      sidebarLogo: storageSetting.sidebarLogo === undefined ? sidebarLogo : storageSetting.sidebarLogo,
      dynamicTitle: storageSetting.dynamicTitle === undefined ? dynamicTitle : storageSetting.dynamicTitle,
      footerVisible: storageSetting.footerVisible === undefined ? footerVisible : storageSetting.footerVisible,
      footerContent: footerContent,
      isDark: isDark.value
    }),
    actions: {
      // 修改布局设置
      changeSetting(data) {
        const { key, value } = data
        if (this.hasOwnProperty(key)) {
          this[key] = value
        }
      },
      // 设置网页标题
      setTitle(title) {
        this.title = title
        useDynamicTitle()
      },
      // 设置主题模式（暗黑/亮色），并同步侧边栏主题
      setThemeMode(nextIsDark) {
        const target = Boolean(nextIsDark)
        const was = this.isDark
        this.isDark = target
        if (was !== target) {
          toggleDark(target)
        }
        this.sideTheme = target ? 'theme-dark' : 'theme-light'

        // 侧边栏主题同步写入 layout-setting，避免刷新后回到旧配置
        try {
          const raw = localStorage.getItem('layout-setting')
          const cached = raw ? JSON.parse(raw) : {}
          const next = typeof cached === 'object' && cached !== null ? cached : {}
          next.sideTheme = this.sideTheme
          localStorage.setItem('layout-setting', JSON.stringify(next))
        } catch (e) {}
      },
      // 切换暗黑模式
      toggleTheme() {
        this.setThemeMode(!this.isDark)
      }
    }
  })

export default useSettingsStore
