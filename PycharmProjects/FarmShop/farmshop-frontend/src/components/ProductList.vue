<template>
  <div class="container py-5">
    <h2 class="mb-4">Nos produits</h2>

    <div v-if="products.length > 0" class="row g-4">
      <div v-for="product in products" :key="product.id" class="col-md-4">
        <div class="card h-100 shadow-sm">
          <router-link :to="`/products/${product.id}`" class="text-decoration-none">
            <div class="product-thumb" :style="{ backgroundImage: `url(${BASE_MEDIA}${product.image})` }"></div>
          </router-link>
          <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="text-muted">{{ product.category }}</p>
            <p class="fw-bold text-success">{{ product.price }} €</p>
            <p class="text-muted small">Stock: {{ product.stock }}</p>
            <div class="d-flex align-items-center gap-2 mt-3">
              <input type="number" min="1" v-model.number="quantities[product.id]" class="form-control w-50" />
              <button
                class="btn btn-outline-primary btn-sm"
                @click="addToCart(product.id)"
                :disabled="loadingProductId === product.id"
              >
                <span v-if="loadingProductId === product.id">⏳</span>
                <span v-else-if="successProductId === product.id">✔️</span>
                <span v-else>Ajouter</span>
              </button>
            </div>
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
import { useToast } from 'vue-toastification'
import { fetchCartCount } from '@/stores/cart'

const BASE_MEDIA = 'http://127.0.0.1:8000'

const products = ref([])
const nextPage = ref(null)
const prevPage = ref(null)
const currentPage = ref(1)
const quantities = ref({})
const loadingProductId = ref(null)
const successProductId = ref(null)

const toast = useToast()

const fetchProducts = async (page = 1) => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/products/?page=${page}`)
    products.value = res.data.results
    nextPage.value = res.data.next
    prevPage.value = res.data.previous
    currentPage.value = page

    res.data.results.forEach(p => {
      if (!quantities.value[p.id]) quantities.value[p.id] = 1
    })
  } catch (error) {
    console.error("Erreur lors du chargement des produits :", error)
  }
}

const changePage = (page) => {
  if (page >= 1) {
    fetchProducts(page)
  }
}

const addToCart = async (productId) => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    toast.warning("Vous devez être connecté pour ajouter au panier.")
    return
  }

  loadingProductId.value = productId

  try {
    await axios.post("http://127.0.0.1:8000/api/cart/add_item/", {
      product_id: productId,
      quantity: quantities.value[productId] || 1
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })

    successProductId.value = productId
    toast.success("Produit ajouté au panier.")
    fetchCartCount()
  } catch (error) {
    console.error("Erreur ajout panier :", error)
    toast.error("Erreur lors de l'ajout au panier.")
  } finally {
    loadingProductId.value = null
    setTimeout(() => {
      successProductId.value = null
    }, 2000)
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
