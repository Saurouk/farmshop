<template>
  <div class="container py-5">
    <h2 class="mb-4">
      <font-awesome-icon icon="receipt" class="me-2" />
      Historique de vos commandes
    </h2>

    <div v-if="orders.length">
      <div v-for="order in orders" :key="order.id" class="card mb-4 shadow-sm">
        <div class="card-body">
          <h5 class="card-title">Commande #{{ order.id }}</h5>
          <p class="mb-1 text-muted">Date : {{ formatDate(order.created_at) }}</p>
          <p class="mb-1 text-muted">Statut : <strong>{{ formatStatus(order.status) }}</strong></p>
          <p class="mb-1 text-muted">Total : <strong class="text-success">{{ order.total_price }} €</strong></p>

          <ul class="list-group mt-3">
            <li
              v-for="item in order.items"
              :key="item.id"
              class="list-group-item d-flex justify-content-between"
            >
              <span>{{ item.quantity }} x {{ item.product.name }}</span>
              <span>{{ item.price_per_unit }} €</span>
            </li>
          </ul>

          <div class="text-end mt-3">
            <a :href="`${API_BASE_URL}/api/orders/admin/${order.id}/invoice/`" class="btn btn-outline-primary btn-sm" target="_blank">
              Télécharger facture
            </a>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="alert alert-info text-center">
      Aucune commande trouvée.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000'
const orders = ref([])
const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const fetchOrders = async () => {
  try {
    const res = await axios.get(`${API_BASE_URL}/api/orders/history/`, { headers })
    orders.value = res.data.results || []
  } catch (err) {
    console.error("Erreur chargement historique des commandes:", err)
  }
}

const formatDate = (dateStr) => new Date(dateStr).toLocaleString()
const formatStatus = (status) => {
  const map = {
    pending: "En attente",
    confirmed: "Confirmée",
    preparing: "Préparation",
    shipped: "Expédiée",
    delivered: "Livrée",
    canceled: "Annulée",
    paid: "Payée"
  }
  return map[status] || status
}

onMounted(fetchOrders)
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
}
</style>
