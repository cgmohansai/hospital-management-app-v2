<template>
  <header class="navbar navbar-expand-lg navbar-light bg-white shadow-sm fixed-top" :class="{ 'scrolled': isScrolled }">
    <div class="container">
      <div class="d-flex align-items-center">
        <div class="me-3">
          <MedicalIcons type="hospital" :color="'#3b82f6'" :strokeColor="'#8b5cf6'" style="width: 40px; height: 40px;" />
        </div>
        <span class="navbar-brand mb-0 h1 fw-bold text-primary">{{ t('hospitalName') }}</span>
      </div>
      
      <div class="d-flex align-items-center gap-3 d-none d-md-flex">
        <div class="d-flex gap-2">
          <div v-for="(item, index) in medicalIcons" :key="index" class="p-2">
            <MedicalIcons 
              :type="item.type" 
              :color="'#3b82f6'" 
              :strokeColor="'#8b5cf6'"
              style="width: 28px; height: 28px; opacity: 0.7;"
            />
          </div>
        </div>
      </div>
      
      <div class="d-flex align-items-center gap-2">
        <router-link to="/login" class="btn btn-link text-decoration-none d-none d-md-inline">{{ t('login') }}</router-link>
        <router-link to="/signup" class="btn btn-primary rounded-pill px-4">{{ t('signup') }}</router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { i18n } from '../utils/i18n'
import MedicalIcons from './MedicalIcons.vue'

const isScrolled = ref(false)
const currentLang = ref(i18n.current)

const t = (key) => {
  const _ = currentLang.value
  return i18n.t(key)
}

const medicalIcons = [
  { type: 'heart' },
  { type: 'stethoscope' },
  { type: 'doctor' },
  { type: 'nurse' }
]

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  const updateLanguage = () => {
    currentLang.value = i18n.current
  }
  window.addEventListener('languagechange', updateLanguage)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
/* Minimal custom styles - Bootstrap handles most styling */
.navbar.scrolled {
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.95) !important;
}
</style>
