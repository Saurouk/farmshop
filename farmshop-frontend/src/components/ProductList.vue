<template>
  <div>
    <h2>Nos produits</h2>
    <div v-if="products.length > 0">
      <div v-for="product in products" :key="product.id" class="product-card">
        <router-link :to="`/products/${product.id}`">
          <h3>{{ product.name }}</h3>
          <p>{{ product.price }} €</p>
          <p>{{ product.category }}</p>
        </router-link>
      </div>
    </div>
    <p v-else>Chargement des produits...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const products = ref([]);

const fetchProducts = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/products/");
    products.value = response.data;
  } catch (error) {
    console.error("Erreur lors du chargement des produits :", error);
  }
};

onMounted(() => {
  fetchProducts();
});
</script>

<style scoped>
.product-card {
  border: 1px solid #ddd;
  padding: 10px;
  margin: 10px;
}
</style>
