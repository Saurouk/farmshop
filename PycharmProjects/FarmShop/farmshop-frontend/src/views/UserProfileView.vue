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
          :src="user.profile_picture ? 'http://127.0.0.1:8000' + user.profile_picture : defaultAvatar"
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

      <hr />

      <div class="section">
        <div class="d-flex justify-content-between align-items-center mb-2">
          <h5 class="mb-0">📥 Messages reçus</h5>
          <button class="btn btn-sm btn-outline-secondary" @click="toggleInbox">
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

      <div class="section">
        <h5>📨 Contacter l'admin</h5>
        <p class="mb-1">Admin : <strong>{{ user.admin_contact?.username }}</strong></p>
        <p class="mb-2">Email : <a :href="'mailto:' + user.admin_contact?.email">{{ user.admin_contact?.email }}</a></p>
        <textarea class="form-control mb-2" v-model="messageContent" rows="3" placeholder="Votre message..."></textarea>
        <input type="file" @change="handleAttachment" class="form-control mb-2" />
        <button class="btn btn-primary" @click="contactAdmin">Envoyer</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const user = ref(null)
const messages = ref([])
const loading = ref(true)
const messageContent = ref('')
const attachment = ref(null)
const defaultAvatar = '/default-avatar.png'
const showInbox = ref(true)

const toggleInbox = () => {
  showInbox.value = !showInbox.value
}

const fetchProfile = async () => {
  const token = localStorage.getItem('access_token')
  const headers = { Authorization: `Bearer ${token}` }
  try {
    const resUser = await axios.get('http://127.0.0.1:8000/api/users/me/', { headers })
    const resMessages = await axios.get('http://127.0.0.1:8000/api/users/messages/', { headers })
    user.value = resUser.data
    messages.value = resMessages.data.results || resMessages.data
  } catch (err) {
    console.error('Erreur chargement du profil :', err)
  } finally {
    loading.value = false
  }
}

const contactAdmin = async () => {
  const token = localStorage.getItem('access_token')
  const formData = new FormData()
  formData.append('recipient', user.value.admin_contact.username)
  formData.append('content', messageContent.value)
  if (attachment.value) {
    formData.append('attachment', attachment.value)
  }

  try {
    await axios.post('http://127.0.0.1:8000/api/users/messages/', formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    messageContent.value = ''
    attachment.value = null
    fetchProfile()
    alert('Message envoyé à l\'admin.')
  } catch (err) {
    console.error('Erreur envoi message :', err)
  }
}

const uploadProfilePicture = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('profile_picture', file)
  const token = localStorage.getItem('access_token')

  try {
    await axios.patch('http://127.0.0.1:8000/api/users/me/', formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    fetchProfile()
  } catch (err) {
    console.error('Erreur upload photo :', err)
  }
}

const markAsRead = async (msg) => {
  if (msg.is_read) return

  const token = localStorage.getItem('access_token')
  try {
    await axios.patch(`http://127.0.0.1:8000/api/users/messages/${msg.id}/`, {
      is_read: true
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    msg.is_read = true
  } catch (err) {
    console.error('Erreur mise à jour lecture message :', err)
  }
}

const handleAttachment = (e) => {
  attachment.value = e.target.files[0]
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
