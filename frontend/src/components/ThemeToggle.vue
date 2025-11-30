<template>
  <button class="btn btn-light rounded-circle position-fixed top-0 end-0 m-3 shadow" 
          @click="toggleTheme" 
          :aria-label="t('theme')"
          style="width: 50px; height: 50px; z-index: 1000;">
    <span class="fs-5">{{ isDark ? '☀️' : '🌙' }}</span>
  </button>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { theme } from '../utils/theme'
import { i18n } from '../utils/i18n'

const isDark = ref(false)

const t = (key) => i18n.t(key)

const toggleTheme = () => {
  const newTheme = theme.toggle()
  isDark.value = newTheme === 'dark'
}

onMounted(() => {
  isDark.value = theme.isDark()
})
</script>
