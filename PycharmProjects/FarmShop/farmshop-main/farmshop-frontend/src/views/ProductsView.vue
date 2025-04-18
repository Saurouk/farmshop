<template>
  <div class="container py-5">
    <h2 class="mb-4">Nos produits</h2>

    <div v-if="products.length > 0" class="row g-4">
      <div v-for="product in products" :key="product.id" class="col-md-4">
        <div class="card h-100 shadow-sm p-2">
          <router-link :to="`/products/${product.id}`" class="text-decoration-none">
            <div
              class="product-thumb"
              :style="{ backgroundImage: `url(${product.image})` }"
            ></div>
            <div class="card-body">
              <h5 class="card-title">{{ product.name }}</h5>
              <p class="text-muted">{{ product.category }}</p>
              <p class="fw-bold text-success">{{ product.price }} €</p>
              <p class="text-muted">Stock : {{ product.stock }} {{ product.unit_of_measure }}</p>
            </div>
          </router-link>

          <div class="d-flex align-items-center gap-2 px-3 pb-3">
            <input
              type="number"
              min="1"
              :max="product.stock"
              v-model.number="quantities[product.id]"
              class="form-control form-control-sm w-50"
            />
            <button class="btn btn-sm btn-primary" @click="addToCart(product.id)">Ajouter au panier</button>
          </div>
        </div>
      </div>
    </div>

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
import { fetchCartCount } from '@/stores/cart'

const products = ref([])
const quantities = ref({})
const nextPage = ref(null)
const prevPage = ref(null)
const currentPage = ref(1)

const fetchProducts = async (page = 1) => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/products/?page=${page}`)
    products.value = res.data.results
    products.value.forEach(p => quantities.value[p.id] = 1)
    nextPage.value = res.data.next
    prevPage.value = res.data.previous
    currentPage.value = page
  } catch (error) {
    console.error("Erreur lors du chargement des produits :", error)
  }
}

const addToCart = async (productId) => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert("Veuillez vous connecter pour ajouter au panier.")
    return
  }

  try {
    await axios.post("http://127.0.0.1:8000/api/cart/add_item/", {
      product_id: productId,
      quantity: quantities.value[productId] || 1
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    await fetchCartCount()
  } catch (error) {
    console.error("Erreur ajout au panier :", error)
    alert("Erreur lors de l'ajout au panier.")
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
  border-radius: 6px;
}
</style>
