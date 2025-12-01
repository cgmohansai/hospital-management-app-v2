<template>
  <div id="app">
    <Navbar />
    <router-view />
    <Footer />
  </div>
</template>

<script setup>
import Navbar from './components/navbar.vue';
import Footer from './components/footer.vue';
</script>

<style>
body {
  font-family: 'Poppins', sans-serif;
}
</style>
