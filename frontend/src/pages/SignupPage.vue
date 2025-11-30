<template>
  <div class="signup-page vh-100 d-flex align-items-center justify-content-center position-relative py-5">
    <!-- Floating Header -->
    <FloatingHeader />
    
    <!-- Theme and Language Toggles -->
    <ThemeToggle />
    <LanguageToggle />
    
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-7">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5">
              <div class="text-center mb-4">
                <div class="mb-3">
                  <MedicalIcons type="hospital" :color="'#3b82f6'" :strokeColor="'#8b5cf6'" style="width: 60px; height: 60px;" />
                </div>
                <h1 class="h2 fw-bold mb-2">{{ t('createAccount') }}</h1>
                <p class="text-muted">{{ t('tagline') }}</p>
              </div>

              <form @submit.prevent="handleRegister">
                <div class="row g-3 mb-3">
                  <div class="col-md-6">
                    <label for="name" class="form-label fw-semibold">
                      <MedicalIcons type="doctor" :color="'#3b82f6'" :strokeColor="'#8b5cf6'" class="me-2" style="width: 18px; height: 18px;" />
                      {{ t('name') }}
                    </label>
                    <input
                      id="name"
                      v-model="form.name"
                      type="text"
                      class="form-control form-control-lg"
                      :class="{ 'is-invalid': errors.name }"
                      :placeholder="t('name')"
                      required
                    />
                    <div v-if="errors.name" class="invalid-feedback">{{ errors.name }}</div>
                  </div>

                  <div class="col-md-6">
                    <label for="username" class="form-label fw-semibold">
                      <MedicalIcons type="stethoscope" :color="'#3b82f6'" :strokeColor="'#8b5cf6'" class="me-2" style="width: 18px; height: 18px;" />
                      {{ t('username') }}
                    </label>
                    <input
                      id="username"
                      v-model="form.username"
                      type="text"
                      class="form-control form-control-lg"
                      :class="{ 'is-invalid': errors.username }"
                      :placeholder="t('username')"
                      required
                    />
                    <div v-if="errors.username" class="invalid-feedback">{{ errors.username }}</div>
                  </div>
                </div>

                <div class="mb-3">
                  <label for="email" class="form-label fw-semibold">
                    <MedicalIcons type="heart" :color="'#3b82f6'" :strokeColor="'#8b5cf6'" class="me-2" style="width: 18px; height: 18px;" />
                    {{ t('email') }}
                  </label>
                  <input
                    id="email"
                    v-model="form.email"
                    type="email"
                    class="form-control form-control-lg"
                    :class="{ 'is-invalid': errors.email }"
                    :placeholder="t('email')"
                    required
                  />
                  <div v-if="errors.email" class="invalid-feedback">{{ errors.email }}</div>
                </div>

                <div class="mb-3">
                  <label for="phone" class="form-label fw-semibold">
                    <MedicalIcons type="nurse" :color="'#3b82f6'" :strokeColor="'#8b5cf6'" class="me-2" style="width: 18px; height: 18px;" />
                    {{ t('phone') }}
                  </label>
                  <input
                    id="phone"
                    v-model="form.phone"
                    type="tel"
                    class="form-control form-control-lg"
                    :class="{ 'is-invalid': errors.phone }"
                    :placeholder="t('phone')"
                    required
                  />
                  <div v-if="errors.phone" class="invalid-feedback">{{ errors.phone }}</div>
                </div>

                <div class="mb-3">
                  <label for="role" class="form-label fw-semibold">
                    <MedicalIcons type="doctor" :color="'#3b82f6'" :strokeColor="'#8b5cf6'" class="me-2" style="width: 18px; height: 18px;" />
                    {{ t('role') }}
                  </label>
                  <select
                    id="role"
                    v-model="form.role"
                    class="form-select form-select-lg"
                    :class="{ 'is-invalid': errors.role }"
                    required
                  >
                    <option value="patient">{{ t('rolePatient') }}</option>
                    <option value="doctor">{{ t('roleDoctor') }}</option>
                  </select>
                  <div v-if="errors.role" class="invalid-feedback">{{ errors.role }}</div>
                  <small class="form-text text-muted" v-if="form.role === 'doctor'">
                    {{ t('doctorApprovalNote') }}
                  </small>
                </div>

                <div class="row g-3 mb-4">
                  <div class="col-md-6">
                    <label for="password" class="form-label fw-semibold">{{ t('password') }}</label>
                    <div class="input-group">
                      <input
                        id="password"
                        v-model="form.password"
                        :type="showPassword ? 'text' : 'password'"
                        class="form-control form-control-lg"
                        :class="{ 'is-invalid': errors.password }"
                        :placeholder="t('password')"
                        required
                      />
                      <button
                        class="btn btn-outline-secondary"
                        type="button"
                        @click="showPassword = !showPassword"
                      >
                        {{ showPassword ? '👁️' : '👁️‍🗨️' }}
                      </button>
                    </div>
                    <div v-if="errors.password" class="invalid-feedback d-block">{{ errors.password }}</div>
                  </div>

                  <div class="col-md-6">
                    <label for="confirmPassword" class="form-label fw-semibold">{{ t('confirmPassword') }}</label>
                    <input
                      id="confirmPassword"
                      v-model="form.confirmPassword"
                      :type="showConfirmPassword ? 'text' : 'password'"
                      class="form-control form-control-lg"
                      :class="{ 'is-invalid': errors.confirmPassword }"
                      :placeholder="t('confirmPassword')"
                      required
                    />
                    <div v-if="errors.confirmPassword" class="invalid-feedback">{{ errors.confirmPassword }}</div>
                  </div>
                </div>

                <div v-if="errorMessage" class="alert alert-danger" role="alert">
                  {{ errorMessage }}
                </div>

                <button type="submit" class="btn btn-primary btn-lg w-100 mb-3" :disabled="loading">
                  <span v-if="loading">{{ t('createAccount') }}...</span>
                  <span v-else>{{ t('createAccount') }}</span>
                </button>
              </form>

              <div class="text-center pt-3 border-top">
                <p class="mb-2 text-muted">
                  {{ t('haveAccount') }}
                  <router-link to="/login" class="text-decoration-none fw-semibold">{{ t('login') }}</router-link>
                </p>
                <router-link to="/" class="text-decoration-none small text-muted">{{ t('home') }}</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../utils/api'
import { i18n } from '../utils/i18n'
import ThemeToggle from '../components/ThemeToggle.vue'
import LanguageToggle from '../components/LanguageToggle.vue'
import FloatingHeader from '../components/FloatingHeader.vue'
import MedicalIcons from '../components/MedicalIcons.vue'

const router = useRouter()
const currentLang = ref(i18n.current)

const form = reactive({
  name: '',
  username: '',
  email: '',
  phone: '',
  role: 'patient',
  password: '',
  confirmPassword: '',
})

const errors = reactive({
  name: '',
  username: '',
  email: '',
  phone: '',
  role: '',
  password: '',
  confirmPassword: '',
})

const showPassword = ref(false)
const showConfirmPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')

const t = (key) => {
  const _ = currentLang.value
  return i18n.t(key)
}

const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

const validatePhone = (phone) => {
  const re = /^[\d\s\-\+\(\)]+$/
  return re.test(phone) && phone.replace(/\D/g, '').length >= 10
}

const validateForm = () => {
  Object.keys(errors).forEach(key => errors[key] = '')
  let isValid = true

  if (!form.name.trim()) {
    errors.name = 'Full name is required'
    isValid = false
  } else if (form.name.trim().length < 2) {
    errors.name = 'Name must be at least 2 characters'
    isValid = false
  }

  if (!form.username.trim()) {
    errors.username = 'Username is required'
    isValid = false
  } else if (form.username.trim().length < 3) {
    errors.username = 'Username must be at least 3 characters'
    isValid = false
  }

  if (!form.email.trim()) {
    errors.email = 'Email is required'
    isValid = false
  } else if (!validateEmail(form.email)) {
    errors.email = 'Please enter a valid email address'
    isValid = false
  }

  if (!form.phone.trim()) {
    errors.phone = 'Phone number is required'
    isValid = false
  } else if (!validatePhone(form.phone)) {
    errors.phone = 'Please enter a valid phone number'
    isValid = false
  }

  if (!form.role || !['patient', 'doctor'].includes(form.role)) {
    errors.role = 'Please select a valid role'
    isValid = false
  }

  if (!form.password) {
    errors.password = 'Password is required'
    isValid = false
  } else if (form.password.length < 6) {
    errors.password = 'Password must be at least 6 characters'
    isValid = false
  }

  if (!form.confirmPassword) {
    errors.confirmPassword = 'Please confirm your password'
    isValid = false
  } else if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match'
    isValid = false
  }

  return isValid
}

const handleRegister = async () => {
  errorMessage.value = ''
  
  if (!validateForm()) {
    return
  }

  loading.value = true

  try {
    const { confirmPassword, ...registerData } = form
    const response = await api.register(registerData)
    
    localStorage.setItem('user', JSON.stringify(response.data))
    
    alert('Registration successful! Please login.')
    router.push('/login')
  } catch (error) {
    errorMessage.value = error.message || 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  const updateLanguage = () => {
    currentLang.value = i18n.current
  }
  window.addEventListener('languagechange', updateLanguage)
})
</script>

<style scoped>
/* Minimal custom styles - Bootstrap handles most styling */
.signup-page {
  background: linear-gradient(135deg, #e8f4f8 0%, #f0e8f5 100%);
}
</style>
