<template>
  <div class="container text-center mt-5">
    <h2 class="text-danger">❌ Échec de l'activation</h2>
    <p class="mt-3">Le lien d’activation est invalide ou a expiré.</p>
    <router-link to="/register" class="btn btn-secondary mt-4">Créer un nouveau compte</router-link>
  </div>
</template>

<script setup>
</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>
