<template>
  <div class="container py-5">
    <div v-if="article" class="blog-detail">
      <h1 class="mb-3">{{ article.title }}</h1>
      <p class="text-muted">Par {{ article.author }} – {{ formatDate(article.created_at) }}</p>

      <img
        v-if="article.thumbnail"
        :src="article.thumbnail"
        alt="Vignette"
        class="img-fluid rounded my-4 blog-thumbnail"
      />

      <div class="blog-content" v-html="article.content"></div>

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
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const article = ref(null)
const route = useRoute()

const fetchArticle = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/blog/articles/${route.params.id}/`)
    article.value = res.data
  } catch (err) {
    console.error('Erreur chargement article:', err)
  }
}

const formatDate = (str) => {
  return new Date(str).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

onMounted(fetchArticle)
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
