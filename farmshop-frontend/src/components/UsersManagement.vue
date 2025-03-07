<template>
  <div class="users-management">
    <h2>Gestion des Utilisateurs</h2>

    <!-- Message de chargement -->
    <div v-if="loading">Chargement des utilisateurs...</div>

    <!-- Message d'erreur -->
    <div v-if="error" class="error">{{ error }}</div>

    <!-- Tableau des utilisateurs -->
    <table v-if="users.length > 0">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nom d'utilisateur</th>
          <th>Email</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>
            <button @click="deleteUser(user.id)">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else-if="!loading && users.length === 0">Aucun utilisateur trouvé.</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      users: [],
      loading: false,
      error: null,
    };
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get("http://localhost:8000/api/users/", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        this.users = response.data;
      } catch (err) {
        this.error = "Erreur lors du chargement des utilisateurs.";
      } finally {
        this.loading = false;
      }
    },
    async deleteUser(userId) {
      if (!confirm("Voulez-vous vraiment supprimer cet utilisateur ?")) return;
      try {
        await axios.delete(`http://localhost:8000/api/users/${userId}/`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        this.users = this.users.filter(user => user.id !== userId);
      } catch (err) {
        this.error = "Impossible de supprimer l'utilisateur.";
      }
    },
  },
};
</script>

<style scoped>
.users-management {
  padding: 20px;
  max-width: 800px;
  margin: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
th {
  background-color: #f4f4f4;
}
button {
  background-color: red;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}
button:hover {
  background-color: darkred;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
