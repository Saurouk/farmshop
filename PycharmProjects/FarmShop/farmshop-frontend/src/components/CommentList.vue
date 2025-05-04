<template>
  <div class="mt-5">
    <h4>🗨️ Commentaires</h4>

    <div v-if="comments.length">
      <div v-for="comment in comments" :key="comment.id" class="border p-3 my-2 rounded bg-light">
        <div class="d-flex justify-content-between align-items-start">
          <div>
            <p class="mb-1"><strong>{{ comment.user }}</strong> :</p>
            <p class="mb-0">{{ comment.content }}</p>
            <small class="text-muted">{{ formatDate(comment.created_at) }}</small>
          </div>
          <div v-if="isAuthenticated" class="ms-3">
            <button @click="reportComment(comment.id)" class="btn btn-sm btn-outline-danger">
              ⚠️ Signaler
            </button>
          </div>
        </div>
      </div>
    </div>
    <p v-else>Aucun commentaire pour cet article.</p>

    <div class="mt-4">
      <h5>Ajouter un commentaire</h5>
      <p class="form-text text-muted fst-italic" style="opacity: 0.8;">
        📝 Merci d’écrire dans un bon français et de rester respectueux. Tous les commentaires sont modérés par un administrateur.
      </p>
      <textarea v-model="newComment" placeholder="Écrivez votre commentaire ici..." rows="4" class="form-control"></textarea>
      <div class="text-danger mt-2" v-if="error">{{ error }}</div>
      <button @click="submitComment" class="btn btn-primary mt-2">Publier</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const comments = ref([])
const newComment = ref("")
const error = ref("")

const isAuthenticated = computed(() => !!localStorage.getItem('access_token'))

const fetchComments = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/blog/comments/?article=${route.params.id}`)
    comments.value = res.data
  } catch (err) {
    console.error("❌ Erreur récupération des commentaires :", err)
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) {
    error.value = "Veuillez écrire un commentaire avant de publier."
    return
  }

  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }

  try {
    await axios.post('http://127.0.0.1:8000/api/blog/comments/', {
      article: route.params.id,
      content: newComment.value
    }, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })

    newComment.value = ""
    error.value = ""
    await fetchComments()
  } catch (err) {
    console.error("❌ Erreur envoi du commentaire :", err)
    error.value = "Une erreur est survenue."
  }
}

const reportComment = async (commentId) => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    router.push('/login')
    return
  }

  if (!confirm("Voulez-vous vraiment signaler ce commentaire ?")) return

  try {
    await axios.post('http://127.0.0.1:8000/api/blog/reports/', {
      reported_comment: commentId,
      reason: "Contenu inapproprié"
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })

    alert("🚨 Le commentaire a été signalé. Merci pour votre vigilance.")
  } catch (err) {
    console.error("❌ Erreur lors du signalement :", err)
    alert("Une erreur est survenue lors du signalement.")
  }
}

onMounted(fetchComments)
watch(() => route.params.id, fetchComments)

const formatDate = (date) => {
  return new Date(date).toLocaleString('fr-FR', {
    dateStyle: 'medium',
    timeStyle: 'short'
  })
}
</script>

<style scoped>
textarea {
  resize: none;
}
</style>
