<script setup>
import Navbar from './components/Navbar.vue';
</script>

<template>
  <div id="app" class="app-background">
    <Navbar />
    <main class="page-content">
      <router-view />
    </main>
  </div>
</template>

<style>
html, body {
  margin: 0;
  padding: 0;
  min-height: 100%;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f4f9f4 !important; /* vert clair */
}

.app-background {
  min-height: 100vh;
  background-color: #f4f9f4;
}

.page-content {
  padding-top: 60px; /* espace pour éviter que la navbar cache le contenu */
}
</style>
