<template>
  <section class="about-section py-5 bg-light">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-md-6 mb-4 mb-md-0">
          <img
            src="/aboutus.jpg"
            alt="Présentation FarmShop"
            class="img-fluid rounded shadow"
          />
        </div>
        <div class="col-md-6">
          <h2 class="mb-3">À propos de FarmShop</h2>
          <p>
            FarmShop est une boutique agricole en ligne qui met en avant des produits locaux,
            biologiques et responsables. Nous travaillons directement avec les producteurs pour
            vous offrir des produits frais, authentiques et de qualité.
          </p>
          <p>
            Notre mission : rapprocher les fermes des foyers, soutenir l’agriculture durable et
            simplifier vos achats alimentaires.
          </p>
          <router-link to="/products" class="btn btn-outline-primary mt-3">
            Explorer nos produits
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// Aucune logique JS
</script>

<style scoped>
.about-section img {
  max-height: 350px;
  object-fit: cover;
}
</style>
