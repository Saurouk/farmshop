<template>
  <div class="profile-container">
    <h2>👤 Mon Profil</h2>

    <div v-if="user" class="profile-info">
      <!-- Image de profil -->
      <img :src="user.profile_picture ? 'http://127.0.0.1:8000' + user.profile_picture : defaultAvatar" alt="Photo de profil" class="profile-pic">

      <p><strong>Nom d'utilisateur :</strong> {{ user.username }}</p>
      <p><strong>Email :</strong> {{ user.email }}</p>

      <!-- Formulaire d'upload d'une nouvelle photo de profil -->
      <input type="file" @change="uploadProfilePicture" />

      <h3>📩 Boîte de réception</h3>
      <ul v-if="messages.length">
        <li v-for="msg in messages" :key="msg.id">
          <strong>{{ msg.sender }}:</strong> {{ msg.content }}
          <span v-if="!msg.is_read" class="unread">🔵 Non lu</span>
        </li>
      </ul>
      <p v-else>Aucun message reçu.</p>

      <h3>📩 Contacter l'admin</h3>
      <p>Admin : <strong>{{ user.admin_contact.username }}</strong></p>
      <p>Email : <a :href="'mailto:' + user.admin_contact.email">{{ user.admin_contact.email }}</a></p>

      <textarea v-model="messageContent" placeholder="Écrire un message"></textarea>
      <button class="contact-admin" @click="contactAdmin">✉️ Envoyer</button>
    </div>

    <div v-else class="loading">Chargement du profil...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const user = ref(null)
const messages = ref([])
const messageContent = ref("")
const defaultAvatar = '/default-avatar.png'

onMounted(async () => {
  try {
    const token = localStorage.getItem('access_token')

    // Récupérer les infos de l'utilisateur
    const response = await axios.get('http://127.0.0.1:8000/api/users/me/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    user.value = response.data

    // Récupérer les messages reçus
    const messagesResponse = await axios.get('http://127.0.0.1:8000/api/users/messages/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    messages.value = messagesResponse.data
  } catch (error) {
    console.error('❌ Erreur lors du chargement du profil :', error)
  }
})

const contactAdmin = async () => {
  try {
    const token = localStorage.getItem('access_token')
    await axios.post('http://127.0.0.1:8000/api/users/messages/', {
      recipient: user.value.admin_contact.username,
      content: messageContent.value
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert("📨 Message envoyé à l'admin !")
    messageContent.value = ""
  } catch (error) {
    console.error("❌ Erreur lors de l'envoi du message :", error)
  }
}

const uploadProfilePicture = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('profile_picture', file)

  try {
    const token = localStorage.getItem('access_token')
    await axios.patch('http://127.0.0.1:8000/api/users/me/', formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    alert("📸 Photo de profil mise à jour !")
    location.reload()
  } catch (error) {
    console.error("❌ Erreur lors de l'upload :", error)
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  background: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  text-align: center;
}

.profile-info p {
  font-size: 1.2rem;
}

.profile-pic {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  margin-bottom: 10px;
  object-fit: cover;
}

.contact-admin, input[type="file"] {
  display: block;
  margin: 10px auto;
  padding: 10px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.contact-admin:hover {
  background: #0056b3;
}
</style>
