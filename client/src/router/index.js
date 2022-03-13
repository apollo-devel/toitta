import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/register',
    name: 'register',
    meta: { layout: 'simple-layout' },
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/login',
    name: 'login',
    meta: { layout: 'simple-layout' },
    component: () => import('../views/LoginView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
