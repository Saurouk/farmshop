<template>
  <div class="container py-5">
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Chargement...</span>
      </div>
    </div>

    <div v-else class="profile-wrapper shadow p-4 rounded bg-white">
      <div class="d-flex align-items-center gap-4 mb-4">
        <img
          :src="user.profile_picture ? user.profile_picture + '?ts=' + Date.now() : defaultAvatar"
          class="rounded-circle profile-pic"
          alt="avatar"
        />
        <div>
          <h4 class="mb-1">{{ user.username }}</h4>
          <p class="text-muted mb-0">{{ user.email }}</p>
          <label class="btn btn-sm btn-outline-primary mt-2">
            Modifier la photo
            <input type="file" hidden @change="uploadProfilePicture" />
          </label>
        </div>
      </div>

      <div class="mb-3">
        <label for="bio" class="form-label">Bio</label>
        <div v-if="!editBio">
          <p class="text-muted">{{ user.bio || 'Aucune bio renseignée.' }}</p>
          <button class="btn btn-sm btn-outline-secondary" @click="editBio = true">Modifier la bio</button>
        </div>
        <div v-else>
          <textarea
            id="bio"
            v-model="user.bio"
            class="form-control"
            rows="3"
            placeholder="Parlez un peu de vous..."
          ></textarea>
          <button class="btn btn-primary btn-sm mt-2 me-2" @click="updateBio">
            Enregistrer
          </button>
          <button class="btn btn-sm btn-secondary mt-2" @click="editBio = false">
            Annuler
          </button>
        </div>
      </div>

      <div class="mb-4">
        <h5>📬 Newsletter</h5>
        <p class="text-muted">Recevez nos dernières actualités et offres agricoles.</p>
        <button
          class="btn"
          :class="subscribed ? 'btn-danger' : 'btn-success'"
          @click="toggleNewsletter"
        >
          {{ subscribed ? 'Se désinscrire' : "S'inscrire à la newsletter" }}
        </button>
      </div>

      <hr />

      <div class="section text-center mb-4">
        <button class="btn btn-outline-danger" @click="deleteAccount">
          ❌ Supprimer mon compte
        </button>
      </div>

      <div class="section">
        <div class="d-flex justify-content-between align-items-center mb-2">
          <h5>📬 Messages reçus</h5>
          <button class="btn btn-sm btn-outline-secondary" @click="showInbox = !showInbox">
            {{ showInbox ? 'Masquer' : 'Afficher' }}
          </button>
        </div>

        <div v-if="showInbox && messages.length" class="message-list">
          <div
            v-for="msg in messages"
            :key="msg.id"
            class="message-box p-3 mb-2 border rounded"
            @click="markAsRead(msg)"
            style="cursor: pointer;"
          >
            <div class="d-flex justify-content-between">
              <strong>{{ msg.sender }}</strong>
              <span class="text-muted small">{{ formatDate(msg.created_at) }}</span>
            </div>
            <p class="mb-0">{{ msg.content }}</p>
            <span v-if="!msg.is_read" class="badge bg-info text-dark mt-1">Non lu</span>
            <div v-if="msg.attachment" class="mt-2">
              <a
                :href="msg.attachment"
                class="btn btn-sm btn-outline-secondary"
                target="_blank"
              >
                📌 Télécharger la pièce jointe
              </a>
            </div>
          </div>
        </div>
        <p v-else-if="showInbox" class="text-muted">Aucun message reçu.</p>
      </div>

      <hr />

      <div class="section text-center">
        <button class="btn btn-outline-primary" @click="showModal = true">
          📨 Contacter l'admin
        </button>
      </div>
    </div>

    <ContactAdminModal
      :visible="showModal"
      :admin-username="user?.admin_contact?.username"
      @close="showModal = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import ContactAdminModal from '@/components/ContactAdminModal.vue'

const user = ref(null)
const messages = ref([])
const loading = ref(true)
const defaultAvatar = '/default-avatar.png'
const showModal = ref(false)
const showInbox = ref(true)
const editBio = ref(false)
const subscribed = ref(false)

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const fetchProfile = async () => {
  try {
    const resUser = await axios.get('http://127.0.0.1:8000/api/users/me/', { headers })
    const resMessages = await axios.get('http://127.0.0.1:8000/api/users/messages/', { headers })
    user.value = resUser.data
    messages.value = resMessages.data.results || resMessages.data
    await checkSubscription()
  } catch (err) {
    console.error('Erreur chargement du profil :', err)
  } finally {
    loading.value = false
  }
}

const uploadProfilePicture = async (event) => {
  const file = event.target.files[0]
  if (!file || !file.type.startsWith('image/')) return alert("Seules les images sont autorisées.")
  const formData = new FormData()
  formData.append('profile_picture', file)
  try {
    await axios.patch('http://127.0.0.1:8000/api/users/me/', formData, {
      headers: { ...headers, 'Content-Type': 'multipart/form-data' }
    })
    fetchProfile()
  } catch (err) {
    console.error('Erreur upload photo :', err)
  }
}

const updateBio = async () => {
  try {
    await axios.patch('http://127.0.0.1:8000/api/users/me/', { bio: user.value.bio }, { headers })
    editBio.value = false
  } catch (err) {
    console.error('❌ Erreur mise à jour bio :', err)
  }
}

const deleteAccount = async () => {
  if (!confirm("Voulez-vous télécharger vos données avant de supprimer votre compte ?")) return
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/users/download/', {
      headers,
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${user.value.username}_donnees.zip`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    await axios.delete('http://127.0.0.1:8000/api/users/me/delete/', { headers })
    alert("Votre compte a été supprimé avec succès.")
    localStorage.clear()
    window.location.href = '/login'
  } catch (err) {
    console.error('Erreur suppression du compte :', err)
  }
}

const markAsRead = async (msg) => {
  if (msg.is_read) return
  try {
    await axios.patch(`http://127.0.0.1:8000/api/users/messages/${msg.id}/`, { is_read: true }, { headers })
    msg.is_read = true
  } catch (err) {
    console.error('Erreur lecture message :', err)
  }
}

const toggleNewsletter = async () => {
  const action = subscribed.value ? 'unsubscribe' : 'subscribe'
  try {
    const response = await axios.post(`http://127.0.0.1:8000/api/newsletter/${action}/`, {
      email: user.value.email
    })
    subscribed.value = !subscribed.value
    alert(subscribed.value ? '✅ Inscription réussie.' : '🚫 Désinscription confirmée.')
    console.log(`✅ Réponse ${action} :`, response.data)
  } catch (err) {
    console.error(`❌ Erreur ${action} newsletter :`, err)
    alert('Erreur : ' + (err.response?.data?.error || 'Impossible de modifier l\'abonnement.'))
  }
}

const checkSubscription = async () => {
  try {
    const res = await axios.post(`http://127.0.0.1:8000/api/newsletter/subscribe/`, {
      email: user.value.email
    })
    if (res.data?.message?.includes('Inscription')) {
      subscribed.value = true
    }
  } catch (err) {
    console.log('ℹ️ Résultat checkSubscription :', err.response?.data)
    if (err.response?.data?.error === 'Déjà inscrit à la newsletter.') {
      subscribed.value = true
    } else {
      subscribed.value = false
    }
  }
}

const formatDate = (str) => new Date(str).toLocaleString()

onMounted(fetchProfile)
</script>

<style scoped>
.profile-wrapper {
  max-width: 700px;
  margin: auto;
}
.profile-pic {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border: 2px solid #ccc;
}
.message-box {
  background-color: #f8f9fa;
}
.section {
  margin-top: 2rem;
}
</style>
