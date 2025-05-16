<template>
  <div class="admin-dashboard">
    <h1>⚙️ Panneau d'administration</h1>

    <div class="mb-4 d-flex flex-wrap justify-content-center gap-2">
      <button @click="activeTab = 'users'" class="btn btn-primary">Gérer les utilisateurs</button>
      <button @click="activeTab = 'blog'" class="btn btn-secondary">Gérer le blog</button>
      <button @click="activeTab = 'products'" class="btn btn-success">Gérer les produits</button>
      <button @click="activeTab = 'categories'" class="btn btn-dark">Gérer les catégories</button>
      <button @click="activeTab = 'locations'" class="btn btn-warning">Gérer les locations</button>
      <button @click="activeTab = 'stats'" class="btn btn-info">Statistiques vues</button>
      <button @click="activeTab = 'newsletter'" class="btn btn-outline-info">Gérer les newsletters</button>
    </div>

    <UsersManagement v-if="activeTab === 'users'" />
    <BlogAdmin v-if="activeTab === 'blog'" />
    <ProductAdmin v-if="activeTab === 'products'" />
    <CategoryAdmin v-if="activeTab === 'categories'" />
    <AdminRentalsView v-if="activeTab === 'locations'" />
    <DashboardStats v-if="activeTab === 'stats'" />
    <NewsletterAdmin v-if="activeTab === 'newsletter'" />
  </div>
</template>

<script setup>
import { ref } from "vue"
import UsersManagement from "@/components/UsersManagement.vue"
import BlogAdmin from "@/components/BlogAdmin.vue"
import ProductAdmin from "@/components/ProductAdmin.vue"
import CategoryAdmin from "@/components/CategoryAdmin.vue"
import AdminRentalsView from "@/components/AdminRentalsView.vue"
import DashboardStats from "@/components/DashboardStats.vue"
import NewsletterAdmin from "@/components/NewsletterAdmin.vue"

const activeTab = ref("users")
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
  max-width: 1000px;
  margin: auto;
  text-align: center;
}
</style>
