<template>
  <div class="login-page vh-100 d-flex align-items-center justify-content-center position-relative">
    <!-- Floating Header -->
    <FloatingHeader />
    
    <!-- Theme and Language Toggles -->
    <ThemeToggle />
    <LanguageToggle />
    
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5">
              <div class="text-center mb-4">
                <div class="mb-3">
                  <MedicalIcons type="hospital" :color="'#3b82f6'" :strokeColor="'#8b5cf6'" style="width: 60px; height: 60px;" />
                </div>
                <h1 class="h2 fw-bold mb-2">{{ t('login') }}</h1>
                <p class="text-muted">{{ t('tagline') }}</p>
              </div>

              <form @submit.prevent="handleLogin">
                <div class="mb-3">
                  <label for="username" class="form-label fw-semibold">
                    <MedicalIcons type="doctor" :color="'#3b82f6'" :strokeColor="'#8b5cf6'" class="me-2" style="width: 18px; height: 18px;" />
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

                <div class="mb-4">
                  <label for="password" class="form-label fw-semibold">
                    <MedicalIcons type="heart" :color="'#3b82f6'" :strokeColor="'#8b5cf6'" class="me-2" style="width: 18px; height: 18px;" />
                    {{ t('password') }}
                  </label>
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

                <div v-if="errorMessage" class="alert alert-danger" role="alert">
                  {{ errorMessage }}
                </div>

                <button type="submit" class="btn btn-primary btn-lg w-100 mb-3" :disabled="loading">
                  <span v-if="loading">{{ t('login') }}...</span>
                  <span v-else>{{ t('signIn') }}</span>
                </button>
              </form>

              <div class="text-center pt-3 border-top">
                <p class="mb-2 text-muted">
                  {{ t('noAccount') }}
                  <router-link to="/signup" class="text-decoration-none fw-semibold">{{ t('signup') }}</router-link>
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
  username: '',
  password: '',
})

const errors = reactive({
  username: '',
  password: '',
})

const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')

const t = (key) => {
  const _ = currentLang.value
  return i18n.t(key)
}

const validateForm = () => {
  errors.username = ''
  errors.password = ''
  let isValid = true

  if (!form.username.trim()) {
    errors.username = 'Username is required'
    isValid = false
  }

  if (!form.password) {
    errors.password = 'Password is required'
    isValid = false
  } else if (form.password.length < 6) {
    errors.password = 'Password must be at least 6 characters'
    isValid = false
  }

  return isValid
}

const handleLogin = async () => {
  errorMessage.value = ''
  
  if (!validateForm()) {
    return
  }

  loading.value = true

  try {
    const response = await api.login(form.username, form.password)
    
    localStorage.setItem('authToken', response.data.token)
    localStorage.setItem('user', JSON.stringify(response.data))
    
    router.push('/')
  } catch (error) {
    errorMessage.value = error.message || 'Login failed. Please try again.'
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
.login-page {
  background: linear-gradient(135deg, #e8f4f8 0%, #f0e8f5 100%);
}
</style>
