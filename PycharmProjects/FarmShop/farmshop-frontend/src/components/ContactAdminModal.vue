<template>
  <div class="modal-backdrop" v-if="visible">
    <div class="modal-content">
      <h4>📨 Contacter l'admin</h4>
      <select v-model="reason" class="form-select mb-2">
        <option disabled value="">Sélectionner une raison</option>
        <option>Produit</option>
        <option>Blog</option>
        <option>Commande</option>
        <option>Location</option>
        <option>Autres</option>
      </select>
      <textarea v-model="message" class="form-control mb-2" rows="4" placeholder="Votre message..."></textarea>
      <input type="file" @change="handleFile" class="form-control mb-2" />
      <div class="d-flex justify-content-end gap-2">
        <button class="btn btn-secondary" @click="$emit('close')">Annuler</button>
        <button class="btn btn-primary" @click="submitMessage">Envoyer</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const props = defineProps({ visible: Boolean, adminUsername: String })
const emit = defineEmits(['close'])

const message = ref('')
const reason = ref('')
const file = ref(null)
const toast = useToast()

const handleFile = (e) => {
  file.value = e.target.files[0]
}

const submitMessage = async () => {
  if (!reason.value || !message.value) {
    toast.warning("Veuillez compléter tous les champs.")
    return
  }

  const token = localStorage.getItem('access_token')
  const formData = new FormData()
  formData.append('recipient', props.adminUsername)
  formData.append('content', `[${reason.value}] ${message.value}`)
  if (file.value) formData.append('attachment', file.value)

  try {
    await axios.post('http://127.0.0.1:8000/api/users/messages/', formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    toast.success("Message envoyé à l'admin.")
    emit('close')
  } catch (err) {
    toast.error("Erreur lors de l'envoi.")
    console.error(err)
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0; left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
}
</style>
