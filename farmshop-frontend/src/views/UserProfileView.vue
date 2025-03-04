<template>
  <div class="profile-container">
    <h2>👤 Mon Profil</h2>

    <div v-if="user" class="profile-info">
      <img :src="user.profile_picture ? 'http://127.0.0.1:8000' + user.profile_picture : defaultAvatar" alt="Photo de profil" class="profile-pic">
      <p><strong>Nom d'utilisateur :</strong> {{ user.username }}</p>
      <p><strong>Email :</strong> {{ user.email }}</p>

      <h3>📩 Contacter l'admin</h3>
      <p>Admin : <strong>{{ user.admin_contact.username }}</strong></p>
      <p>Email : <a :href="'mailto:' + user.admin_contact.email">{{ user.admin_contact.email }}</a></p>

      <button class="contact-admin" @click="contactAdmin">✉️ Envoyer un message</button>
    </div>

    <div v-else class="loading">Chargement du profil...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const user = ref(null)
const defaultAvatar = '/default-avatar.png'  // ✅ Remplace par un avatar par défaut si besoin

onMounted(async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await axios.get('http://127.0.0.1:8000/api/users/me/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    user.value = response.data
  } catch (error) {
    console.error('❌ Erreur lors du chargement du profil :', error)
  }
})

const contactAdmin = () => {
  alert("📨 Fonctionnalité à implémenter : Envoi d'un message à l'admin !")
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

.contact-admin {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
}

.contact-admin:hover {
  background: #0056b3;
}
</style>
