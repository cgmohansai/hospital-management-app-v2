<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-header bg-primary text-white">
            <h3 class="mb-0">Login</h3>
          </div>
          <div class="card-body">
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <form @submit.prevent="loginUser">
              <div class="mb-3">
                <label for="username" class="form-label">Username or Email</label>
                <input type="text" class="form-control" id="username" v-model="username" required>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" v-model="password" required>
              </div>
              <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Login
              </button>
            </form>
          </div>
          <div class="card-footer text-center">
            <small>Don't have an account? <router-link to="/register">Register here</router-link></small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../utils/api';

const router = useRouter();

// -- Form State --
const username = ref('');
const password = ref('');

// -- UI State --
const error = ref('');
const loading = ref(false);

// -- Methods --

// Handle user login submission
const loginUser = async () => {
  // Reset UI state
  error.value = '';
  loading.value = true;

  try {
    // 1. Send login request to backend
    const response = await api.post('/auth/login', {
      username: username.value,
      password: password.value
    });

    // 2. Store authentication token and user details
    localStorage.setItem('token', response.data.token);
    localStorage.setItem('user', JSON.stringify({
        id: response.data.id,
        username: response.data.username,
        email: response.data.email,
        name: response.data.name,
        roles: response.data.roles
    }));

    // 3. Redirect to dashboard
    // Using window.location.href to ensure a full reload, updating Navbar state
    window.location.href = '/dashboard'; 

  } catch (err) {
    // Handle login errors
    if (err.response && err.response.data && err.response.data.message) {
      error.value = err.response.data.message;
    } else {
      error.value = 'An error occurred during login. Please check your credentials.';
    }
  } finally {
    loading.value = false;
  }
};
</script>
