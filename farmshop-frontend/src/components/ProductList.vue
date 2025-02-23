<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const products = ref([])
const searchQuery = ref('')
const selectedCategory = ref('')
const router = useRouter()

const filteredProducts = computed(() => {
  return products.value.filter(p => {
    const matchesSearch = searchQuery.value
      ? p.name.toLowerCase().includes(searchQuery.value.toLowerCase())
      : true

    const matchesCategory = selectedCategory.value
      ? p.category === selectedCategory.value
      : true

    return matchesSearch && matchesCategory
  })
})

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/products/')
    console.log('✅ API Response:', response.data)
    products.value = response.data
  } catch (error) {
    console.error('Erreur API:', error)
  }
})

const categories = computed(() => {
  const uniqueCategories = [...new Set(products.value.map(p => p.category))]
  return uniqueCategories
})

const viewProduct = (id) => {
  router.push(`/products/${id}`)
}
</script>

<template>
  <div class="container mt-4">
    <h2 class="mb-4">🌽 Nos produits</h2>

    <div class="row mb-4">
      <div class="col-md-6">
        <input type="text" v-model="searchQuery" class="form-control" placeholder="🔍 Rechercher un produit...">
      </div>
      <div class="col-md-6">
        <select v-model="selectedCategory" class="form-control">
          <option value="">Toutes les catégories</option>
          <option v-for="category in categories" :key="category">
            {{ category }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="filteredProducts.length" class="row">
      <div v-for="product in filteredProducts" :key="product.id" class="col-md-4 mb-4">
        <div class="card">
          <img :src="product.imageUrl" class="card-img-top" :alt="product.name">
          <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text"><strong>{{ product.price }}€</strong></p>
            <p class="card-text text-muted">{{ product.category }}</p>
            <button @click="viewProduct(product.id)" class="btn btn-primary">👁️ Voir plus</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Ajoute ce bloc pour debug -->
    <div v-else>
      <p class="alert alert-warning">Aucun produit trouvé.</p>
      <pre>{{ filteredProducts }}</pre>
      <pre>{{ products }}</pre>
    </div>
  </div>
</template>

<style scoped>
.card-img-top {
  height: 200px;
  object-fit: cover;
}
</style>