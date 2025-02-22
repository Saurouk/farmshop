import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // ✅ Import Vue Router

import './assets/main.css'; // ✅ Style global

const app = createApp(App);

app.use(router); // ✅ Activation de Vue Router
app.mount('#app');
