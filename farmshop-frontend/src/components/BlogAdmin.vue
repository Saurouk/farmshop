<template>
  <div class="blog-admin">
    <h2>📝 Gestion du blog</h2>

    <div class="btn-group mb-3">
      <button @click="activeSection = 'articles'" class="btn btn-outline-primary">Articles</button>
      <button @click="activeSection = 'comments'" class="btn btn-outline-secondary">Commentaires</button>
      <button @click="activeSection = 'reports'" class="btn btn-outline-danger">Signalements</button>
    </div>

    <div v-if="activeSection === 'articles'">
      <h3>Articles</h3>
      <div class="text-start mb-2">
        <button @click="createMode = true" class="btn btn-success">+ Nouvel article</button>
      </div>
      <div v-if="createMode" class="card p-3 mb-4">
        <input v-model="newArticle.title" class="form-control mb-2" placeholder="Titre de l'article" />
        <textarea v-model="newArticle.content" class="form-control mb-2" rows="4" placeholder="Contenu..."></textarea>
        <button @click="submitArticle" class="btn btn-primary">Publier</button>
        <button @click="createMode = false" class="btn btn-link">Annuler</button>
      </div>
      <ul class="list-group">
        <li class="list-group-item d-flex justify-content-between align-items-center" v-for="a in articles" :key="a.id">
          <div>
            <strong>{{ a.title }}</strong>
            <div><small class="text-muted">{{ a.created_at }}</small></div>
          </div>
          <button @click="deleteArticle(a.id)" class="btn btn-sm btn-outline-danger">Supprimer</button>
        </li>
      </ul>
    </div>

    <div v-if="activeSection === 'comments'">
      <h3>Commentaires</h3>
      <ul class="list-group">
        <li class="list-group-item" v-for="c in comments" :key="c.id">
          <strong>{{ c.user }}</strong> sur <em>{{ c.article_title }}</em><br>
          {{ c.content }}
          <div class="text-muted small">{{ c.created_at }}</div>
        </li>
      </ul>
    </div>

    <div v-if="activeSection === 'reports'">
      <h3>Signalements</h3>
      <ul class="list-group">
        <li class="list-group-item d-flex justify-content-between align-items-start" v-for="r in reports" :key="r.id">
          <div>
            <strong>{{ r.reported_comment }}</strong><br>
            <small>{{ r.reason }}</small>
          </div>
          <div>
            <button @click="deleteComment(r.reported_comment)" class="btn btn-sm btn-danger">Supprimer</button>
            <button @click="ignoreReport(r.reported_comment)" class="btn btn-sm btn-outline-secondary ms-2">Ignorer</button>
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

const newArticle = ref({ title: '', content: '' })
const createMode = ref(false)

const fetchAll = async () => {
  const token = localStorage.getItem("access_token")
  const headers = { Authorization: `Bearer ${token}` }

  const [a, c, r] = await Promise.all([
    axios.get("http://127.0.0.1:8000/api/blog/", { headers }),
    axios.get("http://127.0.0.1:8000/api/blog/comments/", { headers }),
    axios.get("http://127.0.0.1:8000/api/blog/admin/reported-comments/", { headers }),
  ])
  articles.value = a.data
  comments.value = c.data
  reports.value = r.data
}

const submitArticle = async () => {
  const token = localStorage.getItem("access_token")
  const headers = { Authorization: `Bearer ${token}` }
  await axios.post("http://127.0.0.1:8000/api/blog/", newArticle.value, { headers })
  newArticle.value = { title: '', content: '' }
  createMode.value = false
  fetchAll()
}

const deleteArticle = async (id) => {
  const token = localStorage.getItem("access_token")
  const headers = { Authorization: `Bearer ${token}` }
  await axios.delete(`http://127.0.0.1:8000/api/blog/${id}/`, { headers })
  fetchAll()
}

const deleteComment = async (id) => {
  const token = localStorage.getItem("access_token")
  await axios.delete(`http://127.0.0.1:8000/api/blog/admin/delete-comment/${id}/`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  fetchAll()
}

const ignoreReport = async (id) => {
  const token = localStorage.getItem("access_token")
  await axios.patch(`http://127.0.0.1:8000/api/blog/admin/ignore-report/${id}/`, {}, {
    headers: { Authorization: `Bearer ${token}` }
  })
  fetchAll()
}

onMounted(fetchAll)
</script>

<style scoped>
.blog-admin {
  text-align: left;
  max-width: 800px;
  margin: auto;
}
</style>
