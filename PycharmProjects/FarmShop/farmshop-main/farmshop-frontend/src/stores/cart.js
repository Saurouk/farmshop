import { ref } from 'vue'
import axios from 'axios'

export const cartCount = ref(0)

export const fetchCartCount = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/cart/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    cartCount.value = res.data.items.length
  } catch (err) {
    console.error('Erreur chargement du panier', err)
  }
}
