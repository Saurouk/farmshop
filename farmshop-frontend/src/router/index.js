import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import ProductsView from '@/views/ProductsView.vue';
import BlogView from '@/views/BlogView.vue';
import ContactView from '@/views/ContactView.vue';
import LoginView from '@/views/LoginView.vue';
import ProductDetailView from '@/views/ProductDetailView.vue';

const routes = [
  { path: '/', component: HomeView },
  { path: '/products', component: ProductsView },
  { path: '/blog', component: BlogView },
  { path: '/contact', component: ContactView },
  { path: '/login', component: LoginView },
  { path: '/product/:id', component: ProductDetailView, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
