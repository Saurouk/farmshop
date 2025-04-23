import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  faHome,
  faBox,
  faBook,
  faEnvelope,
  faUser,
  faGear,
  faReceipt,
  faTruck
} from '@fortawesome/free-solid-svg-icons'

library.add(faHome, faBox, faBook, faEnvelope, faUser, faGear, faReceipt, faTruck)

const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(router)
app.use(Toast)
app.mount('#app')
