<template>
  <div class="container py-5">
    <h2 class="mb-4">🗕️ Mes locations</h2>
    <div v-if="rentals.length">
      <div v-for="r in rentals" :key="r.id" class="card mb-3 p-3 shadow-sm">
        <p><strong>Produit :</strong> {{ r.product.name }}</p>
        <p><strong>Période :</strong> {{ formatDate(r.start_date) }} → {{ formatDate(r.end_date) }}</p>
        <p><strong>Statut :</strong>
          <span class="badge" :class="badgeClass(r)">
            {{ rentalStatus(r) }}
          </span>
        </p>
        <p v-if="r.total_price"><strong>Total :</strong> {{ r.total_price }} €</p>
      </div>
    </div>
    <div v-else class="alert alert-info text-center">Aucune location.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const rentals = ref([])
const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const fetchRentals = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/orders/rentals/my/', { headers })
    rentals.value = res.data
  } catch (err) {
    console.error("Erreur chargement:", err)
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

const rentalStatus = (rental) => {
  const today = new Date()
  const end = new Date(rental.end_date)
  return rental.is_active
    ? (end >= today ? 'En cours' : 'Terminée ✅')
    : 'Annulée'
}

const badgeClass = (rental) => {
  const today = new Date()
  const end = new Date(rental.end_date)
  if (!rental.is_active) return 'bg-secondary'
  return end >= today ? 'bg-primary' : 'bg-success'
}

onMounted(fetchRentals)
</script>

<style scoped>
.container {
  max-width: 700px;
  margin: auto;
}
</style>
