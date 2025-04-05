<template>
  <div class="blog-admin">
    <h2 class="mb-4">📝 Gestion du blog</h2>

    <div class="btn-group mb-4">
      <button @click="activeSection = 'articles'" :class="sectionClass('articles')">📄 Articles</button>
      <button @click="activeSection = 'comments'" :class="sectionClass('comments')">💬 Commentaires</button>
      <button @click="activeSection = 'reports'" :class="sectionClass('reports')">
        🚨 Signalements <span v-if="reports.length" class="badge bg-danger ms-2">{{ reports.length }}</span>
      </button>
    </div>

    <div v-if="activeSection === 'articles'">
      <h3 class="mb-3">📰 Liste des articles</h3>
      <button @click="showCreateForm" class="btn btn-success mb-3">+ Nouvel article</button>

      <div v-if="createMode || editingArticle" class="card card-body shadow-sm mb-4">
        <input v-model="form.title" class="form-control mb-2" placeholder="Titre de l'article" />
        <textarea v-model="form.content" class="form-control mb-2" rows="4" placeholder="Contenu..."></textarea>
        <div class="d-flex justify-content-end gap-2">
          <button @click="submitForm" class="btn btn-primary">✅ {{ editingArticle ? 'Mettre à jour' : 'Publier' }}</button>
          <button @click="resetForm" class="btn btn-outline-secondary">❌ Annuler</button>
        </div>
      </div>

      <ul class="list-group shadow-sm">
        <li class="list-group-item d-flex justify-content-between align-items-center" v-for="a in articles" :key="a.id">
          <div>
            <strong>{{ a.title }}</strong>
            <div class="text-muted small">📅 {{ formatDate(a.created_at) }}</div>
          </div>
          <div class="d-flex gap-2">
            <button @click="editArticle(a)" class="btn btn-sm btn-outline-warning">✏️ Éditer</button>
            <button @click="deleteArticle(a.id)" class="btn btn-sm btn-outline-danger">🗑️ Supprimer</button>
          </div>
        </li>
      </ul>
    </div>

    <div v-if="activeSection === 'comments'">
      <h3 class="mb-3">💬 Tous les commentaires</h3>
      <ul class="list-group">
        <li class="list-group-item" v-for="c in comments" :key="c.id">
          <strong>{{ c.user }}</strong> sur <em>{{ c.article_title }}</em><br />
          {{ c.content }}
          <div class="text-muted small">📅 {{ formatDate(c.created_at) }}</div>
        </li>
      </ul>
    </div>

    <div v-if="activeSection === 'reports'">
      <h3 class="mb-3">🚨 Signalements en attente</h3>
      <ul class="list-group">
        <li class="list-group-item d-flex justify-content-between align-items-start bg-warning-subtle" v-for="r in reports" :key="r.id">
          <div>
            <strong>Commentaire #{{ r.reported_comment }}</strong><br />
            <span class="text-muted small">Motif : {{ r.reason }}</span>
          </div>
          <div class="d-flex gap-2">
            <button @click="deleteComment(r.reported_comment)" class="btn btn-sm btn-danger">🗑️ Supprimer</button>
            <button @click="ignoreReport(r.reported_comment)" class="btn btn-sm btn-outline-dark">🚫 Ignorer</button>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const activeSection = ref('articles')
const articles = ref([])
const comments = ref([])
const reports = ref([])

const form = ref({ title: '', content: '' })
const createMode = ref(false)
const editingArticle = ref(null)

const token = localStorage.getItem("access_token")
const headers = { Authorization: `Bearer ${token}` }

const fetchAll = async () => {
  const [a, c, r] = await Promise.all([
    axios.get("http://127.0.0.1:8000/api/blog/", { headers }),
    axios.get("http://127.0.0.1:8000/api/blog/comments/", { headers }),
    axios.get("http://127.0.0.1:8000/api/blog/admin/reported-comments/", { headers })
  ])
  articles.value = a.data
  comments.value = c.data
  reports.value = r.data
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'long', year: 'numeric'
  })
}

const showCreateForm = () => {
  resetForm()
  createMode.value = true
}

const submitForm = async () => {
  try {
    if (editingArticle.value) {
      await axios.put(`http://127.0.0.1:8000/api/blog/${editingArticle.value.id}/`, form.value, { headers })
    } else {
      await axios.post("http://127.0.0.1:8000/api/blog/", form.value, { headers })
    }
    resetForm()
    fetchAll()
  } catch (err) {
    console.error("❌ Erreur lors de l'envoi de l'article :", err.response)
    alert("Erreur lors de l'envoi de l'article")
  }
}

const editArticle = (article) => {
  editingArticle.value = article
  form.value = { title: article.title, content: article.content }
  createMode.value = false
}

const resetForm = () => {
  form.value = { title: '', content: '' }
  createMode.value = false
  editingArticle.value = null
}

const deleteArticle = async (id) => {
  await axios.delete(`http://127.0.0.1:8000/api/blog/${id}/`, { headers })
  fetchAll()
}

const deleteComment = async (id) => {
  await axios.delete(`http://127.0.0.1:8000/api/blog/admin/delete-comment/${id}/`, { headers })
  fetchAll()
}

const ignoreReport = async (id) => {
  await axios.patch(`http://127.0.0.1:8000/api/blog/admin/ignore-report/${id}/`, {}, { headers })
  fetchAll()
}

const sectionClass = (section) => {
  return {
    'btn': true,
    'btn-primary': activeSection.value === section,
    'btn-outline-primary': activeSection.value !== section
  }
}

onMounted(fetchAll)
</script>

<style scoped>
.blog-admin {
  text-align: left;
  max-width: 850px;
  margin: auto;
  padding-bottom: 50px;
}
.btn-group button {
  margin-right: 10px;
}
</style>
