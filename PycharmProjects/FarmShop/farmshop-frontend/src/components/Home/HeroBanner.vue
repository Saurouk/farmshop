<template>
  <div class="hero-banner d-flex align-items-center justify-content-center text-center text-white">
    <div class="overlay"></div>
    <div class="hero-content">

      <router-link to="/products" class="btn btn-light btn-lg mt-3">Découvrir nos produits</router-link>
    </div>
  </div>
</template>

<script setup>
// Pas de logique JS nécessaire ici
</script>

<style scoped>
.hero-banner {
  background-image: url('/hero-farm.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  width: 100%;
  height: 60vh; /* au lieu de 100vh */
  position: relative;
  margin: 0;
  padding: 2rem 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: auto;
  color: white;
  text-align: center;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background: rgba(0, 0, 0, 0.4);
}
</style>
