// auth.js
import { reactive, computed } from 'vue'
import axios from 'axios'

const API_BASE_URL = '/api'

const state = reactive({
  username: localStorage.getItem('username') || null,
  isAuthenticated: !!localStorage.getItem('access_token'),
  isAdmin: localStorage.getItem('isAdmin') === 'true',
  profilePicture: null
})

const updateAdminStatus = () => {
  state.isAdmin = localStorage.getItem('isAdmin') === 'true'
}

const fetchCurrentUser = async () => {
  try {
    const res = await axios.get(`${API_BASE_URL}/users/me/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })

    const user = res.data
    state.username = user.username
    state.profilePicture = user.profile_picture
    state.isAuthenticated = true
    state.isAdmin = user.is_staff === true

    localStorage.setItem('username', user.username)
    localStorage.setItem('isAdmin', state.isAdmin ? 'true' : 'false')
  } catch (err) {
    console.error("❌ Erreur lors de la récupération de l'utilisateur :", err)
  }
}

const setUser = (user) => {
  state.username = user.username
  state.profilePicture = user.profile_picture
  state.isAuthenticated = true
  state.isAdmin = user.is_staff === true

  localStorage.setItem('username', user.username)
  localStorage.setItem('isAdmin', state.isAdmin ? 'true' : 'false')

  updateAdminStatus()
}

const logoutUser = () => {
  localStorage.clear()
  state.username = null
  state.profilePicture = null
  state.isAuthenticated = false
  state.isAdmin = false
}

if (state.isAuthenticated) {
  fetchCurrentUser()
}

const isLoggedIn = computed(() => state.isAuthenticated)
const isAdmin = computed(() => state.isAdmin)

export default {
  state,
  fetchCurrentUser,
  setUser,
  logoutUser,
  isLoggedIn,
  isAdmin,
  updateAdminStatus
}
