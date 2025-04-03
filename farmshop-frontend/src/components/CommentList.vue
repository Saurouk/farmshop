<template>
  <div class="mt-4">
    <h3>💬 Commentaires</h3>

    <div v-if="comments.length">
      <div v-for="comment in comments" :key="comment.id" class="comment-box">
        <p><strong>{{ comment.user }}</strong> :</p>
        <p>{{ comment.content }}</p>
        <p class="text-muted small">{{ formatDate(comment.created_at) }}</p>
      </div>
    </div>
    <div v-else>
      <p>Aucun commentaire pour cet article.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const comments = ref([])

const fetchComments = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/blog/comments/?article=${route.params.id}`)
    comments.value = res.data
  } catch (err) {
    console.error('❌ Erreur chargement commentaires:', err)
  }
}

onMounted(fetchComments)

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('fr-FR', {
    day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit'
  })
}
</script>

<style scoped>
.comment-box {
  border: 1px solid #eee;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
}
</style>
