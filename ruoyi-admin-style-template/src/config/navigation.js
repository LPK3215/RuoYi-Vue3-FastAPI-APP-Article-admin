export const navigationGroups = [
  {
    key: 'workspace',
    label: '工作台',
    icon: 'Monitor',
    description: '概览、布局说明与日常入口',
    items: [
      {
        path: '/dashboard',
        name: 'dashboard',
        title: '仪表盘',
        icon: 'Odometer',
        affix: true,
        component: () => import('@/views/DashboardView.vue'),
      },
      {
        path: '/layout-guide',
        name: 'layoutGuide',
        title: '布局导览',
        icon: 'Grid',
        component: () => import('@/views/LayoutGuideView.vue'),
      },
    ],
  },
  {
    key: 'visual',
    label: '风格预览',
    icon: 'Brush',
    description: '主题、组件与交互效果演示',
    items: [
      {
        path: '/theme-studio',
        name: 'themeStudio',
        title: '主题实验室',
        icon: 'MagicStick',
        component: () => import('@/views/ThemeStudioView.vue'),
      },
      {
        path: '/components-gallery',
        name: 'componentsGallery',
        title: '组件展示',
        icon: 'Collection',
        component: () => import('@/views/ComponentsGalleryView.vue'),
      },
    ],
  },
  {
    key: 'system',
    label: '系统',
    icon: 'Setting',
    description: '用户资料与模板说明',
    items: [
      {
        path: '/profile',
        name: 'profile',
        title: '管理员资料',
        icon: 'User',
        component: () => import('@/views/ProfileView.vue'),
      },
    ],
  },
]

export const flatNavigation = navigationGroups.flatMap((group) =>
  group.items.map((item) => ({
    ...item,
    groupKey: group.key,
    groupLabel: group.label,
    groupIcon: group.icon,
  })),
)

export function getFirstRouteForGroup(groupKey) {
  return navigationGroups.find((group) => group.key === groupKey)?.items?.[0]?.path || '/dashboard'
}
