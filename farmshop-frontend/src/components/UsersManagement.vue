<template>
  <div class="users-management">
    <h2>👥 Gestion des Utilisateurs</h2>
    <button @click="openModal()" class="btn btn-success">➕ Ajouter un utilisateur</button>

    <table class="table table-striped mt-4">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nom d'utilisateur</th>
          <th>Email</th>
          <th>Admin</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.is_staff ? "✅" : "❌" }}</td>
          <td>
            <button @click="openModal(user)" class="btn btn-warning btn-sm">✏️ Modifier</button>
            <button @click="deleteUser(user.id)" class="btn btn-danger btn-sm">🗑 Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- MODAL AJOUT / MODIFICATION UTILISATEUR -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h3>{{ editingUser ? "Modifier" : "Ajouter" }} un utilisateur</h3>
        <input type="text" v-model="newUser.username" placeholder="Nom d'utilisateur" required />
        <input type="email" v-model="newUser.email" placeholder="Email" required />
        <input type="password" v-model="newUser.password" placeholder="Mot de passe (laisser vide si inchangé)" />
        <label>
          <input type="checkbox" v-model="newUser.is_staff" />
          Administrateur
        </label>
        <button @click="saveUser" class="btn btn-primary">💾 Enregistrer</button>
        <button @click="closeModal" class="btn btn-secondary">❌ Annuler</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const users = ref([]);
const showModal = ref(false);
const editingUser = ref(null);

const newUser = ref({
  username: "",
  email: "",
  password: "",
  is_staff: false,
});

// 🔄 Récupérer les utilisateurs depuis l'API Django
const fetchUsers = async () => {
  try {
    const token = localStorage.getItem("access_token"); // ✅ Récupère le token JWT
    if (!token) {
      console.error("❌ Aucun token trouvé. L'utilisateur doit être authentifié.");
      return;
    }

    const response = await axios.get("http://127.0.0.1:8000/api/users/", {
      headers: { Authorization: `Bearer ${token}` } // ✅ Ajoute le token JWT
    });

    users.value = response.data;
    console.log("✅ Liste des utilisateurs récupérée :", users.value);
  } catch (error) {
    console.error("❌ Erreur lors de la récupération des utilisateurs:", error);
  }
};


// 🔹 Ouvrir le modal pour Ajouter / Modifier un utilisateur
const openModal = (user = null) => {
  if (user) {
    editingUser.value = user;
    newUser.value = { ...user, password: "" }; // Ne pas pré-remplir le mot de passe
  } else {
    editingUser.value = null;
    newUser.value = { username: "", email: "", password: "", is_staff: false };
  }
  showModal.value = true;
};

// 🔹 Sauvegarder (ajouter ou modifier) un utilisateur
const saveUser = async () => {
  try {
    if (editingUser.value) {
      await axios.put(`http://127.0.0.1:8000/api/users/${editingUser.value.id}/`, newUser.value);
    } else {
      await axios.post("http://127.0.0.1:8000/api/users/", newUser.value);
    }
    closeModal();
    fetchUsers(); // Actualiser la liste des utilisateurs
  } catch (error) {
    console.error("Erreur lors de l'enregistrement:", error);
  }
};

// 🔹 Supprimer un utilisateur
const deleteUser = async (userId) => {
  if (!confirm("Supprimer cet utilisateur ?")) return;
  try {
    await axios.delete(`http://127.0.0.1:8000/api/users/${userId}/`);
    fetchUsers(); // Actualiser la liste
  } catch (error) {
    console.error("Erreur lors de la suppression:", error);
  }
};

// 🔄 Fermer le modal
const closeModal = () => {
  showModal.value = false;
  editingUser.value = null;
};

onMounted(fetchUsers);
</script>

<style scoped>
.table {
  width: 100%;
  margin-top: 20px;
}
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
}
</style>
