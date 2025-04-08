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

    <div v-if="article">
      <hr class="my-4">
      <h4>Commentaires</h4>
      <div v-if="comments.length">
        <ul class="list-group mb-3">
          <li class="list-group-item" v-for="c in comments" :key="c.id">
            <strong>{{ c.user }}</strong><br>
            {{ c.content }}
            <div class="text-muted small">{{ formatDate(c.created_at) }}</div>
            <button class="btn btn-sm btn-outline-danger mt-2" @click="reportComment(c.id)">🚨 Signaler</button>
          </li>
        </ul>
      </div>
      <div v-else>
        <p class="text-muted">Aucun commentaire pour le moment.</p>
      </div>
      <div class="mb-3">
        <textarea v-model="commentContent" class="form-control" placeholder="Ajouter un commentaire..." rows="3" />
        <div class="d-flex justify-content-end mt-2">
          <button @click="submitComment" class="btn btn-primary">💬 Publier</button>
        </div>
      </div>
    </div>

    <div v-else class="text-center mt-5">
      <p>Chargement de l'article...</p>
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
const form = ref({ title: '', content: '' })
const isEditing = ref(false)

const token = localStorage.getItem("access_token")
const headers = token ? { Authorization: `Bearer ${token}` } : {}

const isStaff = ref(false)
const comments = ref([])
const commentContent = ref('')

const fetchArticle = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/blog/articles/${route.params.id}/`, { headers })
    article.value = res.data
    form.value = { title: res.data.title, content: res.data.content }
  } catch (err) {
    console.error("❌ Erreur fetchArticle :", err.response || err)
  }
}

const fetchComments = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/blog/comments/?article=${route.params.id}`, { headers })
    comments.value = res.data
  } catch (err) {
    console.error("Erreur chargement commentaires :", err)
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
    const res = await axios.put(`http://127.0.0.1:8000/api/blog/articles/${route.params.id}/`, form.value, { headers })
    article.value = res.data
    isEditing.value = false
  } catch (err) {
    console.error("Erreur lors de la mise à jour :", err)
    alert("Erreur lors de la mise à jour de l'article.")
  }
}

const submitComment = async () => {
  if (!token) {
    router.push('/login')
    return
  }
  try {
    await axios.post("http://127.0.0.1:8000/api/blog/comments/", {
      article: route.params.id,
      content: commentContent.value
    }, { headers })
    commentContent.value = ''
    fetchComments()
  } catch (err) {
    console.error("❌ Erreur publication commentaire:", err.response || err)
    alert("Erreur lors de la publication du commentaire.")
  }
}

const reportComment = async (commentId) => {
  if (!token) {
    router.push('/login')
    return
  }

  const reason = prompt("Raison du signalement :")
  if (!reason) return

  try {
    await axios.post("http://127.0.0.1:8000/api/blog/reports/", {
      reported_comment: commentId,
      reason: reason
    }, { headers })
    alert("✅ Commentaire signalé !")
  } catch (err) {
    console.error("❌ Erreur signalement :", err.response || err)
    alert("Erreur lors du signalement.")
  }
}

onMounted(() => {
  fetchArticle()
  fetchComments()
  checkIfAdmin()
})
</script>

<style scoped>
.container {
  max-width: 800px;
}
</style>
