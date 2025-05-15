<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2>📝 Inscription</h2>
      <p>Créez votre compte FarmShop.</p>

      <form @submit.prevent="register">
        <input v-model="username" type="text" placeholder="Nom d'utilisateur" required />
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Mot de passe" required />
        <input v-model="confirmPassword" type="password" placeholder="Confirmer le mot de passe" required />
        <button type="submit">S'inscrire</button>
      </form>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success">{{ successMessage }}</p>

      <p>Déjà inscrit ? <router-link to="/login">Connectez-vous</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const errorMessage = ref("");
const successMessage = ref("");
const router = useRouter();

const register = async () => {
  errorMessage.value = "";
  successMessage.value = "";

  if (password.value !== confirmPassword.value) {
    errorMessage.value = "Les mots de passe ne correspondent pas.";
    return;
  }

  try {
    const response = await axios.post("http://127.0.0.1:8000/api/users/register/", {
      username: username.value,
      email: email.value,
      password: password.value,
    });

    successMessage.value = response.data.message || "Inscription réussie. Veuillez vérifier votre e-mail pour activer votre compte.";
    setTimeout(() => {
      router.push("/login");
    }, 2500);
  } catch (error) {
    if (error.response && error.response.data) {
      const errors = error.response.data;
      const details = Object.entries(errors)
        .map(([field, msgs]) => `${field}: ${msgs.join(', ')}`)
        .join('\n');
      errorMessage.value = `Erreur(s) :\n${details}`;
    } else {
      errorMessage.value = "Erreur lors de l'inscription. Veuillez réessayer.";
    }
    console.error("❌ Erreur inscription :", error);
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
  background-color: #28a745;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

button:hover {
  background-color: #218838;
}

.error {
  color: red;
  margin-top: 10px;
  white-space: pre-line;
}

.success {
  color: green;
  margin-top: 10px;
}
</style>
