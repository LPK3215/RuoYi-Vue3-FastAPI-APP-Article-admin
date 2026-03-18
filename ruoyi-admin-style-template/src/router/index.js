import { createRouter, createWebHashHistory } from 'vue-router'
import AdminLayout from '@/layout/AdminLayout.vue'
import { flatNavigation } from '@/config/navigation'

const childRoutes = flatNavigation.map((item) => ({
  path: item.path.replace(/^\//, ''),
  name: item.name,
  component: item.component,
  meta: {
    title: item.title,
    icon: item.icon,
    affix: item.affix || false,
    groupKey: item.groupKey,
    groupLabel: item.groupLabel,
    groupIcon: item.groupIcon,
  },
}))

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      component: AdminLayout,
      redirect: '/dashboard',
      children: childRoutes,
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/dashboard',
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
