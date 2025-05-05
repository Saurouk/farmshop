<template>
  <div class="container py-5">
    <h2 class="mb-4">💖 Ma Wishlist</h2>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Chargement...</span>
      </div>
    </div>

    <div v-else-if="wishlist.length">
      <div
        v-for="item in wishlist"
        :key="item.id"
        class="card mb-3 p-3 shadow-sm d-flex flex-row align-items-center justify-content-between"
      >
        <div class="d-flex align-items-center">
          <img
            :src="item.product_detail.image"
            alt="product"
            class="me-3"
            style="width: 100px; height: auto; object-fit: cover"
          />
          <div>
            <h5>{{ item.product_detail.name }}</h5>
            <p class="mb-1 text-muted">{{ item.product_detail.description }}</p>
            <p class="mb-1"><strong>{{ item.product_detail.price }} €</strong></p>
          </div>
        </div>
        <button @click="removeFromWishlist(item.product_detail.id)" class="btn btn-outline-danger">
          ❌ Retirer
        </button>
      </div>
    </div>

    <div v-else class="alert alert-info text-center">
      Aucun produit en liste d’envie.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const wishlist = ref([])
const loading = ref(true)
const toast = useToast()
const router = useRouter()

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const fetchWishlist = async () => {
  if (!token) {
    toast.warning("Veuillez vous connecter pour voir votre wishlist.")
    router.push('/login')
    return
  }

  try {
    const res = await axios.get('http://127.0.0.1:8000/api/products/wishlist/', { headers })
    wishlist.value = res.data.results
  } catch (err) {
    toast.error('Erreur lors du chargement de la wishlist.')
  } finally {
    loading.value = false
  }
}

const removeFromWishlist = async (productId) => {
  try {
    await axios.delete(`http://127.0.0.1:8000/api/products/wishlist/${productId}/remove/`, { headers })
    wishlist.value = wishlist.value.filter(item => item.product_detail.id !== productId)
    toast.success("Produit retiré de la wishlist.")
  } catch (err) {
    toast.error("Erreur lors de la suppression.")
    console.error(err)
  }
}

onMounted(fetchWishlist)
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
}
</style>
