<template>
  <div class="login-container d-flex align-items-center justify-content-center">
    <div class="card login-card shadow-lg border-0 rounded-4 overflow-hidden">
      <div class="row g-0 h-100">
        <!-- Left Side: Image/Brand -->
        <div class="col-md-5 d-none d-md-flex align-items-center justify-content-center bg-primary text-white p-5">
          <div class="text-center">
            <i class="bi bi-heart-pulse-fill display-1 mb-3"></i>
            <h2 class="fw-bold">LifeSync</h2>
            <p class="lead">Your Health, Our Priority.</p>
          </div>
        </div>
        
        <!-- Right Side: Form -->
        <div class="col-md-7 p-5 bg-white">
          <div class="text-center mb-4">
            <h3 class="fw-bold text-primary">Welcome Back</h3>
            <p class="text-muted">Please login to your account</p>
          </div>

          <div v-if="error" class="alert alert-danger rounded-3">{{ error }}</div>
          
          <form @submit.prevent="loginUser">
            <div class="mb-4">
              <label for="username" class="form-label fw-semibold text-secondary">Username or Email</label>
              <div class="input-group">
                <span class="input-group-text bg-light border-end-0"><i class="bi bi-person text-muted"></i></span>
                <input type="text" class="form-control bg-light border-start-0 ps-0" id="username" v-model="username" placeholder="Enter your username" required>
              </div>
            </div>
            
            <div class="mb-4">
              <label for="password" class="form-label fw-semibold text-secondary">Password</label>
              <div class="input-group">
                <span class="input-group-text bg-light border-end-0"><i class="bi bi-lock text-muted"></i></span>
                <input type="password" class="form-control bg-light border-start-0 ps-0" id="password" v-model="password" placeholder="Enter your password" required>
              </div>
            </div>
            
            <button type="submit" class="btn btn-primary w-100 py-2 rounded-pill fw-bold shadow-sm" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Login
            </button>
          </form>
          
          <div class="text-center mt-4">
            <p class="small text-muted">Don't have an account? <router-link to="/register" class="text-primary fw-bold text-decoration-none">Register here</router-link></p>
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

<style scoped>
.login-container {
  min-height: 80vh;
  background-color: #f8f9fa;
  padding-top: 80px;
  padding-bottom: 40px;
}
.login-card {
  max-width: 900px;
  width: 100%;
  min-height: 500px;
}
.form-control:focus {
  box-shadow: none;
  border-color: #ced4da;
}
.input-group-text {
  border-color: #ced4da;
}
</style>
