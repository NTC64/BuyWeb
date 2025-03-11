import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router/index.js'
import axios from 'axios'

createApp(App).use(router).mount('#app')

axios.defaults.baseURL = 'http://127.0.0.1:2002'
