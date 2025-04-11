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

      <!-- PAGINATION -->
      <div class="pagination-controls mt-4 d-flex justify-content-center gap-3">
        <button @click="changePage(currentPage - 1)" :disabled="!prevPage" class="btn btn-outline-primary">← Précédent</button>
        <span>Page {{ currentPage }}</span>
        <button @click="changePage(currentPage + 1)" :disabled="!nextPage" class="btn btn-outline-primary">Suivant →</button>
      </div>
    </div>
    <p v-else>Chargement des produits...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const products = ref([])
const nextPage = ref(null)
const prevPage = ref(null)
const currentPage = ref(1)

const fetchProducts = async (page = 1) => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/products/?page=${page}`)
    products.value = res.data.results
    nextPage.value = res.data.next
    prevPage.value = res.data.previous
    currentPage.value = page
  } catch (error) {
    console.error("Erreur lors du chargement des produits :", error)
  }
}

const changePage = (page) => {
  if (page >= 1) {
    fetchProducts(page)
  }
}

onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
.product-card {
  border: 1px solid #ddd;
  padding: 10px;
  margin: 10px;
}
</style>
