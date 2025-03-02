<template>
  <nav class="navbar">
    <router-link to="/">🏠 Accueil</router-link>
    <router-link to="/products">🛍️ Produits</router-link>
    <router-link to="/blog">📝 Blog</router-link>

    <div class="auth-links">
      <span v-if="isLoggedIn">👤 {{ username }}</span>
      <router-link v-if="!isLoggedIn" to="/login">🔐 Connexion</router-link>
      <button v-if="isLoggedIn" @click="logout">🚪 Déconnexion</button>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const username = ref(""); // Stocke le nom d'utilisateur
const isLoggedIn = computed(() => !!localStorage.getItem("access_token"));

// Récupérer les infos du user connecté
const fetchUser = async () => {
  try {
    if (!isLoggedIn.value) return;

    const response = await axios.get("http://127.0.0.1:8000/api/users/me/", {
      headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
    });
    username.value = response.data.username;
  } catch (error) {
    console.error("❌ Erreur lors de la récupération de l'utilisateur :", error);
    logout();
  }
};

// Se déconnecter
const logout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  username.value = "";
  router.push("/login");
};

// Charger l'utilisateur connecté au démarrage
onMounted(fetchUser);
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  padding: 15px;
  background: #007bff;
  color: white;
}
.auth-links {
  display: flex;
  gap: 15px;
}
button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
}
button:hover {
  text-decoration: underline;
}
</style>
