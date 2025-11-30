<template>
  <div class="dropdown position-fixed top-0 end-0 m-3" style="margin-right: 70px !important; z-index: 1000;">
    <button class="btn btn-light dropdown-toggle shadow" 
            @click="showMenu = !showMenu" 
            :aria-label="t('language')"
            type="button"
            id="languageDropdown"
            data-bs-toggle="dropdown"
            aria-expanded="false">
      <span class="me-2">🌐</span>
      <span>{{ currentLang.toUpperCase() }}</span>
    </button>
    <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="languageDropdown">
      <li v-for="lang in languages" :key="lang">
        <button
          class="dropdown-item"
          :class="{ 'active': lang === currentLang }"
          @click="changeLanguage(lang)"
          type="button"
        >
          {{ getLangName(lang) }}
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { i18n } from '../utils/i18n'

const showMenu = ref(false)
const currentLang = ref('en')
const languages = ['en', 'es', 'fr']

const t = (key) => i18n.t(key)

const getLangName = (code) => {
  const names = { en: 'English', es: 'Español', fr: 'Français' }
  return names[code] || code
}

const changeLanguage = (lang) => {
  i18n.setLanguage(lang)
  currentLang.value = lang
  showMenu.value = false
  window.dispatchEvent(new Event('languagechange'))
}

const handleClickOutside = (event) => {
  if (!event.target.closest('.dropdown')) {
    showMenu.value = false
  }
}

onMounted(() => {
  currentLang.value = i18n.current
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
