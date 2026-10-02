import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
    },
    {
      path: '/assets',
      name: 'assets',
      component: () => import('../views/AssetsView.vue'),
    },
    {
      path: '/assets/:id',
      name: 'asset-detail',
      component: () => import('../views/AssetDetailView.vue'),
      props: true,
    },
    {
      path: '/readings/new',
      name: 'add-reading',
      component: () => import('../views/AddReadingView.vue'),
    },
    {
      path: '/statistics',
      name: 'statistics',
      component: () => import('../views/StatisticsView.vue'),
    },
    {
      path: '/currencies',
      name: 'currencies',
      component: () => import('../views/CurrenciesView.vue'),
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
