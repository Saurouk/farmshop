<template>
  <div class="blog-admin">
    <h2 class="mb-4">Gestion du blog</h2>

    <div class="btn-group mb-4">
      <button @click="activeSection = 'articles'" :class="sectionClass('articles')">Articles</button>
      <button @click="activeSection = 'comments'" :class="sectionClass('comments')">Commentaires</button>
      <button @click="activeSection = 'reports'" :class="sectionClass('reports')">
        Signalements <span v-if="reports.length" class="badge bg-danger ms-2">{{ reports.length }}</span>
      </button>
      <button @click="activeSection = 'resolved'" :class="sectionClass('resolved')">
        Signalés traités <span v-if="resolvedReports.length" class="badge bg-secondary ms-2">{{ resolvedReports.length }}</span>
      </button>
    </div>

    <!-- ARTICLES -->
    <div v-if="activeSection === 'articles'">
      <h3>Liste des articles</h3>
      <button @click="showCreateForm" class="btn btn-success mb-3">+ Nouvel article</button>

      <div v-if="createMode || editingArticle" class="card card-body shadow-sm mb-4">
        <input v-model="form.title" class="form-control mb-2" placeholder="Titre de l'article" />
        <textarea v-model="form.content" class="form-control mb-2" rows="6" placeholder="Contenu HTML..."></textarea>
        <input type="file" class="form-control mb-2" @change="handleThumbnail" />
        <div class="form-check mb-2">
          <input type="checkbox" class="form-check-input" v-model="form.is_published" id="pubCheck" />
          <label class="form-check-label" for="pubCheck">Publié</label>
        </div>
        <div class="d-flex justify-content-end gap-2">
          <button @click="submitForm" class="btn btn-primary">{{ editingArticle ? 'Mettre à jour' : 'Publier' }}</button>
          <button @click="resetForm" class="btn btn-outline-secondary">Annuler</button>
        </div>
      </div>

      <ul class="list-group shadow-sm">
        <li class="list-group-item d-flex justify-content-between align-items-center" v-for="a in articles" :key="a.id">
          <div>
            <strong>{{ a.title }}</strong>
            <div class="text-muted small">🗕 {{ formatDate(a.created_at) }}</div>
          </div>
          <div class="d-flex gap-2">
            <button @click="editArticle(a)" class="btn btn-sm btn-outline-warning">Éditer</button>
            <button @click="deleteArticle(a.id)" class="btn btn-sm btn-outline-danger">Supprimer</button>
          </div>
        </li>
      </ul>

      <div class="pagination-controls d-flex justify-content-center gap-3 mt-3">
        <button class="btn btn-outline-secondary" @click="changePageArticles(-1)" :disabled="!prevArticles">←</button>
        <span>Page {{ pageArticles }}</span>
        <button class="btn btn-outline-secondary" @click="changePageArticles(1)" :disabled="!nextArticles">→</button>
      </div>
    </div>

    <!-- COMMENTAIRES -->
    <div v-if="activeSection === 'comments'">
      <h3>Tous les commentaires</h3>
      <ul class="list-group">
        <li class="list-group-item d-flex justify-content-between align-items-start" v-for="c in comments" :key="c.id">
          <div>
            <strong>{{ c.user }}</strong> sur <em>{{ c.article_title }}</em><br />
            {{ c.content }}
            <div class="text-muted small">🗕 {{ formatDate(c.created_at) }}</div>
          </div>
          <button @click="deleteComment(c.id)" class="btn btn-sm btn-outline-danger ms-2">🗑</button>
        </li>
      </ul>

      <div class="pagination-controls d-flex justify-content-center gap-3 mt-3">
        <button class="btn btn-outline-secondary" @click="changePageComments(-1)" :disabled="!prevComments">←</button>
        <span>Page {{ pageComments }}</span>
        <button class="btn btn-outline-secondary" @click="changePageComments(1)" :disabled="!nextComments">→</button>
      </div>
    </div>

    <!-- SIGNALEMENTS -->
    <div v-if="activeSection === 'reports'">
      <h3>Signalements en attente</h3>
      <ul class="list-group">
        <li class="list-group-item d-flex justify-content-between align-items-start bg-warning-subtle" v-for="r in reports" :key="r.id">
          <div>
            <strong>Commentaire #{{ r.reported_comment }}</strong><br />
            <span class="text-muted small">Signalé par : {{ r.reporter }}</span><br />
            <span class="text-muted small">Motif : {{ r.reason }}</span>
          </div>
          <div class="d-flex gap-2">
            <button @click="deleteComment(r.reported_comment)" class="btn btn-sm btn-danger">Supprimer</button>
            <button @click="ignoreReport(r.reported_comment)" class="btn btn-sm btn-outline-dark">Ignorer</button>
          </div>
        </li>
      </ul>

      <div class="pagination-controls d-flex justify-content-center gap-3 mt-3">
        <button class="btn btn-outline-secondary" @click="changePageReports(-1)" :disabled="!prevReports">←</button>
        <span>Page {{ pageReports }}</span>
        <button class="btn btn-outline-secondary" @click="changePageReports(1)" :disabled="!nextReports">→</button>
      </div>
    </div>

    <!-- SIGNALEMENTS TRAITÉS -->
    <div v-if="activeSection === 'resolved'">
      <h3>Signalements traités</h3>
      <ul class="list-group">
        <li class="list-group-item d-flex justify-content-between align-items-start" v-for="r in resolvedReports" :key="r.id">
          <div>
            <strong>Commentaire #{{ r.reported_comment }}</strong><br />
            <span class="text-muted small">Signalé par : {{ r.reporter }}</span><br />
            <span class="text-muted small">Motif : {{ r.reason }}</span>
            <div class="badge bg-secondary mt-2">✅ Traité</div>
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
const resolvedReports = ref([])

const form = ref({ title: '', content: '', is_published: true, thumbnail: null })
const createMode = ref(false)
const editingArticle = ref(null)

const token = localStorage.getItem("access_token")
const headers = { Authorization: `Bearer ${token}` }

const pageArticles = ref(1)
const nextArticles = ref(null)
const prevArticles = ref(null)

const pageComments = ref(1)
const nextComments = ref(null)
const prevComments = ref(null)

const pageReports = ref(1)
const nextReports = ref(null)
const prevReports = ref(null)

const fetchAll = async () => {
  try {
    const [a, c, allReports] = await Promise.all([
      axios.get(`http://127.0.0.1:8000/api/blog/articles/?page=${pageArticles.value}`, { headers }),
      axios.get(`http://127.0.0.1:8000/api/blog/comments/?page=${pageComments.value}`, { headers }),
      axios.get(`http://127.0.0.1:8000/api/blog/reports/?page=${pageReports.value}`, { headers })
    ])

    articles.value = a.data.results
    nextArticles.value = a.data.next
    prevArticles.value = a.data.previous

    comments.value = c.data.results
    nextComments.value = c.data.next
    prevComments.value = c.data.previous

    const all = allReports.data.results
    reports.value = all.filter(r => !r.resolved)
    resolvedReports.value = all.filter(r => r.resolved)
    nextReports.value = allReports.data.next
    prevReports.value = allReports.data.previous
  } catch (err) {
    console.error("❌ Erreur lors de la récupération des données:", err)
  }
}

const showCreateForm = () => {
  resetForm()
  createMode.value = true
}

const handleThumbnail = (e) => {
  const file = e.target.files[0]
  if (file) form.value.thumbnail = file
}

const submitForm = async () => {
  const formData = new FormData()
  formData.append('title', form.value.title)
  formData.append('content', form.value.content)
  formData.append('is_published', form.value.is_published)
  if (form.value.thumbnail) {
    formData.append('thumbnail', form.value.thumbnail)
  }

  try {
    if (editingArticle.value) {
      await axios.put(`http://127.0.0.1:8000/api/blog/articles/${editingArticle.value.id}/`, formData, {
        headers: { ...headers, 'Content-Type': 'multipart/form-data' }
      })
    } else {
      await axios.post("http://127.0.0.1:8000/api/blog/articles/", formData, {
        headers: { ...headers, 'Content-Type': 'multipart/form-data' }
      })
    }
    resetForm()
    fetchAll()
  } catch (err) {
    console.error("❌ Erreur lors de l'envoi de l'article:", err)
  }
}

const editArticle = (article) => {
  editingArticle.value = article
  form.value = {
    title: article.title,
    content: article.content,
    is_published: article.is_published,
    thumbnail: null
  }
  createMode.value = false
}

const resetForm = () => {
  form.value = { title: '', content: '', is_published: true, thumbnail: null }
  createMode.value = false
  editingArticle.value = null
}

const deleteArticle = async (id) => {
  await axios.delete(`http://127.0.0.1:8000/api/blog/articles/${id}/`, { headers })
  fetchAll()
}

const deleteComment = async (id) => {
  if (!confirm("🗑 Supprimer ce commentaire ?")) return
  await axios.delete(`http://127.0.0.1:8000/api/blog/admin/delete-comment/${id}/`, { headers })
  fetchAll()
}

const ignoreReport = async (id) => {
  await axios.patch(`http://127.0.0.1:8000/api/blog/admin/ignore-report/${id}/`, {}, { headers })
  fetchAll()
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'long', year: 'numeric'
  })
}

const sectionClass = (section) => {
  return {
    'btn': true,
    'btn-primary': activeSection.value === section,
    'btn-outline-primary': activeSection.value !== section
  }
}

const changePageArticles = (step) => {
  pageArticles.value += step
  fetchAll()
}
const changePageComments = (step) => {
  pageComments.value += step
  fetchAll()
}
const changePageReports = (step) => {
  pageReports.value += step
  fetchAll()
}

onMounted(fetchAll)
</script>

<style scoped>
.blog-admin {
  max-width: 850px;
  margin: auto;
  padding-bottom: 50px;
}
.btn-group button {
  margin-right: 10px;
}
</style>
