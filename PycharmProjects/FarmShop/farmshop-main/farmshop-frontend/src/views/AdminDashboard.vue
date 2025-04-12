<template>
  <div class="admin-dashboard">
    <h1>⚙️ Panneau d'administration</h1>

    <!-- Boutons de navigation -->
    <div class="mb-4">
      <button @click="activeTab = 'users'" class="btn btn-primary me-2">Gérer les utilisateurs</button>
      <button @click="activeTab = 'blog'" class="btn btn-secondary me-2">Gérer le blog</button>
      <button @click="activeTab = 'products'" class="btn btn-success">Gérer les produits</button>
    </div>

    <!-- Contenu -->
    <UsersManagement v-if="activeTab === 'users'" />
    <BlogAdmin v-if="activeTab === 'blog'" />
    <ProductAdmin v-if="activeTab === 'products'" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import UsersManagement from "@/components/UsersManagement.vue";
import BlogAdmin from "@/components/BlogAdmin.vue";
import ProductAdmin from "@/components/ProductAdmin.vue"; // ✅ Ajout du composant
const activeTab = ref("users");
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
  max-width: 1000px;
  margin: auto;
  text-align: center;
}
</style>
