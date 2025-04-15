<template>
  <div class="container py-5">
    <div v-if="product" class="card product-detail shadow-sm mx-auto">
      <div
        class="product-image"
        :style="{ backgroundImage: `url(${product.image})` }"
      ></div>

      <div class="card-body">
        <h2 class="card-title mb-3">{{ product.name }}</h2>
        <h4 class="text-success fw-bold">{{ product.price }} €</h4>
        <p class="badge bg-info text-dark me-2">{{ product.category }}</p>
        <p class="badge bg-light text-dark">{{ product.unit_of_measure }}</p>
        <p class="mt-3 product-description">{{ product.description }}</p>

        <div class="d-flex justify-content-between align-items-center mt-4">
          <router-link to="/products" class="btn btn-outline-secondary">← Retour aux produits</router-link>
          <span class="text-muted small">
            Stock : {{ product.stock }} {{ product.unit_of_measure }}<br />
            <span v-if="product.is_rentable" class="text-success">Disponible à la location ✅</span>
            <span v-else class="text-danger">Non louable ❌</span>
          </span>
        </div>
      </div>
    </div>

    <div v-else class="alert alert-warning text-center">
      Chargement du produit...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute();
const product = ref(null);

onMounted(async () => {
  try {
    const productId = route.params.id;
    const response = await axios.get(`http://127.0.0.1:8000/api/products/${productId}/`);
    product.value = response.data;
  } catch (error) {
    console.error('❌ Erreur API:', error);
  }
});
</script>

<style scoped>
.product-detail {
  max-width: 800px;
  border-radius: 12px;
  overflow: hidden;
  background: white;
}

.product-image {
  height: 400px;
  background-size: cover;
  background-position: center;
  border-bottom: 1px solid #ccc;
}

.card-body {
  padding: 30px;
}

.card-title {
  font-size: 1.8rem;
  font-weight: bold;
}

.product-description {
  font-size: 1.1rem;
  color: #444;
  line-height: 1.6;
}
</style>
