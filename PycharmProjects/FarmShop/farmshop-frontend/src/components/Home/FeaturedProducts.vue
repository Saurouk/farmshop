<template>
  <div class="featured-products container py-5">
    <h2 class="mb-4 text-center">🌟 Produits phares</h2>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-success" role="status">
        <span class="visually-hidden">Chargement...</span>
      </div>
    </div>

    <div v-else-if="products.length === 0" class="alert alert-info text-center">
      Aucun produit à afficher pour le moment.
    </div>

    <div v-else class="row g-4">
      <div class="col-md-4" v-for="product in products" :key="product.id">
        <div class="card h-100 shadow-sm">
          <img
            :src="product.image ? product.image : '/default-product.jpg'"
            class="card-img-top"
            :alt="product.name"
            style="object-fit: cover; height: 200px;"
          />
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text text-muted">{{ truncate(product.description, 100) }}</p>
            <router-link :to="`/products/${product.id}`" class="mt-auto btn btn-outline-primary">
              Voir le produit
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const products = ref([])
const loading = ref(true)

const fetchFeatured = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/products/?limit=3')
    products.value = res.data.results || res.data
  } catch (err) {
    console.error('❌ Erreur chargement produits phares :', err)
  } finally {
    loading.value = false
  }
}

const truncate = (text, length) => {
  return text.length > length ? text.substring(0, length) + '...' : text
}

onMounted(fetchFeatured)
</script>

<style scoped>
.featured-products {
  background-color: #f8f9fa;
  border-radius: 8px;
}
</style>
