<template>
  <div class="container py-5">
    <h2 class="mb-4">Votre panier</h2>

    <div v-if="cart && cart.items && cart.items.length">
      <ul class="list-group mb-4">
        <li v-for="item in cart.items" :key="item.id" class="list-group-item d-flex justify-content-between align-items-center">
          <div>
            <h5 class="mb-1">{{ item.product.name }}</h5>
            <p class="mb-1 text-muted">Prix unitaire : {{ item.product.price }} €</p>
            <p class="mb-1">Quantité :
              <button @click="decreaseQuantity(item)" class="btn btn-sm btn-outline-secondary me-1">-</button>
              {{ item.quantity }}
              <button @click="increaseQuantity(item)" class="btn btn-sm btn-outline-secondary ms-1">+</button>
            </p>
          </div>
          <div class="text-end">
            <p class="mb-1"><strong>{{ item.total_price }} €</strong></p>
            <button @click="removeItem(item.product.id)" class="btn btn-sm btn-outline-danger">Supprimer</button>
          </div>
        </li>
      </ul>

      <div class="text-end mt-4">
        <h5>Total du panier : <span class="text-success fw-bold">{{ cart.total_price }} €</span></h5>
        <p class="text-muted mt-2"><small>TVA incluse dans tous les prix affichés.</small></p>
      </div>
    </div>

    <div v-else class="alert alert-info text-center">
      Votre panier est vide.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import router from '@/router'

const cart = ref(null)
const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const fetchCart = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/cart/', { headers })
    cart.value = res.data
  } catch (err) {
    console.error("❌ Erreur chargement du panier :", err)
    if (err.response && err.response.status === 401) {
      router.push('/login')
    }
  }
}

const increaseQuantity = async (item) => {
  try {
    await axios.post('http://127.0.0.1:8000/api/cart/add_item/', {
      product_id: item.product.id,
      quantity: 1
    }, { headers })
    fetchCart()
  } catch (err) {
    console.error("❌ Erreur augmentation quantité :", err)
  }
}

const decreaseQuantity = async (item) => {
  if (item.quantity <= 1) {
    await removeItem(item.product.id)
    return
  }

  try {
    await axios.post('http://127.0.0.1:8000/api/cart/remove_item/', {
      product_id: item.product.id,
      quantity: 1
    }, { headers })
    fetchCart()
  } catch (err) {
    console.error("❌ Erreur diminution quantité :", err)
  }
}

const removeItem = async (productId) => {
  try {
    await axios.post('http://127.0.0.1:8000/api/cart/remove_item/', {
      product_id: productId,
      quantity: 1000
    }, { headers })
    fetchCart()
  } catch (err) {
    console.error("❌ Erreur suppression produit :", err)
  }
}

onMounted(() => {
  fetchCart()
})
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
}
</style>
