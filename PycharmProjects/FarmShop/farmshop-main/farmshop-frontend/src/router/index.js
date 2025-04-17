import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ProductsView from '../views/ProductsView.vue';
import ProductDetailView from '../views/ProductDetailView.vue';
import BlogView from '../views/BlogView.vue';
import ContactView from '../views/ContactView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '@/views/RegisterView.vue';
import auth from '@/stores/auth';

const routes = [
  { path: '/', component: HomeView },
  { path: '/products', component: ProductsView },
  { path: '/products/:id', component: ProductDetailView },
  {
    path: '/cart',
    name: 'CartView',
    component: () => import('@/views/CartView.vue'),
    meta: { requiresAuth: true }
  },
  { path: '/blog', component: BlogView },
  { path: '/blog/:id', component: () => import('@/views/ArticleDetail.vue') },
  { path: '/contact', component: ContactView },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  {
    path: '/profile',
    name: 'UserProfile',
    component: () => import('@/views/UserProfileView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: () => import('@/views/AdminDashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/produits',
    name: 'ProductAdmin',
    component: () => import('@/components/ProductAdmin.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !auth.isLoggedIn.value) {
    next('/login');
  } else if (to.meta.requiresAdmin && !auth.isAdmin.value) {
    next('/');
  } else {
    next();
  }
});

export default router;
