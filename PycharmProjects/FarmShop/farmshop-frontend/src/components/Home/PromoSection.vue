<template>
  <section class="promo-section text-white text-center py-5">
    <div class="container">
      <h2 class="mb-3">🎁 Offre Spéciale du Mois</h2>
      <p class="lead mb-4">
        Profiter des réductions sur les produits sélectionnés de notre magasin
      </p>
      <router-link to="/products" class="btn btn-light btn-lg">
        Voir les produits
      </router-link>
    </div>
  </section>
</template>

<script setup>
// Aucune logique JS pour le moment
</script>

<style scoped>
.promo-section {
  background-image: url('/promosection.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  width: 100%;
  min-height: 300px; /* réduit */
  padding: 3rem 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

</style>
