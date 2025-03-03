<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2>🔐 Connexion</h2>
      <p>Connectez-vous à votre compte FarmShop.</p>

      <form @submit.prevent="login">
        <input v-model="username" type="text" placeholder="Nom d'utilisateur" required />
        <input v-model="password" type="password" placeholder="Mot de passe" required />
        <button type="submit">Se connecter</button>
      </form>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

      <p>Pas encore de compte ? <router-link to="/register">Inscrivez-vous</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import auth from "@/stores/auth";  // ✅ Importer l'état global

const username = ref("");
const password = ref("");
const errorMessage = ref("");
const router = useRouter();

const login = async () => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/auth/login/", {
      username: username.value,
      password: password.value,
    });

    // ✅ Stocker les tokens JWT et le username
    auth.setUser({ username: username.value });
    localStorage.setItem("access_token", response.data.access);
    localStorage.setItem("refresh_token", response.data.refresh);

    // ✅ Rediriger après connexion réussie
    router.push("/");
  } catch (error) {
    errorMessage.value = "Nom d'utilisateur ou mot de passe incorrect.";
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f4f4f4;
}

.auth-box {
  width: 350px;
  padding: 20px;
  background: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  border-radius: 8px;
}

input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

button:hover {
  background-color: #0056b3;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
