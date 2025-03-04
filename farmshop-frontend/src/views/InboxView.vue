<template>
  <div class="container">
    <h2>📩 Boîte de Réception</h2>
    <div v-if="messages.length">
      <div v-for="message in messages" :key="message.id" class="message-card">
        <p><strong>De :</strong> {{ message.sender.username }}</p>
        <p>{{ message.content }}</p>
        <p class="text-muted">{{ new Date(message.created_at).toLocaleString() }}</p>
      </div>
    </div>
    <p v-else>Aucun message reçu.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const messages = ref([]);

onMounted(async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/users/messages/", {
      headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
    });
    messages.value = response.data;
  } catch (error) {
    console.error("❌ Erreur lors du chargement des messages :", error);
  }
});
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
