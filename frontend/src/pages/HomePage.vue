<template>
  <div class="home-page">
    <!-- Floating Header -->
    <FloatingHeader />
    
    <!-- Theme and Language Toggles -->
    <ThemeToggle />
    <LanguageToggle />
    
    <!-- Hero Section -->
    <section class="hero-section vh-100 d-flex align-items-center justify-content-center position-relative">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-10 text-center">
            <div class="mb-4">
              <MedicalIcons type="hospital" :color="'#3b82f6'" :strokeColor="'#8b5cf6'" class="mb-3" style="width: 80px; height: 80px;" />
            </div>
            <h1 class="display-3 fw-bold mb-3">
              <span class="text-muted d-block fs-4 mb-2">{{ t('welcome') }}</span>
              <span class="text-primary">{{ t('hospitalName') }}</span>
            </h1>
            <p class="lead text-muted mb-5">{{ t('tagline') }}</p>
            <div class="d-flex gap-3 justify-content-center flex-wrap">
              <router-link to="/signup" class="btn btn-primary btn-lg px-5 py-3 rounded-pill">
                {{ t('getStarted') }}
              </router-link>
              <router-link to="/login" class="btn btn-outline-primary btn-lg px-5 py-3 rounded-pill">
                {{ t('learnMore') }}
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section py-5" ref="featuresRef">
      <div class="container">
        <h2 class="text-center display-4 fw-bold mb-5">{{ t('features.title') }}</h2>
        <div class="row g-4">
          <div 
            v-for="(feature, index) in features" 
            :key="index"
            class="col-md-6 col-lg-3"
          >
            <div class="card h-100 shadow-sm border-0">
              <div class="card-body text-center p-4">
                <div class="mb-3">
                  <MedicalIcons 
                    :type="feature.iconType" 
                    :color="'#3b82f6'" 
                    :strokeColor="'#8b5cf6'"
                    style="width: 60px; height: 60px;"
                  />
                </div>
                <h3 class="h5 fw-bold mb-3">{{ t(feature.title) }}</h3>
                <p class="text-muted mb-0">{{ t(feature.desc) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Services Section -->
    <section class="services-section py-5 bg-light" ref="servicesRef">
      <div class="container">
        <h2 class="text-center display-4 fw-bold mb-5">{{ t('services') }}</h2>
        <div class="row g-4">
          <div 
            v-for="(service, index) in services" 
            :key="index"
            class="col-md-6 col-lg-4"
          >
            <div class="card h-100 shadow-sm border-0">
              <div class="card-body text-center p-4">
                <div class="mb-3">
                  <MedicalIcons 
                    :type="service.iconType" 
                    :color="'#3b82f6'" 
                    :strokeColor="'#8b5cf6'"
                    style="width: 60px; height: 60px;"
                  />
                </div>
                <h3 class="h5 fw-bold mb-3">{{ service.name }}</h3>
                <p class="text-muted mb-0">{{ service.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { i18n } from '../utils/i18n'
import ThemeToggle from '../components/ThemeToggle.vue'
import LanguageToggle from '../components/LanguageToggle.vue'
import FloatingHeader from '../components/FloatingHeader.vue'
import MedicalIcons from '../components/MedicalIcons.vue'

const router = useRouter()
const featuresRef = ref(null)
const servicesRef = ref(null)
const currentLang = ref(i18n.current)

const t = (key) => {
  const _ = currentLang.value
  return i18n.t(key)
}

const features = [
  { iconType: 'hospital', title: 'features.care', desc: 'features.careDesc' },
  { iconType: 'doctor', title: 'features.experts', desc: 'features.expertsDesc' },
  { iconType: 'stethoscope', title: 'features.technology', desc: 'features.technologyDesc' },
  { iconType: 'heart', title: 'features.support', desc: 'features.supportDesc' }
]

const services = [
  { iconType: 'stethoscope', name: 'General Medicine', description: 'Comprehensive health care services' },
  { iconType: 'doctor', name: 'Specialist Care', description: 'Expert medical consultations' },
  { iconType: 'heart', name: 'Cardiology', description: 'Heart and cardiovascular care' },
  { iconType: 'nurse', name: 'Nursing Care', description: 'Professional nursing services' }
]

const handleScroll = () => {
  const elements = [featuresRef.value, servicesRef.value]
  
  elements.forEach(el => {
    if (!el) return
    
    const rect = el.getBoundingClientRect()
    const isVisible = rect.top < window.innerHeight && rect.bottom > 0
    
    if (isVisible) {
      el.classList.add('visible')
    }
  })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll()
  
  const updateLanguage = () => {
    currentLang.value = i18n.current
  }
  window.addEventListener('languagechange', updateLanguage)
})
</script>

<style scoped>
/* Minimal custom styles - Bootstrap handles most styling */
.hero-section {
  background: linear-gradient(135deg, #e8f4f8 0%, #f0e8f5 100%);
}
</style>
