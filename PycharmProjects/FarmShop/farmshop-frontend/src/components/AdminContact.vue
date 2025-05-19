<template>
  <div class="container mt-5">
    <h2 class="mb-4">📬 Messages de Contact</h2>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Chargement...</span>
      </div>
    </div>

    <div v-else>
      <div v-if="messages.length === 0" class="alert alert-info">
        Aucun message reçu.
      </div>

      <div v-for="msg in messages" :key="msg.id" class="card mb-3">
        <div class="card-header d-flex justify-content-between">
          <div>
            <strong>{{ msg.email }}</strong> —
            <span class="text-muted">{{ formatDate(msg.created_at) }}</span>
          </div>
          <span class="badge" :class="msg.is_handled ? 'bg-success' : 'bg-warning text-dark'">
            {{ msg.is_handled ? 'Traité' : 'En attente' }}
          </span>
        </div>
        <div class="card-body">
          <h5 class="card-title">{{ msg.subject }}</h5>
          <p><strong>Raison:</strong> {{ displayReason(msg.reason) }}</p>
          <p>{{ msg.content }}</p>

          <div v-if="msg.is_handled">
            <hr />
            <h6 class="text-success">Réponse :</h6>
            <p>{{ msg.response }}</p>
            <p class="text-muted"><small>Répondu le {{ formatDate(msg.responded_at) }}</small></p>
          </div>

          <div v-else class="mt-3">
            <textarea v-model="msg.reply" class="form-control" rows="3" placeholder="Rédiger votre réponse ici..."></textarea>
            <button class="btn btn-primary btn-sm mt-2" @click="sendResponse(msg)">Envoyer la réponse</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const messages = ref([])
const loading = ref(true)

const fetchMessages = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/contact/messages/')
    messages.value = res.data.map(msg => ({ ...msg, reply: '' }))
  } catch (err) {
    console.error('❌ Erreur chargement messages :', err)
  } finally {
    loading.value = false
  }
}

const sendResponse = async (msg) => {
  if (!msg.reply.trim()) {
    alert("Veuillez entrer une réponse.")
    return
  }

  try {
    await axios.patch(`http://127.0.0.1:8000/api/contact/respond/${msg.id}/`, {
      response: msg.reply
    })

    msg.is_handled = true
    msg.response = msg.reply
    msg.responded_at = new Date().toISOString()
    msg.reply = ''

    alert('✅ Réponse envoyée avec succès.')
  } catch (err) {
    console.error('❌ Erreur envoi réponse :', err)
    alert("Erreur lors de l'envoi de la réponse.")
  }
}

const displayReason = (reason) => {
  const mapping = {
    products: 'Nos produits',
    articles: 'Nos articles',
    other: 'Autres'
  }
  return mapping[reason] || reason
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString()
}

onMounted(fetchMessages)
</script>

<style scoped>
textarea {
  resize: vertical;
}
</style>
