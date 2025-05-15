<template>
  <div class="container text-center mt-5">
    <h2 class="text-success">🎉 Compte activé avec succès !</h2>
    <p class="mt-3">Vous pouvez maintenant vous connecter à votre compte FarmShop.</p>
    <router-link to="/login" class="btn btn-primary mt-4">Se connecter</router-link>
    <div id="toast" class="toast-msg">✅ Compte activé !</div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  const toast = document.getElementById('toast')
  if (toast) {
    toast.classList.add('show')
    setTimeout(() => toast.classList.remove('show'), 4000)
  }
})
</script>

<style scoped>
.container {
  max-width: 600px;
}

.toast-msg {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background-color: #28a745;
  color: white;
  padding: 12px 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.4s ease-in-out;
  z-index: 9999;
}
.toast-msg.show {
  opacity: 1;
  transform: translateY(0);
}
</style>
