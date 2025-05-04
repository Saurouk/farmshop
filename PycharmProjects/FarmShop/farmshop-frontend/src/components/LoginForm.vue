<template>
  <div>
    <h2>Se connecter</h2>
    <form @submit.prevent="login">
      <input v-model="username" type="text" placeholder="Nom d'utilisateur" required />
      <input v-model="password" type="password" placeholder="Mot de passe" required />
      <button type="submit">Connexion</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const errorMessage = ref('');
const router = useRouter();

const login = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/auth/login/', {
      username: username.value,
      password: password.value
    });

    // Stocker les tokens JWT
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);

    // Rediriger après connexion réussie
    router.push('/products');
  } catch (error) {
    errorMessage.value = "Nom d'utilisateur ou mot de passe incorrect.";
  }
};
</script>

<style>
.error {
  color: red;
}
</style>
