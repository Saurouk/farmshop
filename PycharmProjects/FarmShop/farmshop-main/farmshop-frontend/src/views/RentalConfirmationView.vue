<template>
  <div class="container py-5 text-center">
    <h2 class="mb-4 text-success">Location confirmée avec succès !</h2>

    <div class="card p-4 shadow mx-auto" style="max-width: 600px">
      <h4 class="mb-3">{{ productName }}</h4>
      <p><strong>Date de début :</strong> {{ startDate }}</p>
      <p><strong>Date de fin :</strong> {{ endDate }}</p>
      <p><strong>Durée :</strong> {{ rentalDays }} jour(s)</p>
      <p class="text-success fw-bold">
        <strong>Total :</strong> {{ totalPrice }} €
      </p>
      <router-link to="/products" class="btn btn-outline-primary mt-3">
        Retour aux produits
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()
const productName = route.query.name
const startDate = route.query.start
const endDate = route.query.end
const price = parseFloat(route.query.price || 0)

const rentalDays = computed(() => {
  const start = new Date(startDate)
  const end = new Date(endDate)
  const diff = (end - start) / (1000 * 60 * 60 * 24)
  return diff >= 1 ? Math.floor(diff) : 0
})

const totalPrice = computed(() => rentalDays.value * price)
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
}
</style>
