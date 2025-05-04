<template>
  <div class="container py-5 text-center">
    <h2 class="mb-4">Paiement sécurisé</h2>

    <div v-if="clientSecret">
      <form @submit.prevent="handleSubmit">
        <div id="payment-element" class="mb-4"></div>
        <button class="btn btn-success" :disabled="loading">
          {{ loading ? 'Traitement...' : 'Payer' }}
        </button>
      </form>
    </div>

    <div v-else>
      <p>Chargement du paiement...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { loadStripe } from '@stripe/stripe-js'
import axios from 'axios'

const stripePromise = loadStripe('pk_test_51QrPDURvR1l52m5MSTwGjNHQn5Gjb2nHQZO3HFfKVvuKx3Jx3dzwSnpN6ZH9UAUHYErqtyjMLJt7wBYZmfidARXn00RiBvLNJn')
const clientSecret = ref(null)
const stripe = ref(null)
const elements = ref(null)
const loading = ref(false)

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const fetchPaymentIntent = async () => {
  try {
    const res = await axios.post('http://127.0.0.1:8000/api/orders/create-payment-intent/', {}, { headers })
    clientSecret.value = res.data.client_secret
    stripe.value = await stripePromise
    elements.value = stripe.value.elements({ clientSecret: clientSecret.value })
    const paymentElement = elements.value.create('payment')
    paymentElement.mount('#payment-element')
  } catch (err) {
    console.error(err)
  }
}

const handleSubmit = async () => {
  loading.value = true
  const { error } = await stripe.value.confirmPayment({
    elements: elements.value,
    confirmParams: {
      return_url: window.location.origin + '/checkout/success',
    }
  })

  if (error) {
    alert(error.message)
    loading.value = false
  }
}

onMounted(fetchPaymentIntent)
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: auto;
}
</style>
