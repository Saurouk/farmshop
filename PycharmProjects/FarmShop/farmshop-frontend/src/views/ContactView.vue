<template>
  <div class="container py-5">
    <h1 class="mb-4">Contactez-nous 📞</h1>

    <div class="mb-3">
      <label for="email" class="form-label">Votre email</label>
      <input v-model="email" type="email" class="form-control" id="email" placeholder="votre@email.com" required />
    </div>

    <div class="mb-3">
      <label for="reason" class="form-label">Raison du contact</label>
      <select v-model="reason" class="form-select" id="reason">
        <option disabled value="">Choisissez une raison</option>
        <option value="products">Nos produits</option>
        <option value="articles">Nos articles</option>
        <option value="other">Autres</option>
      </select>
    </div>

    <div class="mb-3">
      <label for="subject" class="form-label">Objet</label>
      <input v-model="subject" type="text" class="form-control" id="subject" placeholder="Objet du message" required />
    </div>

    <div class="mb-3">
      <label for="message" class="form-label">Votre message</label>
      <textarea v-model="message" class="form-control" id="message" rows="5" placeholder="Tapez votre message ici..." required></textarea>
    </div>

    <div class="text-end">
      <button class="btn btn-primary" @click="submitForm">📨 Envoyer</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const email = ref('')
const reason = ref('')
const subject = ref('')
const message = ref('')

const submitForm = async () => {
  if (!email.value || !reason.value || !subject.value || !message.value) {
    alert('Tous les champs sont obligatoires.')
    return
  }

  const payload = {
    email: email.value,
    reason: reason.value,
    subject: subject.value,
    content: message.value  // ✅ Correction ici
  }

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/contact/submit/', payload)
    alert('✅ Votre message a été envoyé.')
    email.value = ''
    reason.value = ''
    subject.value = ''
    message.value = ''
  } catch (err) {
    console.error('❌ Erreur envoi formulaire :', err)
    console.log('📩 Détail de l\'erreur backend :', err.response?.data)
    alert("Une erreur s'est produite lors de l'envoi du message.")
  }
}
</script>

<style scoped>
.container {
  max-width: 700px;
}
</style>
