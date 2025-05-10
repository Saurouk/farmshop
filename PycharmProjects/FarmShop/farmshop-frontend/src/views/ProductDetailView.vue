<template>
  <div class="container py-5">
    <div v-if="product && product.name" class="card product-detail shadow-sm mx-auto">
      <img v-if="product.image" :src="product.image" class="card-img-top" :alt="product.name" />
      <div class="card-body">
        <h2 class="card-title mb-3">{{ product.name }}</h2>
        <h4 class="text-success fw-bold">{{ product.price }} €</h4>
        <p class="badge bg-info text-dark me-2">{{ product.category }}</p>
        <p class="badge bg-light text-dark">{{ product.unit_of_measure }}</p>
        <p class="mt-3 product-description">{{ product.description }}</p>

        <!-- Galerie des images secondaires -->
        <div v-if="product.images && product.images.length" class="gallery row mt-4">
          <div
            v-for="(img, index) in product.images"
            :key="img.id"
            class="col-md-3 mb-3"
            @click="showLightbox(index)"
            style="cursor: pointer;"
          >
            <img :src="img.image" class="img-fluid rounded shadow-sm gallery-image" />
          </div>
        </div>

        <div class="d-flex justify-content-between align-items-center mt-4">
          <router-link to="/products" class="btn btn-outline-secondary">← Retour aux produits</router-link>
          <span class="text-muted small">
            Stock : {{ product.stock }} {{ product.unit_of_measure }}<br />
            <span v-if="product.is_rentable" class="text-success">Disponible à la location ✅</span>
          </span>
        </div>

        <div class="d-flex mt-4 gap-2 flex-wrap">
          <input type="number" min="1" v-model="quantity" class="form-control w-auto" />
          <button class="btn btn-primary" @click="addToCart">Ajouter au panier</button>
          <router-link
            v-if="product.is_rentable"
            :to="`/rentals/payment/${product.id}`"
            class="btn btn-outline-primary"
          >
            Louer ce produit
          </router-link>
          <button
            class="btn"
            :class="isInWishlist ? 'btn-danger' : 'btn-outline-danger'"
            @click="toggleWishlist"
          >
            {{ isInWishlist ? '💔 Retirer de la wishlist' : '💖 Ajouter à la wishlist' }}
          </button>
        </div>
      </div>
    </div>

    <div v-else class="alert alert-warning text-center">Chargement du produit...</div>

    <VueEasyLightbox v-if="product && product.images && product.images.length"
      :visible="lightboxVisible"
      :imgs="product.images.map(img => img.image)"
      :index="lightboxIndex"
      @hide="lightboxVisible = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import VueEasyLightbox from 'vue-easy-lightbox'
import { useToast } from 'vue-toastification'
import { fetchCartCount } from '@/stores/cart'

const route = useRoute()
const product = ref({ images: [] })
const quantity = ref(1)
const lightboxVisible = ref(false)
const lightboxIndex = ref(0)
const token = localStorage.getItem('access_token')
const isLoggedIn = !!token
const toast = useToast()
const isInWishlist = ref(false)

const showLightbox = (index) => {
  lightboxIndex.value = index
  lightboxVisible.value = true
}

const addToCart = async () => {
  if (!isLoggedIn) {
    toast.warning('Vous devez être connecté pour ajouter au panier.')
    return
  }

  try {
    await axios.post("http://127.0.0.1:8000/api/cart/add_item/", {
      product_id: product.value.id,
      quantity: quantity.value
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    fetchCartCount()
    toast.success('Produit ajouté au panier !')
  } catch (error) {
    console.error("❌ Erreur ajout au panier :", error)
    toast.error("Erreur lors de l'ajout au panier.")
  }
}

const checkWishlist = async () => {
  if (!isLoggedIn) return
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/products/wishlist/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    isInWishlist.value = res.data.results?.some(item => item.product_detail.id === product.value.id)
  } catch (err) {
    console.error('Erreur vérification wishlist', err)
  }
}

const toggleWishlist = async () => {
  if (!isLoggedIn) {
    toast.warning('Veuillez vous connecter pour utiliser la wishlist.')
    return
  }

  try {
    if (isInWishlist.value) {
      await axios.delete(`http://127.0.0.1:8000/api/products/wishlist/${product.value.id}/remove/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      isInWishlist.value = false
      toast.info('Produit retiré de votre wishlist.')
    } else {
      await axios.post('http://127.0.0.1:8000/api/products/wishlist/', {
        product: product.value.id
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      isInWishlist.value = true
      toast.success('Produit ajouté à votre wishlist.')
    }
  } catch (err) {
    console.error('Erreur wishlist', err)
    toast.error('Action wishlist échouée.')
  }
}

onMounted(async () => {
  try {
    const productId = route.params.id
    const response = await axios.get(`http://127.0.0.1:8000/api/products/${productId}/`)
    product.value = response.data
    checkWishlist()
  } catch (error) {
    console.error('❌ Erreur API:', error)
  }
})
</script>

<style scoped>
.product-detail {
  max-width: 900px;
  border-radius: 12px;
  overflow: hidden;
}
.card-img-top {
  height: 400px;
  object-fit: cover;
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
.gallery-image {
  height: 120px;
  object-fit: cover;
}
</style>
