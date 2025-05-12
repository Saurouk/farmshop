<template>
  <div class="container py-5">
    <div v-if="article" class="blog-detail">
      <h1 class="mb-3">{{ article.title }}</h1>
      <p class="text-muted">Par {{ article.author }} – {{ formatDate(article.created_at) }}</p>

      <div v-if="canEdit" class="text-end mb-3">
        <button @click="editArticle" class="btn btn-outline-primary btn-sm">
          ✏️ Modifier l'article
        </button>
      </div>

      <img
        v-if="article.thumbnail"
        :src="article.thumbnail"
        alt="Vignette"
        class="img-fluid rounded my-4 blog-thumbnail"
      />

      <div class="blog-content" v-html="article.content"></div>

      <div class="d-flex justify-content-start gap-2 mt-3">
        <a :href="facebookShareUrl" target="_blank" class="btn btn-outline-primary btn-sm">Partager sur Facebook</a>
        <a :href="twitterShareUrl" target="_blank" class="btn btn-outline-info btn-sm">Partager sur Twitter</a>
        <a :href="whatsappShareUrl" target="_blank" class="btn btn-outline-success btn-sm">Partager sur WhatsApp</a>
      </div>

      <hr class="my-5" />

      <h4 class="mb-3">Commentaires ({{ article.comments_count }})</h4>
      <div v-if="article.comments.length">
        <div v-for="comment in article.comments" :key="comment.id" class="mb-3 p-3 border rounded">
          <p class="mb-1"><strong>{{ comment.user }}</strong></p>
          <p class="mb-1">{{ comment.content }}</p>
          <small class="text-muted">{{ formatDate(comment.created_at) }}</small>
        </div>
      </div>
      <div v-else class="text-muted">Aucun commentaire pour cet article.</div>
    </div>

    <div v-else class="alert alert-info text-center">Chargement de l'article...</div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const article = ref(null)
const user = ref(null)
const route = useRoute()
const router = useRouter()

const fetchArticle = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/blog/articles/${route.params.id}/`)
    article.value = res.data
  } catch (err) {
    console.error('Erreur chargement article:', err)
  }
}

const fetchUser = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/users/me/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    user.value = res.data
  } catch (err) {
    console.error('Erreur chargement utilisateur:', err)
  }
}

const canEdit = computed(() => {
  if (!user.value || !article.value) return false
  return user.value.is_staff || user.value.username === article.value.author
})

const editArticle = () => {
  router.push('/admin/dashboard')
}

const formatDate = (str) => {
  return new Date(str).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

const facebookShareUrl = computed(() =>
  `https://www.facebook.com/sharer/sharer.php?u=http://localhost:5173/blog/${route.params.id}`
)

const twitterShareUrl = computed(() =>
  `https://twitter.com/intent/tweet?url=http://localhost:5173/blog/${route.params.id}&text=${encodeURIComponent(article.value?.title || '')}`
)

const whatsappShareUrl = computed(() =>
  `https://api.whatsapp.com/send?text=${encodeURIComponent(article.value?.title || '')}%20http://localhost:5173/blog/${route.params.id}`
)

onMounted(() => {
  fetchArticle()
  fetchUser()
})
</script>

<style scoped>
.blog-detail {
  max-width: 800px;
  margin: auto;
}
.blog-thumbnail {
  max-height: 400px;
  object-fit: cover;
  width: 100%;
}
.blog-content :deep(*) {
  font-size: 1.1rem;
  line-height: 1.7;
  word-break: break-word;
}
</style>
