<template>
  <div class="container py-5">
    <h2>📩 Boîte de Réception</h2>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Chargement...</span>
      </div>
    </div>

    <div v-else>
      <div v-if="messages.length">
        <div v-for="message in messages" :key="message.id" class="message-card">
          <p><strong>De :</strong> {{ message.sender }}</p>
          <p>{{ message.content }}</p>
          <p class="text-muted small">{{ formatDate(message.created_at) }}</p>
          <div v-if="message.attachment" class="mt-2">
            <a
              :href="'http://127.0.0.1:8000' + message.attachment"
              class="btn btn-sm btn-outline-secondary"
              target="_blank"
            >
              📎 Pièce jointe
            </a>
          </div>
        </div>
      </div>
      <p v-else>Aucun message reçu.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const messages = ref([]);
const loading = ref(true);

const fetchMessages = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/users/messages/", {
      headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
    });
    messages.value = response.data;
  } catch (error) {
    console.error("❌ Erreur lors du chargement des messages :", error);
  } finally {
    loading.value = false;
  }
};

const formatDate = (str) => new Date(str).toLocaleString();

onMounted(fetchMessages);
</script>

<style scoped>
.message-card {
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 5px;
  background: #f9f9f9;
}
</style>
