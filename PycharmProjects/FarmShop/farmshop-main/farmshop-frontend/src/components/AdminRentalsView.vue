<template>
  <div class="admin-rentals">
    <h2 class="mb-4">📅 Gestion des locations</h2>

    <div v-if="rentals.length">
      <div v-for="rental in rentals" :key="rental.id" class="card mb-3 p-3 shadow-sm">
        <p><strong>Produit :</strong> {{ rental.product.name }}</p>
        <p><strong>Client :</strong> {{ rental.user.username }}</p>
        <p><strong>Période :</strong> {{ rental.start_date }} → {{ rental.end_date }}</p>
        <p>
          <strong>Statut :</strong>
          <span class="badge" :class="rental.is_active ? 'bg-success' : 'bg-secondary'">
            {{ rental.is_active ? 'Active' : 'Annulée' }}
          </span>
        </p>
        <button
          class="btn btn-sm btn-outline-danger mt-2"
          @click="cancelRental(rental.id)"
          :disabled="!rental.is_active"
        >
          Annuler la location
        </button>
      </div>
    </div>
    <div v-else class="alert alert-info text-center">Aucune location trouvée.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const rentals = ref([])
const toast = useToast()
const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const fetchRentals = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/products/rentals/', { headers })
    rentals.value = res.data
  } catch (err) {
    toast.error('Erreur chargement des locations')
  }
}

const cancelRental = async (id) => {
  try {
    await axios.patch(`http://127.0.0.1:8000/api/products/rentals/${id}/`, { is_active: false }, { headers })
    toast.success('Location annulée')
    fetchRentals()
  } catch (err) {
    toast.error("Erreur lors de l'annulation")
  }
}

onMounted(fetchRentals)
</script>

<style scoped>
.admin-rentals {
  max-width: 900px;
  margin: auto;
}
</style>
