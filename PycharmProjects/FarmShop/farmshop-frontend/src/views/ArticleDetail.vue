<template>
  <div class="container mt-4">
    <div v-if="article" class="card shadow-sm p-4">
      <div v-if="isEditing">
        <input v-model="form.title" class="form-control mb-3" placeholder="Titre" />
        <textarea v-model="form.content" class="form-control mb-3" rows="6" placeholder="Contenu HTML..." />
        <div class="d-flex justify-content-end gap-2">
          <button @click="saveChanges" class="btn btn-primary">Enregistrer</button>
          <button @click="cancelEdit" class="btn btn-outline-secondary">Annuler</button>
        </div>
      </div>
      <div v-else>
        <h2>{{ article.title }}</h2>
        <p class="text-muted">🕒 {{ formatDate(article.created_at) }}</p>
        <div v-html="article.content" class="article-body" />
        <button v-if="isStaff" @click="startEdit" class="btn btn-outline-warning mt-2">✏️ Modifier</button>
      </div>
    </div>

    <div v-if="article">
      <hr class="my-4" />
      <h4>Commentaires</h4>

      <div v-if="comments.length">
        <ul class="list-group mb-3">
          <li class="list-group-item" v-for="c in comments" :key="c.id">
            <strong>{{ c.user }}</strong><br />
            <div>{{ c.content }}</div>
            <div class="text-muted small">{{ formatDate(c.created_at) }}</div>
            <button
              v-if="isAuthenticated"
              class="btn btn-sm btn-outline-danger mt-2"
              @click="openReportModal(c.id)"
            >
              🚨 Signaler
            </button>
          </li>
        </ul>
      </div>
      <div v-else>
        <p class="text-muted">Aucun commentaire pour le moment.</p>
      </div>

      <div v-if="isAuthenticated" class="mb-3">
        <textarea v-model="commentContent" class="form-control" placeholder="Ajouter un commentaire..." rows="3" />
        <div class="d-flex justify-content-end mt-2">
          <button @click="submitComment" class="btn btn-primary">💬 Publier</button>
        </div>
        <div v-if="successMessage" class="alert alert-success mt-2">{{ successMessage }}</div>
        <div v-if="errorMessage" class="alert alert-warning mt-2">{{ errorMessage }}</div>
      </div>
      <div v-else class="alert alert-info">Veuillez vous connecter pour commenter.</div>
    </div>

    <div v-else class="text-center mt-5">
      <p>Chargement de l'article...</p>
    </div>

    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h5>Signaler un commentaire</h5>
        <select v-model="reportReason" class="form-select mb-2">
          <option disabled value="">Choisir une raison</option>
          <option>Propos injurieux</option>
          <option>Hors sujet</option>
          <option>Spam</option>
          <option>Autre</option>
        </select>
        <textarea v-model="reportMessage" class="form-control mb-2" placeholder="Message (optionnel)" rows="3" />
        <div class="d-flex justify-content-end gap-2">
          <button class="btn btn-outline-secondary" @click="closeModal">Annuler</button>
          <button class="btn btn-danger" @click="submitReport">Envoyer</button>
        </div>
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

const article = ref(null)
const comments = ref([])
const commentContent = ref('')
const isEditing = ref(false)
const isStaff = ref(false)
const isAuthenticated = ref(false)

const form = ref({ title: '', content: '' })

const showModal = ref(false)
const commentToReport = ref(null)
const reportReason = ref('')
const reportMessage = ref('')

const successMessage = ref('')
const errorMessage = ref('')

const token = localStorage.getItem("access_token")
const headers = token ? { Authorization: `Bearer ${token}` } : {}

const fetchArticle = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/blog/articles/${route.params.id}/`, { headers })
    article.value = res.data
    form.value = { title: res.data.title, content: res.data.content }
  } catch (err) {
    console.error("❌ Erreur fetchArticle :", err)
  }
}

const fetchComments = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/blog/comments/?article=${route.params.id}`, { headers })
    comments.value = Array.isArray(res.data.results) ? res.data.results : []
  } catch (err) {
    console.error("Erreur chargement commentaires :", err)
  }
}

const checkAuth = async () => {
  if (!token) return
  try {
    const res = await axios.get("http://127.0.0.1:8000/api/users/me/", { headers })
    isStaff.value = res.data.is_staff
    isAuthenticated.value = true
  } catch (err) {
    console.error("Erreur auth :", err)
  }
}

const formatDate = (date) => new Date(date).toLocaleString('fr-FR', {
  dateStyle: 'medium',
  timeStyle: 'short'
})

const startEdit = () => isEditing.value = true
const cancelEdit = () => {
  form.value = { title: article.value.title, content: article.value.content }
  isEditing.value = false
}

const saveChanges = async () => {
  const formData = new FormData()
  formData.append('title', form.value.title)
  formData.append('content', form.value.content)
  formData.append('is_published', true)

  try {
    const res = await axios.put(`http://127.0.0.1:8000/api/blog/articles/${route.params.id}/`, formData, {
      headers: { ...headers, 'Content-Type': 'multipart/form-data' }
    })
    article.value = res.data
    isEditing.value = false
  } catch (err) {
    console.error("❌ Erreur lors de la mise à jour de l'article :", err)
    alert("Erreur lors de la mise à jour de l'article.")
  }
}

const submitComment = async () => {
  if (!commentContent.value.trim()) {
    errorMessage.value = "Votre commentaire est vide."
    setTimeout(() => errorMessage.value = '', 4000)
    return
  }
  try {
    await axios.post("http://127.0.0.1:8000/api/blog/comments/", {
      article: route.params.id,
      content: commentContent.value
    }, { headers })
    commentContent.value = ''
    await fetchComments()
    successMessage.value = "💬 Commentaire publié avec succès."
    setTimeout(() => successMessage.value = '', 4000)
  } catch (err) {
    errorMessage.value = "Erreur lors de la publication du commentaire."
    setTimeout(() => errorMessage.value = '', 4000)
  }
}

const openReportModal = (id) => {
  commentToReport.value = id
  showModal.value = true
  reportReason.value = ''
  reportMessage.value = ''
}

const closeModal = () => showModal.value = false

const submitReport = async () => {
  if (!reportReason.value) {
    alert("Veuillez sélectionner une raison.")
    return
  }
  try {
    await axios.post("http://127.0.0.1:8000/api/blog/reports/", {
      reported_comment: commentToReport.value,
      reason: `${reportReason.value} - ${reportMessage.value}`
    }, { headers })
    successMessage.value = "🚨 Commentaire signalé avec succès. Merci !"
    closeModal()
  } catch (err) {
    if (err.response?.status === 400) {
      errorMessage.value = "⚠️ Vous avez déjà signalé ce commentaire."
    } else {
      errorMessage.value = "Erreur lors du signalement."
    }
    closeModal()
  } finally {
    setTimeout(() => {
      successMessage.value = ''
      errorMessage.value = ''
    }, 4000)
  }
}

onMounted(() => {
  fetchArticle()
  fetchComments()
  checkAuth()
})
</script>

<style scoped>
.container {
  max-width: 800px;
}
.article-body {
  margin-top: 1rem;
}
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}
</style>
