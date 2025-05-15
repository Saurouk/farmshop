<template>
  <div class="dashboard-stats">
    <h2 class="mb-4">📊 Statistiques</h2>

    <h4 class="mt-4">Produits</h4>

    <div class="mb-3">
      <select v-model="selectedProductFilter" class="form-select w-auto mx-auto">
        <option value="all">Tous les produits</option>
        <option value="out_of_stock">En rupture</option>
        <option value="popular">Populaires</option>
        <option value="most_viewed">Les plus vus</option>
      </select>
    </div>

    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Nom</th>
          <th>Likes</th>
          <th>Stock</th>
          <th>Vues</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in filteredProducts" :key="product.id">
          <td>{{ product.name }}</td>
          <td>{{ product.likes_count }}</td>
          <td>{{ product.stock }}</td>
          <td>{{ product.views }}</td>
        </tr>
      </tbody>
    </table>

    <h4 class="mt-5">Articles de Blog</h4>

    <div class="mb-3">
      <select v-model="selectedArticleFilter" class="form-select w-auto mx-auto">
        <option value="all">Tous les articles</option>
        <option value="most_commented">Les plus commentés</option>
        <option value="most_viewed">Les plus vus</option>
      </select>
    </div>

    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Titre</th>
          <th>Auteur</th>
          <th>Commentaires</th>
          <th>Vues</th>
          <th>Likes</th> <!-- ✅ Ajouté -->
        </tr>
      </thead>
      <tbody>
        <tr v-for="article in filteredArticles" :key="article.id">
          <td>{{ article.title }}</td>
          <td>{{ article.author }}</td>
          <td>{{ article.comments_count }}</td>
          <td>{{ article.views }}</td>
          <td>{{ article.likes_count }}</td> <!-- ✅ Ajouté -->
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const products = ref([])
const articles = ref([])
const selectedProductFilter = ref('all')
const selectedArticleFilter = ref('all')

const fetchStats = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const headers = { Authorization: `Bearer ${token}` }

    const [prodRes, blogRes] = await Promise.all([
      axios.get('http://127.0.0.1:8000/api/products/', { headers }),
      axios.get('http://127.0.0.1:8000/api/blog/articles/', { headers })
    ])

    products.value = prodRes.data.results || prodRes.data
    articles.value = blogRes.data.results || blogRes.data
  } catch (err) {
    console.error("Erreur récupération statistiques :", err)
  }
}

const filteredProducts = computed(() => {
  switch (selectedProductFilter.value) {
    case 'out_of_stock':
      return products.value.filter(p => p.stock === 0)
    case 'popular':
      return products.value.filter(p => p.likes_count > 5)
    case 'most_viewed':
      return products.value.filter(p => p.views > 50)
    default:
      return products.value
  }
})

const filteredArticles = computed(() => {
  switch (selectedArticleFilter.value) {
    case 'most_commented':
      return articles.value.filter(a => a.comments_count > 3)
    case 'most_viewed':
      return articles.value.filter(a => a.views > 100)
    default:
      return articles.value
  }
})

onMounted(fetchStats)
</script>

<style scoped>
h2, h4 {
  text-align: center;
}
table {
  background-color: white;
}
</style>
