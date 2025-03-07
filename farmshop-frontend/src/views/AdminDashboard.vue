<template>
  <div class="admin-dashboard">
    <h1>⚙️ Panneau d'administration</h1>
    <button @click="activeTab = 'users'" class="btn btn-primary">Gérer les utilisateurs</button>

    <UsersManagement v-if="activeTab === 'users'" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import UsersManagement from "@/components/UsersManagement.vue";

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
