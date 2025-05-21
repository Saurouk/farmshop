<template>
  <section class="newsletter-cta text-white text-center py-5">
    <div class="overlay"></div>
    <div class="container position-relative z-1">
      <h2 class="mb-3">📬 Restez informé</h2>
      <p class="mb-4">
        Inscrivez-vous à notre newsletter pour recevoir nos dernières actualités, promotions et conseils agricoles.
      </p>
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="input-group">
            <input
              v-model="email"
              type="email"
              class="form-control"
              placeholder="Entrez votre adresse email"
            />
            <button @click="subscribe" class="btn btn-warning">
              S'inscrire
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const email = ref('')

const subscribe = async () => {
  if (!email.value) {
    alert('Veuillez entrer une adresse email.')
    return
  }

  try {
    await axios.post('http://127.0.0.1:8000/api/newsletter/subscribe/', {
      email: email.value,
    })
    alert('✅ Inscription réussie !')
    email.value = ''
  } catch (err) {
    console.error('❌ Erreur inscription newsletter :', err)
    alert(err.response?.data?.error || 'Une erreur est survenue.')
  }
}
</script>

<style scoped>
.newsletter-cta {
  background-image: url('/newslettercta.jpg');
  background-size: cover;
  background-position: center;
  position: relative;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 0;
}

.container {
  z-index: 1;
}

input {
  border-radius: 0.375rem 0 0 0.375rem;
}
button {
  border-radius: 0 0.375rem 0.375rem 0;
}
</style>
