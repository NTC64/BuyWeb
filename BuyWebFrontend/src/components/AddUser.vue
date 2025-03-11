<script setup>
import { ref } from 'vue'
import axios from 'axios'

const user = ref({
  username: '',
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  phone: '',
  address: '',
})

const handleSubmit = async () => {
  console.log(user.value)
  try {
    const response = await axios.post('http://127.0.0.1:2002/users', user.value)
    console.log(response.data)
    // Reload the page after successful user creation
    window.location.reload()
  } catch (error) {
    console.error('Error creating user:', error)
  }
}
</script>

<template>
  <div class="add-user-container">
    <h2>Add User</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="user.username" required>
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="user.email" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="user.password" required>
      </div>
      <div class="form-group">
        <label for="first_name">First Name:</label>
        <input type="text" id="first_name" v-model="user.first_name" required>
      </div>
      <div class="form-group">
        <label for="last_name">Last Name:</label>
        <input type="text" id="last_name" v-model="user.last_name" required>
      </div>
      <div class="form-group">
        <label for="phone">Phone:</label>
        <input type="text" id="phone" v-model="user.phone" required>  
      </div>
      <div class="form-group">
        <label for="address">Address:</label>
        <input type="text" id="address" v-model="user.address" required>
      </div>
      <button type="submit" >Add User</button> 
    </form>
  </div>
</template>

<style scoped>
.add-user-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc; 
  border-radius: 5px;
  background-color: #f9f9f9;
}

.form-group {
  
  margin-bottom: 15px;  
}

label {
  display: block;
  margin-bottom: 5px;
} 

input[type="text"], input[type="email"], input[type="password"] {
  width: 100%;
  padding: 10px;
  
  border: 1px solid #ccc;
  border-radius: 3px;
} 

button {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  border: none; 
  border-radius: 3px;
  color: white;
  cursor: pointer;
}

button:hover {  
  background-color: #45a049;
}
</style>  
