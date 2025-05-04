<template>
  <div class="product-admin">
    <h2 class="mb-4">🛒 Gestion des produits</h2>

    <div class="card shadow rounded p-4 mb-4" v-if="showForm">
      <div class="mb-3">
        <label class="form-label fw-bold">Nom du produit</label>
        <input v-model="form.name" class="form-control" placeholder="Nom du produit" />
      </div>

      <div class="mb-3">
        <label class="form-label fw-bold">Description</label>
        <textarea v-model="form.description" class="form-control" placeholder="Description du produit"></textarea>
      </div>

      <div class="mb-3">
        <label class="form-label fw-bold">Prix (€)</label>
        <input v-model.number="form.price" type="number" min="0" step="0.01" class="form-control" />
      </div>

      <div class="mb-3">
        <label class="form-label fw-bold">Quantité en stock</label>
        <input v-model.number="form.stock" type="number" min="0" class="form-control" />
      </div>

      <div class="mb-3">
        <label class="form-label fw-bold">Unité de mesure</label>
        <select v-model="form.unit_of_measure" class="form-select">
          <option value="kg">Kilogramme</option>
          <option value="piece">Pièce</option>
          <option value="litre">Litre</option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label fw-bold">Catégorie</label>
        <select v-model="form.category_id" class="form-select">
          <option disabled value="">-- Catégorie --</option>
          <option v-for="c in categories" :value="c.id" :key="c.id">{{ c.name }}</option>
        </select>
      </div>

      <div class="form-check mb-3">
        <input type="checkbox" class="form-check-input" v-model="form.is_rentable" id="rentableCheck">
        <label class="form-check-label" for="rentableCheck">Disponible à la location</label>
      </div>

      <div class="mb-3">
        <label class="form-label fw-bold">Image principale</label>
        <input type="file" class="form-control" @change="handleImage" />
      </div>

      <div class="mb-3">
        <label class="form-label fw-bold">Images de la galerie</label>
        <input type="file" class="form-control" multiple @change="handleGallery" />
      </div>

      <div class="d-flex justify-content-end gap-2">
        <button @click="submitForm" class="btn btn-success">
          {{ editMode ? '💾 Mettre à jour' : '✅ Ajouter' }}
        </button>
        <button @click="resetForm" class="btn btn-outline-secondary">❌ Annuler</button>
      </div>
    </div>

    <button @click="showForm = !showForm" class="btn btn-primary mb-3">
      {{ showForm ? 'Fermer le formulaire' : '+ Ajouter un produit' }}
    </button>

    <ul class="list-group">
      <li v-for="p in products" :key="p.id" class="list-group-item d-flex justify-content-between align-items-center">
        <div>
          <strong>{{ p.name }}</strong> – {{ p.price }} €
          <div class="text-muted small">Catégorie : {{ p.category }}</div>
        </div>
        <div class="d-flex gap-2">
          <button @click="editProduct(p)" class="btn btn-sm btn-outline-warning">✏️</button>
          <button @click="deleteProduct(p.id)" class="btn btn-sm btn-outline-danger">🗑</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const products = ref([])
const categories = ref([])
const gallery = ref([])
const showForm = ref(false)
const editMode = ref(false)
const editingId = ref(null)

const form = ref({
  name: '', description: '', price: 0, stock: 0,
  unit_of_measure: 'piece', is_rentable: false,
  category_id: '', image: null
})

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const fetchProducts = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:8000/api/products/", { headers })
    products.value = res.data.results || res.data
  } catch (err) {
    console.error("❌ Erreur chargement produits :", err)
  }
}

const fetchCategories = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:8000/api/products/categories/", { headers })
    categories.value = Array.isArray(res.data.results) ? res.data.results : res.data
  } catch (err) {
    console.error("❌ Erreur chargement catégories :", err)
    categories.value = []
  }
}

const handleImage = (e) => {
  const file = e.target.files[0]
  if (file) form.value.image = file
}

const handleGallery = (e) => {
  gallery.value = Array.from(e.target.files)
}

const submitForm = async () => {
  const formData = new FormData()
  for (const key in form.value) {
    if (form.value[key] !== null) {
      formData.append(key, form.value[key])
    }
  }
  gallery.value.forEach(file => {
    formData.append('gallery', file)
  })

  try {
    if (editMode.value) {
      await axios.put(`http://127.0.0.1:8000/api/products/${editingId.value}/`, formData, {
        headers: { ...headers, 'Content-Type': 'multipart/form-data' }
      })
    } else {
      await axios.post("http://127.0.0.1:8000/api/products/", formData, {
        headers: { ...headers, 'Content-Type': 'multipart/form-data' }
      })
    }
    resetForm()
    fetchProducts()
  } catch (err) {
    console.error("❌ Erreur envoi produit :", err)
    alert("Erreur lors de l'enregistrement.")
  }
}

const editProduct = (p) => {
  form.value = {
    name: p.name,
    description: p.description,
    price: p.price,
    stock: p.stock,
    unit_of_measure: p.unit_of_measure,
    is_rentable: p.is_rentable,
    category_id: p.category_id,
    image: null
  }
  editingId.value = p.id
  showForm.value = true
  editMode.value = true
}

const resetForm = () => {
  form.value = {
    name: '', description: '', price: 0, stock: 0,
    unit_of_measure: 'piece', is_rentable: false,
    category_id: '', image: null
  }
  editingId.value = null
  showForm.value = false
  editMode.value = false
  gallery.value = []
}

const deleteProduct = async (id) => {
  if (!confirm("🗑 Supprimer ce produit ?")) return
  try {
    await axios.delete(`http://127.0.0.1:8000/api/products/${id}/`, { headers })
    fetchProducts()
  } catch (err) {
    console.error("❌ Erreur suppression produit :", err)
  }
}

onMounted(() => {
  fetchProducts()
  fetchCategories()
})
</script>

<style scoped>
.product-admin {
  max-width: 900px;
  margin: auto;
}
</style>
