<template>
  <div class="container mt-5">
    <div v-if="product" class="card">
      <img :src="product.imageUrl" class="card-img-top" :alt="product.name">
      <div class="card-body">
        <h2 class="card-title">{{ product.name }}</h2>
        <h4 class="text-primary">{{ product.price }} €</h4>
        <p class="text-muted">{{ product.category }}</p>
        <p>{{ product.description }}</p>
        <router-link to="/products" class="btn btn-secondary">🔙 Retour aux produits</router-link>
      </div>
    </div>
    <div v-else class="alert alert-warning">
      Chargement du produit...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const product = ref(null)

onMounted(async () => {
  try {
    const productId = route.params.id
    const response = await axios.get(`http://localhost:8000/api/products/${productId}/`)
    product.value = response.data
    console.log('✅ Détails du produit récupérés:', product.value)
  } catch (error) {
    console.error('❌ Erreur API:', error)
  }
})
</script>

<style scoped>
.card-img-top {
  height: 300px;
  object-fit: cover;
}
</style>
