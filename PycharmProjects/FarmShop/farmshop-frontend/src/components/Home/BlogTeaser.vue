<template>
  <section class="blog-teaser text-white d-flex align-items-center justify-content-center text-center">
    <div class="overlay"></div>
    <div class="content">
      <router-link to="/blog" class="btn btn-outline-light btn-lg">
        Lire nos articles
      </router-link>
    </div>
  </section>
</template>

<script setup>
// Aucun script requis ici
</script>

<style scoped>
.blog-teaser {
  position: relative;
  background-image: url('/blogteaser.jpg');
  background-size: cover;
  background-position: center;
  height: 60vh;
  padding: 2rem;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background: rgba(0, 0, 0, 0.5);
}

.content {
  position: relative;
  z-index: 1;
  max-width: 700px;
}
</style>
