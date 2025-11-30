<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-header bg-success text-white">
            <h3 class="mb-0">Register</h3>
          </div>
          <div class="card-body">
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <div v-if="success" class="alert alert-success">{{ success }}</div>
            <form @submit.prevent="registerUser">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="username" class="form-label">Username</label>
                  <input type="text" class="form-control" id="username" v-model="form.username" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label for="email" class="form-label">Email</label>
                  <input type="email" class="form-control" id="email" v-model="form.email" required>
                </div>
              </div>
              <div class="mb-3">
                <label for="name" class="form-label">Full Name</label>
                <input type="text" class="form-control" id="name" v-model="form.name" required>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input type="password" class="form-control" id="password" v-model="form.password" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label for="phone" class="form-label">Phone</label>
                  <input type="tel" class="form-control" id="phone" v-model="form.phone" required>
                </div>
              </div>
              <!-- Role selection removed: Default to Patient -->
              <button type="submit" class="btn btn-success w-100" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Register
              </button>
            </form>
          </div>
          <div class="card-footer text-center">
            <small>Already have an account? <router-link to="/login">Login here</router-link></small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import api from '../utils/api';

// -- Form Data --
const form = reactive({
  username: '',
  email: '',
  name: '',
  password: '',
  phone: '',
  role: 'patient' // Default role for public registration
});

// -- UI State --
const error = ref('');
const success = ref('');
const loading = ref(false);

// -- Methods --

// Handle user registration submission
const registerUser = async () => {
  // Reset UI state
  error.value = '';
  success.value = '';
  loading.value = true;

  try {
    // 1. Send registration request to backend
    const response = await api.post('/auth/register', form);
    
    // 2. Show success message
    success.value = response.data.message || 'Registration successful! Please login.';
    
    // 3. Clear form fields
    Object.keys(form).forEach(key => {
        if (key === 'role') form[key] = 'patient';
        else form[key] = '';
    });
  } catch (err) {
    // Handle registration errors
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
