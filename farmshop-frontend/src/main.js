import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // ✅ Import du router
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';


const app = createApp(App);

app.use(router); // ✅ Activation de Vue Router
app.use(router);
app.mount('#app');
