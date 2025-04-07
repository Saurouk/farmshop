<template>
  <div class="container mt-4">
    <div v-if="article" class="card shadow-sm p-4">
      <div v-if="isEditing">
        <input v-model="form.title" class="form-control mb-3" placeholder="Titre" />
        <textarea v-model="form.content" class="form-control mb-3" rows="6" placeholder="Contenu de l'article" />
        <div class="d-flex justify-content-end gap-2">
          <button @click="saveChanges" class="btn btn-primary">💾 Enregistrer</button>
          <button @click="cancelEdit" class="btn btn-outline-secondary">Annuler</button>
        </div>
      </div>
      <div v-else>
        <h2>{{ article.title }}</h2>
        <p class="text-muted">🕒 {{ formatDate(article.created_at) }}</p>
        <p>{{ article.content }}</p>
        <button v-if="isStaff" @click="startEdit" class="btn btn-outline-warning mt-2">✏️ Modifier</button>
      </div>
    </div>
    <div v-else class="text-center mt-5">
      <p>Chargement de l'article...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const article = ref(null)
const form = ref({ title: '', content: '' })
const isEditing = ref(false)

const token = localStorage.getItem("access_token")
const headers = token ? { Authorization: `Bearer ${token}` } : {}

const isStaff = ref(false)

const fetchArticle = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/blog/${route.params.id}/`, { headers })
    article.value = res.data
    form.value = { title: res.data.title, content: res.data.content }
  } catch (err) {
    console.error("Erreur de chargement :", err)
  }
}

const checkIfAdmin = async () => {
  if (!token) return
  try {
    const res = await axios.get("http://127.0.0.1:8000/api/users/me/", { headers })
    isStaff.value = res.data.is_staff
  } catch (err) {
    console.error("Erreur lors de la vérification admin :", err)
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleString('fr-FR', {
    dateStyle: 'medium',
    timeStyle: 'short'
  })
}

const startEdit = () => {
  isEditing.value = true
}

const cancelEdit = () => {
  form.value = { title: article.value.title, content: article.value.content }
  isEditing.value = false
}

const saveChanges = async () => {
  try {
    const res = await axios.put(`http://127.0.0.1:8000/api/blog/${route.params.id}/`, form.value, { headers })
    article.value = res.data
    isEditing.value = false
  } catch (err) {
    console.error("Erreur lors de la mise à jour :", err)
    alert("Erreur lors de la mise à jour de l'article.")
  }
}

onMounted(() => {
  fetchArticle()
  checkIfAdmin()
})
</script>

<style scoped>
.container {
  max-width: 800px;
}
</style>
