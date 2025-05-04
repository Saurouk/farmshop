<template>
  <div class="container py-5 text-center">
    <div class="alert alert-success shadow-sm">
      <h2 class="mb-3">🎉 Merci pour votre commande !</h2>
      <p>Votre commande a bien été enregistrée.</p>
      <p class="fw-bold">Numéro de commande : {{ orderId }}</p>
      <router-link to="/products" class="btn btn-primary mt-3">← Continuer vos achats</router-link>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
const orderId = route.params.id
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
}
</style>
