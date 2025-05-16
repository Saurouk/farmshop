<template>
  <div class="newsletter-admin">
    <h2>📨 Gestion des Newsletters</h2>

    <form @submit.prevent="sendNewsletter" class="mb-4">
      <input v-model="subject" type="text" class="form-control mb-2" placeholder="Objet de la newsletter" required />
      <textarea v-model="body" rows="5" class="form-control mb-2" placeholder="Contenu de la newsletter" required></textarea>
      <button class="btn btn-primary">Envoyer la newsletter</button>
    </form>

    <h4>Historique des newsletters</h4>
    <ul class="list-group">
      <li v-for="newsletter in history" :key="newsletter.id" class="list-group-item">
        <strong>{{ newsletter.subject }}</strong> - <span class="text-muted">{{ formatDate(newsletter.created_at) }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const subject = ref('')
const body = ref('')
const history = ref([])

const fetchHistory = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const res = await axios.get('http://127.0.0.1:8000/api/newsletters/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    history.value = res.data
  } catch (err) {
    console.error('Erreur chargement des newsletters :', err)
  }
}

const sendNewsletter = async () => {
  try {
    const token = localStorage.getItem('access_token')
    await axios.post('http://127.0.0.1:8000/api/newsletters/', {
      subject: subject.value,
      body: body.value
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    subject.value = ''
    body.value = ''
    await fetchHistory()
  } catch (err) {
    console.error('Erreur envoi newsletter :', err)
  }
}

const formatDate = (dateStr) => new Date(dateStr).toLocaleString()

onMounted(fetchHistory)
</script>

<style scoped>
.newsletter-admin {
  padding: 20px;
  max-width: 700px;
  margin: auto;
}
</style>
