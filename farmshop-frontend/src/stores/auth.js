import { reactive, computed } from "vue";
import auth from "@/stores/auth";  // ✅ Chemin mis à jour


// ✅ Initialiser l'état à partir du localStorage
const state = reactive({
  username: localStorage.getItem("username") || null,  // ✅ Charge l'utilisateur stocké
  isAuthenticated: !!localStorage.getItem("access_token"),
});

// ✅ Met à jour l'utilisateur après connexion
const setUser = (user) => {
  state.username = user.username;
  state.isAuthenticated = true;
  localStorage.setItem("username", user.username);  // ✅ Stocke le nom de l'utilisateur
};

// ✅ Déconnexion
const logoutUser = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("username");  // ✅ Supprime le username stocké
  state.username = null;
  state.isAuthenticated = false;
};

// ✅ Récupérer l'état d'authentification sous forme de computed property
const isLoggedIn = computed(() => state.isAuthenticated);

export default {
  state,
  setUser,
  logoutUser,
  isLoggedIn,  // ✅ Ajout pour pouvoir l'utiliser facilement dans la navbar
};
