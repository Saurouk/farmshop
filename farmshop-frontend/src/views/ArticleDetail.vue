<template>
  <div class="container mt-5">
    <div v-if="article">
      <h1>{{ article.title }}</h1>
      <p class="text-muted">Par {{ article.author }} – {{ formatDate(article.created_at) }}</p>
      <p>{{ article.content }}</p>
    </div>
    <div v-else class="alert alert-info">Chargement de l'article...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const article = ref(null);

onMounted(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/blog/${route.params.id}/`);
    article.value = response.data;
  } catch (error) {
    console.error('❌ Erreur chargement article:', error);
  }
});

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
};
</script>
