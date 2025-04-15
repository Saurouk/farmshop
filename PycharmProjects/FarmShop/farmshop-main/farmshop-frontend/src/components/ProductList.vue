<template>
  <div class="container py-5">
    <h2 class="mb-4">Nos produits</h2>

    <div v-if="products.length > 0" class="row g-4">
      <div
        v-for="product in products"
        :key="product.id"
        class="col-md-4"
      >
        <router-link :to="`/products/${product.id}`" class="text-decoration-none">
          <div class="card h-100 shadow-sm">
            <div
              class="product-thumb"
              :style="{ backgroundImage: `url(${product.image})` }"
            ></div>
            <div class="card-body">
              <h5 class="card-title">{{ product.name }}</h5>
              <p class="text-muted">{{ product.category }}</p>
              <p class="fw-bold text-success">{{ product.price }} €</p>
            </div>
          </div>
        </router-link>
      </div>
    </div>

    <!-- PAGINATION -->
    <div v-if="products.length" class="pagination-controls mt-5 d-flex justify-content-center gap-3">
      <button @click="changePage(currentPage - 1)" :disabled="!prevPage" class="btn btn-outline-primary">← Précédent</button>
      <span>Page {{ currentPage }}</span>
      <button @click="changePage(currentPage + 1)" :disabled="!nextPage" class="btn btn-outline-primary">Suivant →</button>
    </div>

    <p v-else class="text-center mt-5">Chargement des produits...</p>
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
.product-thumb {
  height: 200px;
  background-size: cover;
  background-position: center;
  border-top-left-radius: 6px;
  border-top-right-radius: 6px;
}
</style>
