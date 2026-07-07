<template>
  <div class="register-container d-flex align-items-center justify-content-center">
    <div class="card register-card shadow-lg border-0 rounded-4 overflow-hidden">
      <div class="row g-0 h-100">
        
        <div class="col-md-4 d-none d-md-flex align-items-center justify-content-center bg-success text-white p-5">
          <div class="text-center">
            <i class="bi bi-person-plus-fill display-1 mb-3"></i>
            <h2 class="fw-bold">Join Us</h2>
            <p class="lead">Start your health journey today.</p>
          </div>
        </div>

        
        <div class="col-md-8 p-5 bg-white">
          <div class="text-center mb-4">
            <h3 class="fw-bold text-success">Create Account</h3>
            <p class="text-muted">Fill in your details to register</p>
          </div>

          <div v-if="error" class="alert alert-danger rounded-3">{{ error }}</div>
          <div v-if="success" class="alert alert-success rounded-3">{{ success }}</div>

          <form @submit.prevent="registerUser">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="username" class="form-label fw-semibold text-secondary">Username</label>
                <input type="text" class="form-control bg-light" id="username" v-model="form.username" placeholder="Choose a username" required>
              </div>
              <div class="col-md-6 mb-3">
                <label for="email" class="form-label fw-semibold text-secondary">Email</label>
                <input type="email" class="form-control bg-light" id="email" v-model="form.email" placeholder="name@example.com" required>
              </div>
            </div>

            <div class="mb-3">
              <label for="name" class="form-label fw-semibold text-secondary">Full Name</label>
              <input type="text" class="form-control bg-light" id="name" v-model="form.name" placeholder="John Doe" required>
            </div>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="password" class="form-label fw-semibold text-secondary">Password</label>
                <input type="password" class="form-control bg-light" id="password" v-model="form.password" placeholder="Create a password" required>
              </div>
              <div class="col-md-6 mb-3">
                <label for="phone" class="form-label fw-semibold text-secondary">Phone</label>
                <input type="tel" class="form-control bg-light" id="phone" v-model="form.phone" placeholder="1234567890" required>
              </div>
            </div>

            <button type="submit" class="btn btn-success w-100 py-2 rounded-pill fw-bold shadow-sm mt-3" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Register
            </button>
          </form>

          <div class="text-center mt-4">
            <p class="small text-muted">Already have an account? <router-link to="/login" class="text-success fw-bold text-decoration-none">Login here</router-link></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import api from '../utils/api';

const form = reactive({
  username: '',
  email: '',
  name: '',
  password: '',
  phone: '',
  role: 'patient' 
});

const error = ref('');
const success = ref('');
const loading = ref(false);

const registerUser = async () => {
  
  error.value = '';
  success.value = '';
  loading.value = true;

  try {
    
    const response = await api.post('/auth/register', form);
    
    
    success.value = response.data.message || 'Registration successful! Please login.';
    
    
    Object.keys(form).forEach(key => {
        if (key === 'role') form[key] = 'patient';
        else form[key] = '';
    });
  } catch (err) {
    
    if (err.response && err.response.data && err.response.data.message) {
      error.value = err.response.data.message;
    } else {
      error.value = 'An error occurred during registration. Please try again.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-container {
  min-height: 80vh;
  background-color: #f8f9fa;
  padding-top: 80px;
  padding-bottom: 40px;
}
.register-card {
  max-width: 1000px;
  width: 100%;
  min-height: 600px;
}
.form-control:focus {
  box-shadow: none;
  border-color: #198754; 
}
</style>
