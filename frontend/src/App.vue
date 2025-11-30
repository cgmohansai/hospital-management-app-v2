<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { theme } from './utils/theme'
import { i18n } from './utils/i18n'

export default {
  name: 'App',
  setup() {
    onMounted(() => {
      theme.init()
      i18n.init()
    })
  }
}
</script>

<style>
/* Minimal custom styles - Bootstrap handles most styling */
html {
  scroll-behavior: smooth;
}
</style>
