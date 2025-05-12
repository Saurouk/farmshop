<template>
  <div class="container py-5">
    <h1>Blog 📚</h1>
    <p>Découvrez nos actualités, conseils et infos agricoles.</p>

    <div v-if="articles.length">
      <div v-for="article in articles" :key="article.id" class="card my-4 shadow-sm blog-card">
        <div class="row g-0">
          <div class="col-md-4" v-if="article.thumbnail">
            <img :src="article.thumbnail" class="img-fluid rounded-start h-100 w-100 object-cover" alt="vignette" />
          </div>
          <div :class="article.thumbnail ? 'col-md-8' : 'col-12'">
            <div class="card-body">
              <h3 class="card-title">{{ article.title }}</h3>
              <p class="card-subtitle text-muted mb-1">
                Par {{ article.author }} – {{ formatDate(article.created_at) }}
              </p>
              <p class="card-text mt-2">
                {{ getExcerpt(article.content) }}...
              </p>

              <div class="d-flex justify-content-between align-items-center mt-3 flex-wrap gap-2">
                <router-link :to="`/blog/${article.id}`" class="btn btn-outline-primary">
                  Lire l'article →
                </router-link>

                <button class="btn btn-outline-danger" @click="toggleLike(article)">
                  ❤️ {{ article.likes_count }} J'aime
                </button>

                <div class="btn-group">
                  <button
                    class="btn btn-outline-secondary dropdown-toggle"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                  >
                    🔗 Partager
                  </button>
                  <ul class="dropdown-menu">
                    <li>
                      <a class="dropdown-item" :href="facebookShareUrl(article)" target="_blank">
                        Facebook
                      </a>
                    </li>
                    <li>
                      <a class="dropdown-item" :href="twitterShareUrl(article)" target="_blank">
                        Twitter
                      </a>
                    </li>
                    <li>
                      <a class="dropdown-item" :href="whatsappShareUrl(article)" target="_blank">
                        WhatsApp
                      </a>
                    </li>
                  </ul>
                </div>
              </div>

            </div>
          </div>
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
  const el = document.createElement('div')
  el.innerHTML = text
  const plainText = el.textContent || el.innerText || ''
  return plainText.length > length ? plainText.slice(0, length) : plainText
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'long', year: 'numeric'
  })
}

const toggleLike = async (article) => {
  const token = localStorage.getItem("access_token")
  if (!token) {
    alert("Connectez-vous pour aimer un article.")
    return
  }
  try {
    const res = await axios.post(
      `http://127.0.0.1:8000/api/blog/articles/${article.id}/toggle_like/`,
      {},
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    )
    article.likes_count = res.data.likes_count
  } catch (err) {
    console.error("❌ Erreur lors du like :", err)
  }
}

const facebookShareUrl = (article) =>
  `https://www.facebook.com/sharer/sharer.php?u=http://localhost:5173/blog/${article.id}`

const twitterShareUrl = (article) =>
  `https://twitter.com/intent/tweet?url=http://localhost:5173/blog/${article.id}&text=${encodeURIComponent(article.title)}`

const whatsappShareUrl = (article) =>
  `https://api.whatsapp.com/send?text=${encodeURIComponent(article.title)}%20http://localhost:5173/blog/${article.id}`
</script>

<style scoped>
.blog-card {
  overflow: hidden;
  border-radius: 10px;
}
.object-cover {
  object-fit: cover;
}
</style>
