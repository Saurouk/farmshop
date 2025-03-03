<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-success shadow-sm">
    <div class="container">
      <router-link class="navbar-brand text-white fw-bold" to="/">
        🌾 FarmShop
      </router-link>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link text-white" active-class="fw-bold" to="/">Accueil</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link text-white" active-class="fw-bold" to="/products">Produits</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link text-white" active-class="fw-bold" to="/blog">Blog</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link text-white" active-class="fw-bold" to="/contact">Contact</router-link>
          </li>
        </ul>

        <div v-if="auth.state.isAuthenticated" class="user-menu">
          <span class="text-white fw-bold">👤 {{ auth.state.username }}</span>
          <button @click="logout" class="btn btn-danger ms-3 fw-bold">Déconnexion</button>
        </div>
        <router-link v-else class="btn btn-warning text-dark ms-3 fw-bold" to="/login">Connexion</router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import auth from "@/stores/auth";
import { useRouter } from "vue-router";

const router = useRouter();

const logout = () => {
  auth.logoutUser();
  router.push("/");
};
</script>
