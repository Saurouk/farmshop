<template>
  <div class="container py-5">
    <h2 class="mb-4">Gestion des Locations</h2>

    <div v-if="loading" class="text-center my-5">
      <span class="spinner-border text-primary" role="status"></span>
    </div>

    <div v-else>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Produit</th>
            <th>Utilisateur</th>
            <th>Date de début</th>
            <th>Date de fin</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rental in rentals" :key="rental.id">
            <td>{{ rental.id }}</td>
            <td>{{ rental.product.name }}</td>
            <td>{{ rental.user }}</td>
            <td>{{ rental.start_date }}</td>
            <td>{{ rental.end_date }}</td>
            <td>
              <span :class="['badge', rental.is_active ? 'bg-success' : 'bg-secondary']">
                {{ rental.is_active ? 'Active' : 'Annulée' }}
              </span>
            </td>
            <td>
              <button
                class="btn btn-sm btn-danger"
                @click="cancelRental(rental.id)"
                :disabled="!rental.is_active"
              >
                Annuler
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const rentals = ref([])
const loading = ref(true)
const toast = useToast()

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const fetchRentals = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/products/rentals/', { headers })
    rentals.value = res.data
  } catch (err) {
    toast.error("Erreur chargement des locations")
  } finally {
    loading.value = false
  }
}

const cancelRental = async (rentalId) => {
  try {
    await axios.patch(`http://127.0.0.1:8000/api/products/rentals/${rentalId}/`, { is_active: false }, { headers })
    toast.success("Location annulée")
    await fetchRentals()
  } catch (err) {
    toast.error("Erreur annulation")
  }
}

onMounted(fetchRentals)
</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: auto;
}
</style>
