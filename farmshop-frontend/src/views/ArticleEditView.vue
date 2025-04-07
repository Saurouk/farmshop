<template>
  <div class="container mt-5">
    <h2>✏️ Modifier l'article</h2>
    <div class="card p-4 mt-3">
      <input v-model="form.title" class="form-control mb-3" placeholder="Titre de l'article" />
      <textarea v-model="form.content" class="form-control mb-3" rows="8" placeholder="Contenu..."></textarea>
      <div class="d-flex justify-content-end gap-2">
        <button @click="submitForm" class="btn btn-primary">💾 Enregistrer</button>
        <router-link :to="`/blog/${articleId}`" class="btn btn-outline-secondary">❌ Annuler</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const articleId = route.params.id

const form = ref({
  title: '',
  content: ''
})

const token = localStorage.getItem('access_token')
const headers = {
  Authorization: `Bearer ${token}`
}

const fetchArticle = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/blog/${articleId}/`, { headers })
    form.value = {
      title: res.data.title,
      content: res.data.content
    }
  } catch (err) {
    console.error('❌ Erreur récupération article :', err)
  }
}

const submitForm = async () => {
  try {
    await axios.put(`http://127.0.0.1:8000/api/blog/${articleId}/`, form.value, { headers })
    router.push(`/blog/${articleId}`)
  } catch (err) {
    console.error('❌ Erreur mise à jour article :', err)
    alert("Erreur lors de la mise à jour")
  }
}

onMounted(fetchArticle)
</script>

<style scoped>
.container {
  max-width: 700px;
}
</style>
