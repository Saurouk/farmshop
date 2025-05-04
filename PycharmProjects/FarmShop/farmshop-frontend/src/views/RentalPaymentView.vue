<template>
  <div class="container py-5">
    <h2 class="mb-4">Paiement de location pour {{ product?.name }}</h2>

    <div v-if="product">
      <p><strong>Prix :</strong> {{ product.price }} € / jour</p>

      <form @submit.prevent="prepareStripePayment" v-if="!clientSecret">
        <div class="mb-3">
          <label for="startDate" class="form-label">Date de début</label>
          <input type="date" v-model="startDate" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="endDate" class="form-label">Date de fin</label>
          <input type="date" v-model="endDate" class="form-control" required />
        </div>

        <div v-if="rentalDays">
          <p class="mb-3">Durée : {{ rentalDays }} jour(s)</p>
          <p class="mb-3 text-success">Total : {{ rentalDays * product.price }} €</p>
        </div>

        <button class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Préparation...' : 'Payer maintenant' }}
        </button>
      </form>

      <div v-if="clientSecret">
        <form @submit.prevent="submitStripePayment">
          <div id="payment-element" class="mb-4"></div>
          <button class="btn btn-success" :disabled="loading">
            {{ loading ? 'Traitement...' : 'Confirmer le paiement' }}
          </button>
        </form>
      </div>
    </div>

    <div v-else class="alert alert-warning">Chargement du produit...</div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useToast } from 'vue-toastification'
import { loadStripe } from '@stripe/stripe-js'

const STRIPE_PUBLISHABLE_KEY = import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY

const route = useRoute()
const router = useRouter()
const toast = useToast()

const product = ref(null)
const startDate = ref('')
const endDate = ref('')
const loading = ref(false)
const clientSecret = ref(null)

const stripe = ref(null)
const elements = ref(null)

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const rentalDays = computed(() => {
  if (!startDate.value || !endDate.value) return 0
  const start = new Date(startDate.value)
  const end = new Date(endDate.value)
  const diff = (end - start) / (1000 * 60 * 60 * 24)
  return diff >= 1 ? Math.floor(diff) : 0
})

const fetchProduct = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/products/${route.params.productId}/`)
    product.value = res.data
  } catch (err) {
    toast.error("Erreur chargement du produit")
    router.push('/')
  }
}

const prepareStripePayment = async () => {
  if (rentalDays.value === 0) {
    toast.error("Veuillez choisir une période valide")
    return
  }

  loading.value = true
  try {
    const res = await axios.post('http://127.0.0.1:8000/api/orders/create-rental-payment-intent/', {
      product_id: route.params.productId,
      start_date: startDate.value,
      end_date: endDate.value
    }, { headers })

    clientSecret.value = res.data.client_secret
    stripe.value = await loadStripe(STRIPE_PUBLISHABLE_KEY)
    elements.value = stripe.value.elements({ clientSecret: clientSecret.value })
    const paymentElement = elements.value.create('payment')
    paymentElement.mount('#payment-element')
  } catch (err) {
    toast.error("Erreur création du paiement")
    console.error(err)
  } finally {
    loading.value = false
  }
}

const submitStripePayment = async () => {
  loading.value = true
  const { error } = await stripe.value.confirmPayment({
    elements: elements.value,
    confirmParams: {
      return_url: `${window.location.origin}/rental/confirmation?start=${startDate.value}&end=${endDate.value}&name=${product.value.name}&price=${product.value.price}`
    }
  })

  if (error) {
    toast.error(error.message)
    loading.value = false
  }
}

onMounted(fetchProduct)
</script>

<style scoped>
.container {
  max-width: 700px;
  margin: auto;
}
</style>
