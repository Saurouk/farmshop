<template>
  <div class="product-admin">
    <h2 class="mb-4">Gestion des produits</h2>

    <!-- Formulaire -->
    <div class="card card-body mb-4" v-if="showForm">
      <input v-model="form.name" class="form-control mb-2" placeholder="Nom du produit" />
      <textarea v-model="form.description" class="form-control mb-2" placeholder="Description"></textarea>
      <input v-model.number="form.price" type="number" class="form-control mb-2" placeholder="Prix" />
      <input v-model.number="form.stock" type="number" class="form-control mb-2" placeholder="Stock" />
      <select v-model="form.unit_of_measure" class="form-select mb-2">
        <option value="kg">Kilogramme</option>
        <option value="piece">Pièce</option>
        <option value="litre">Litre</option>
      </select>
      <select v-model="form.category_id" class="form-select mb-2">
        <option disabled value="">-- Catégorie --</option>
        <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
      </select>
      <div class="form-check mb-2">
        <input type="checkbox" class="form-check-input" v-model="form.is_rentable" id="rentableCheck">
        <label for="rentableCheck" class="form-check-label">Disponible à la location</label>
      </div>
      <input type="file" class="form-control mb-2" @change="handleImage" />

      <div class="d-flex justify-content-end gap-2">
        <button @click="submitForm" class="btn btn-success">{{ editMode ? 'Mettre à jour' : 'Ajouter' }}</button>
        <button @click="resetForm" class="btn btn-outline-secondary">Annuler</button>
      </div>
    </div>

    <button @click="toggleForm" class="btn btn-primary mb-3">
      {{ showForm ? 'Fermer le formulaire' : '+ Ajouter un produit' }}
    </button>

    <!-- Liste -->
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
const showForm = ref(false)
const editMode = ref(false)
const editingId = ref(null)

const form = ref({
  name: '',
  description: '',
  price: 0,
  stock: 0,
  unit_of_measure: 'piece',
  is_rentable: false,
  category_id: '',
  image: null
})

const token = localStorage.getItem('access_token')
const headers = { Authorization: `Bearer ${token}` }

const fetchProducts = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:8000/api/products/", { headers })
    products.value = res.data.results || res.data
  } catch (err) {
    console.error("Erreur chargement produits:", err)
  }
}

const fetchCategories = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:8000/api/products/categories/", { headers })
    categories.value = res.data
  } catch (err) {
    console.error("Erreur chargement catégories:", err)
  }
}

const handleImage = (e) => {
  const file = e.target.files[0]
  if (file) form.value.image = file
}

const submitForm = async () => {
  const formData = new FormData()
  for (const key in form.value) {
    if (form.value[key] !== null && form.value[key] !== '') {
      formData.append(key, form.value[key])
    }
  }

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
    category_id: p.category_id || '',
    image: null
  }
  editingId.value = p.id
  editMode.value = true
  showForm.value = true
}

const resetForm = () => {
  form.value = {
    name: '',
    description: '',
    price: 0,
    stock: 0,
    unit_of_measure: 'piece',
    is_rentable: false,
    category_id: '',
    image: null
  }
  editingId.value = null
  editMode.value = false
  showForm.value = false
}

const deleteProduct = async (id) => {
  if (!confirm("🗑 Supprimer ce produit ?")) return
  try {
    await axios.delete(`http://127.0.0.1:8000/api/products/${id}/`, { headers })
    fetchProducts()
  } catch (err) {
    console.error("Erreur suppression produit :", err)
    alert("Impossible de supprimer ce produit.")
  }
}

const toggleForm = () => {
  showForm.value = !showForm.value
  if (!showForm.value) resetForm()
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
