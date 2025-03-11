<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import AddUser from '../components/AddUser.vue'     
const users = ref([])
const loading = ref(false)
const error = ref(null)

const fetchUsers = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await axios.get('http://127.0.0.1:2002/')
    users.value = response.data

  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to fetch users'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<template>
  <div class="users-container">
    <h1>Users List</h1>
    
    <div v-if="loading" class="loading">
      Loading users...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else class="users-list">
      <div v-if="users.length === 0" class="no-users">
        No users found
      </div>
      <div v-else>
        
        <div v-for="user in users" :key="user.id" class="user-card">
          <h3>{{ user.username }}</h3>
          <p>{{ user.email }}</p>
          <p>{{ user.phone }}</p>
          <p>{{ user.address }}</p>
          
        </div>
        <AddUser />
      </div>
    </div>
  </div>
</template>

<style scoped>
.users-container {
  padding: 2rem;
  width: 100%;  
  margin: 0 auto;
}

h1 {
  color: #333;
  text-align: center;
  margin-bottom: 2rem;
}

.loading, .error, .no-users {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #dc3545;
}

.users-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.user-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-card h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.user-card p {
  margin: 0;
  color: #666;
}
</style>

