<template>
  <div class="container py-5">
    <h1>Blog 📚</h1>
    <p>Découvrez nos actualités, conseils et infos agricoles.</p>

    <div v-if="articles.length">
      <div v-for="article in articles" :key="article.id" class="card my-3">
        <div class="card-body">
          <h3 class="card-title">{{ article.title }}</h3>
          <p class="card-subtitle text-muted">
            Par {{ article.author }} – {{ formatDate(article.created_at) }}
          </p>
          <p class="card-text mt-2">
            {{ getExcerpt(article.content) }}...
          </p>
          <router-link :to="`/blog/${article.id}`" class="btn btn-outline-primary">
            Lire l'article →
          </router-link>
        </div>
      </div>

      <div class="pagination d-flex justify-content-center gap-3 mt-4">
        <button class="btn btn-outline-secondary" @click="prevPage" :disabled="!previous">← Précédent</button>
        <span>Page {{ page }}</span>
        <button class="btn btn-outline-secondary" @click="nextPage" :disabled="!next">Suivant →</button>
      </div>
    </div>

    <div v-else class="alert alert-info">Chargement des articles...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const articles = ref([])
const page = ref(1)
const next = ref(null)
const previous = ref(null)

const fetchArticles = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/blog/articles/?page=${page.value}`)
    articles.value = res.data.results
    next.value = res.data.next
    previous.value = res.data.previous
  } catch (err) {
    console.error("❌ Erreur chargement articles :", err)
  }
}

const nextPage = () => {
  if (next.value) {
    page.value++
    fetchArticles()
  }
}

const prevPage = () => {
  if (previous.value && page.value > 1) {
    page.value--
    fetchArticles()
  }
}

onMounted(fetchArticles)

const getExcerpt = (text, length = 150) => {
  return text.length > length ? text.slice(0, length) : text
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'long', year: 'numeric'
  })
}
</script>

<style scoped>
.card {
  border: 1px solid #ccc;
}
.card-title {
  font-weight: bold;
}
</style>
