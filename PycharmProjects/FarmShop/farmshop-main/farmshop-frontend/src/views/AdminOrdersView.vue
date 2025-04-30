<template>
  <div class="container py-5">
    <h2 class="mb-4">
      <font-awesome-icon icon="truck" class="me-2" /> Gestion des commandes
    </h2>

    <div v-if="orders.length">
      <div v-for="order in orders" :key="order.id" class="card mb-4 shadow-sm">
        <div class="card-body">
          <h5 class="card-title">Commande #{{ order.id }} - {{ order.user }}</h5>
          <p class="mb-1 text-muted">Date : {{ formatDate(order.created_at) }}</p>
          <p class="mb-1">Total : <strong class="text-success">{{ order.total_price }} €</strong></p>

          <div class="d-flex align-items-center mt-2">
            <label for="status-select" class="me-2">Statut :</label>
            <select v-model="order.status" class="form-select form-select-sm w-auto me-2">
              <option v-for="(label, value) in statusOptions" :key="value" :value="value">
                {{ label }}
              </option>
            </select>
            <button class="btn btn-sm btn-primary me-2" @click="updateStatus(order.id, order.status)">
              Mettre à jour
            </button>
            <button class="btn btn-sm btn-outline-success" @click="downloadInvoice(order.id)">
              Télécharger Facture
            </button>
          </div>

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
        </div>
      </div>
    </div>

    <div v-else class="alert alert-info text-center">
      Aucune commande à afficher.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const orders = ref([])
const toast = useToast()

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const statusOptions = {
  pending: 'En attente',
  paid: 'Payée',
  confirmed: 'Confirmée',
  preparing: 'Préparation',
  shipped: 'Expédiée',
  delivered: 'Livrée',
  canceled: 'Annulée'
}

const fetchOrders = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/orders/admin/orders/', { headers })
    orders.value = res.data.results || res.data
  } catch (err) {
    toast.error("Erreur chargement des commandes")
    console.error(err)
  }
}

const updateStatus = async (orderId, status) => {
  try {
    await axios.patch(`http://127.0.0.1:8000/api/orders/admin/${orderId}/update-status/`, { status }, { headers })
    toast.success("Statut mis à jour")
  } catch (err) {
    toast.error("Erreur mise à jour statut")
    console.error(err)
  }
}

const downloadInvoice = (orderId) => {
  window.open(`http://127.0.0.1:8000/api/orders/admin/${orderId}/invoice/`, '_blank')
}

const formatDate = (dateStr) => new Date(dateStr).toLocaleString()

onMounted(fetchOrders)
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: auto;
}
</style>
