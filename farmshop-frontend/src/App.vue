<script setup>
import Navbar from './components/Navbar.vue';
</script>

<template>
  <div>
    <Navbar />
    <div class="container mt-4">
      <router-view></router-view>
    </div>
  </div>
</template>

<style>
/* Ajoute ton CSS global ici */
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f8f9fa;
}

h1 {
  text-align: center;
  color: #2E7D32;
}
</style>
