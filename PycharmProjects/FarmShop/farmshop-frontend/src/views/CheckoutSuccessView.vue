<template>
  <div class="container text-center py-5">
    <h1 class="text-success mb-4">
      <font-awesome-icon icon="check-circle" class="me-2" />
      Merci pour votre achat !
    </h1>
    <p class="lead">Votre commande a été confirmée avec succès.</p>

    <router-link class="btn btn-primary mt-4" to="/products">
      <font-awesome-icon icon="arrow-left" class="me-2" />
      Continuer vos achats
    </router-link>
  </div>
</template>

<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
</script>

<style scoped>
.container {
  max-width: 700px;
  margin: auto;
}
</style>
