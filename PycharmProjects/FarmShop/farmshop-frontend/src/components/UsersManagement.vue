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

    <!-- PAGINATION -->
    <div class="pagination-controls d-flex justify-content-center gap-3 mt-3">
      <button @click="changePage(currentPage - 1)" :disabled="!prevPage" class="btn btn-outline-primary">← Précédent</button>
      <span>Page {{ currentPage }}</span>
      <button @click="changePage(currentPage + 1)" :disabled="!nextPage" class="btn btn-outline-primary">Suivant →</button>
    </div>

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

const API_BASE_URL = "http://127.0.0.1:8000/api";

const users = ref([]);
const showModal = ref(false);
const editingUser = ref(null);
const currentPage = ref(1);
const nextPage = ref(null);
const prevPage = ref(null);

const newUser = ref({
  username: "",
  email: "",
  password: "",
  is_staff: false,
});

const fetchUsers = async (page = 1) => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await axios.get(`${API_BASE_URL}/users/?page=${page}`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    users.value = response.data.results;
    nextPage.value = response.data.next;
    prevPage.value = response.data.previous;
    currentPage.value = page;
  } catch (error) {
    console.error("❌ Erreur lors de la récupération des utilisateurs:", error);
  }
};

const openModal = (user = null) => {
  if (user) {
    editingUser.value = user;
    newUser.value = { ...user, password: "" };
  } else {
    editingUser.value = null;
    newUser.value = { username: "", email: "", password: "", is_staff: false };
  }
  showModal.value = true;
};

const saveUser = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const config = {
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    };

    if (editingUser.value) {
      await axios.put(`${API_BASE_URL}/users/${editingUser.value.id}/`, newUser.value, config);
    } else {
      await axios.post(`${API_BASE_URL}/users/`, newUser.value, config);
    }

    closeModal();
    await fetchUsers(currentPage.value);
  } catch (error) {
    console.error("❌ Erreur lors de l'enregistrement:", error.response?.data || error);
  }
};

const deleteUser = async (userId) => {
  if (!confirm("❌ Supprimer cet utilisateur ?")) return;

  try {
    const token = localStorage.getItem("access_token");
    await axios.delete(`${API_BASE_URL}/users/${userId}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    await fetchUsers(currentPage.value);
  } catch (error) {
    console.error("❌ Erreur lors de la suppression:", error);
  }
};

const closeModal = () => {
  showModal.value = false;
  editingUser.value = null;
};

const changePage = (page) => {
  if (page >= 1) fetchUsers(page);
};

onMounted(() => fetchUsers());
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
