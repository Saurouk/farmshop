<template>
  <section class="why-choose-us py-5 text-white text-center">
    <div class="overlay"></div>
    <div class="container position-relative">
      <h2 class="mb-4">Pourquoi choisir FarmShop ?</h2>
      <div class="row">
        <div class="col-md-4 mb-4">
          <div class="icon-box p-4 border rounded shadow-sm h-100 bg-dark bg-opacity-75">
            <i class="fas fa-seedling fa-2x text-success mb-3"></i>
            <h5>Produits frais et locaux</h5>
            <p class="text-light">Nous travaillons avec des producteurs de confiance pour vous garantir des produits de qualité.</p>
          </div>
        </div>

        <div class="col-md-4 mb-4">
          <div class="icon-box p-4 border rounded shadow-sm h-100 bg-dark bg-opacity-75">
            <i class="fas fa-truck fa-2x text-primary mb-3"></i>
            <h5>Livraison rapide</h5>
            <p class="text-light">Commandez en ligne et recevez vos produits directement à domicile en un temps record.</p>
          </div>
        </div>

        <div class="col-md-4 mb-4">
          <div class="icon-box p-4 border rounded shadow-sm h-100 bg-dark bg-opacity-75">
            <i class="fas fa-leaf fa-2x text-warning mb-3"></i>
            <h5>Engagement écologique</h5>
            <p class="text-light">Nous promouvons une agriculture durable et des emballages écoresponsables.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// Aucun script nécessaire
</script>

<style scoped>
.why-choose-us {
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url('/whychooseus.jpg') center/cover no-repeat;
  position: relative;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background: rgba(0, 0, 0, 0.4);
  z-index: 0;
}

.position-relative > * {
  position: relative;
  z-index: 1;
}
</style>
