<template>
  <div class="container py-5">
    <h2 class="mb-4">Résumé de la commande</h2>

    <div v-if="cart && cart.items.length">
      <ul class="list-group mb-4">
        <li v-for="item in cart.items" :key="item.id" class="list-group-item d-flex justify-content-between align-items-center">
          <div>
            <h5 class="mb-1">{{ item.product.name }}</h5>
            <p class="mb-0 text-muted">Quantité : {{ item.quantity }}</p>
            <p class="mb-0 text-muted">Prix unitaire : {{ item.product.price }} €</p>
          </div>
          <strong>{{ item.total_price }} €</strong>
        </li>
      </ul>

      <div class="text-end">
        <h5>Total à payer : <span class="text-success fw-bold">{{ cart.total_price }} €</span></h5>
        <p class="text-muted"><small>TVA incluse dans tous les prix affichés.</small></p>
        <button class="btn btn-success mt-3" @click="submitOrder">Confirmer la commande</button>
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
    console.error("Erreur chargement du panier :", err)
    router.push('/login')
  }
}

const submitOrder = async () => {
  try {
    const res = await axios.post('http://127.0.0.1:8000/api/orders/create/', {}, { headers })
    const orderId = res.data.order_id
    router.push(`/confirmation/${orderId}`)
  } catch (err) {
    alert(err.response?.data?.error || "Erreur lors de la commande.")
    console.error("Erreur commande :", err)
  }
}

onMounted(fetchCart)
</script>
