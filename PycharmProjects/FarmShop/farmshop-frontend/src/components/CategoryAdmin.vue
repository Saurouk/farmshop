<template>
  <div class="category-admin">
    <h2 class="text-center mb-4">📁 Gestion des catégories</h2>

    <div class="card shadow-sm p-4 mb-4" v-if="showForm">
      <div class="mb-3">
        <label class="form-label fw-bold">Nom de la catégorie</label>
        <input v-model="form.name" class="form-control" placeholder="Ex : Engrais, Outillages..." />
      </div>

      <div class="d-flex justify-content-end gap-2">
        <button @click="submitForm" class="btn btn-success">
          {{ editMode ? '💾 Mettre à jour' : '➕ Ajouter' }}
        </button>
        <button @click="resetForm" class="btn btn-outline-secondary">❌ Annuler</button>
      </div>
    </div>

    <button @click="showForm = !showForm" class="btn btn-primary mb-3">
      {{ showForm ? '➖ Fermer le formulaire' : '+ Nouvelle catégorie' }}
    </button>

    <div class="card shadow-sm p-3">
      <h4 class="mb-3">📂 Liste des catégories</h4>
      <ul class="list-group">
        <li v-for="cat in categories" :key="cat.id" class="list-group-item d-flex justify-content-between align-items-center">
          <div>
            <strong>{{ cat.name }}</strong>
          </div>
          <div class="d-flex gap-2">
            <button @click="editCategory(cat)" class="btn btn-sm btn-outline-warning">✏️</button>
            <button @click="deleteCategory(cat.id)" class="btn btn-sm btn-outline-danger">🗑</button>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const categories = ref([])
const showForm = ref(false)
const editMode = ref(false)
const form = ref({ name: '' })
const editingId = ref(null)

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const fetchCategories = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:8000/api/products/categories/", { headers })
    categories.value = res.data.results || res.data
  } catch (err) {
    console.error("❌ Erreur chargement catégories :", err)
  }
}

const submitForm = async () => {
  try {
    if (editMode.value) {
      await axios.put(`http://127.0.0.1:8000/api/products/categories/${editingId.value}/`, form.value, { headers })
    } else {
      await axios.post("http://127.0.0.1:8000/api/products/categories/", form.value, { headers })
    }
    resetForm()
    fetchCategories()
  } catch (err) {
    console.error("❌ Erreur enregistrement catégorie :", err)
    alert("Erreur lors de l'enregistrement.")
  }
}

const editCategory = (c) => {
  form.value = { name: c.name }
  editingId.value = c.id
  showForm.value = true
  editMode.value = true
}

const resetForm = () => {
  form.value = { name: '' }
  editingId.value = null
  showForm.value = false
  editMode.value = false
}

const deleteCategory = async (id) => {
  if (!confirm("🗑 Supprimer cette catégorie ?")) return
  try {
    await axios.delete(`http://127.0.0.1:8000/api/products/categories/${id}/`, { headers })
    fetchCategories()
  } catch (err) {
    console.error("❌ Erreur suppression catégorie :", err)
  }
}

onMounted(fetchCategories)
</script>

<style scoped>
.category-admin {
  max-width: 700px;
  margin: auto;
}
.card {
  border-radius: 10px;
  background-color: #f8f9fa;
}
.list-group-item {
  font-size: 1rem;
}
</style>
