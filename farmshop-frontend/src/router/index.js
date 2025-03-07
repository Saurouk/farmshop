import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProductsView from '../views/ProductsView.vue'
import ProductDetailView from '../views/ProductDetailView.vue'
import BlogView from '../views/BlogView.vue'
import ContactView from '../views/ContactView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: HomeView },
    { path: '/products', component: ProductsView },
    { path: '/products/:id', component: ProductDetailView },
    { path: '/blog', component: BlogView },
    { path: '/contact', component: ContactView },
    { path: '/login', component: LoginView },
    { path: '/register', component: RegisterView },
    { path: '/inbox', name: 'Inbox', component: () => import('@/views/InboxView.vue'), meta: { requiresAuth: true } },

    {
      path: '/profile',
      name: 'UserProfile',
      component: () => import('@/views/UserProfileView.vue'),
      meta: { requiresAuth: true }
    },

    {
      path: '/admin/users',
      name: 'UsersManagement',
      component: () => import('@/components/UsersManagement.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    }
  ]
})

export default router
