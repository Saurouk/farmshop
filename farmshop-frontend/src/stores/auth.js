// auth.js
import { reactive, computed } from 'vue';
import axios from 'axios';

const API_BASE_URL = "http://127.0.0.1:8000/api"; // ✅ Assure-toi que cette URL est correcte

const state = reactive({
  username: localStorage.getItem('username') || null,
  isAuthenticated: !!localStorage.getItem('access_token'),
  isAdmin: localStorage.getItem('isAdmin') === 'true'
});

// 🔹  `isAdmin` est bien mis à jour après le chargement de l'état
const updateAdminStatus = () => {
  state.isAdmin = localStorage.getItem('isAdmin') === 'true';
};

// 🔹 Fonction pour récupérer l'utilisateur connecté
const fetchCurrentUser = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/users/me/`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
    });

    const user = response.data;
    console.log("🔄 Utilisateur connecté:", user); // Debug

    state.username = user.username;
    state.isAuthenticated = true;
    state.isAdmin = user.is_staff === true;

    localStorage.setItem("username", user.username);
    localStorage.setItem("isAdmin", state.isAdmin ? "true" : "false");
  } catch (error) {
    console.error("❌ Erreur lors de la récupération de l'utilisateur:", error);
  }
};

// 🔹 Fonction pour mettre à jour l'état de l'utilisateur
const setUser = (user) => {
  console.log("🔄 Utilisateur reçu:", user); // Debug

  state.username = user.username;
  state.isAuthenticated = true;
  state.isAdmin = user.is_staff === true;

  localStorage.setItem("username", user.username);
  localStorage.setItem("isAdmin", state.isAdmin ? "true" : "false");

  updateAdminStatus(); // ✅ Mise à jour immédiate de `isAdmin`
};

// 🔹 Fonction de déconnexion
const logoutUser = () => {
  localStorage.clear();
  state.username = null;
  state.isAuthenticated = false;
  state.isAdmin = false;
};

// 🔹 Vérifier si `isAdmin` est bien récupéré après un refresh
if (state.isAuthenticated) {
  fetchCurrentUser();
}

// 🔹 Propriétés calculées
const isLoggedIn = computed(() => state.isAuthenticated);
const isAdmin = computed(() => state.isAdmin);

export default {
  state,
  fetchCurrentUser,
  setUser,
  logoutUser,
  isLoggedIn,
  isAdmin,
  updateAdminStatus
};
