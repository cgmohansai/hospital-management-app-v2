<template>
  <footer class="bg-dark text-white pt-5 pb-3 mt-5">
    <div class="container">
      <div class="row">
        <div class="col-md-4 mb-4">
          <h5>LifeSync</h5>
          <p>
            Best Multi-Speciality Hospital in Chennai, India. Health is our top priority.
          </p>
        </div>
        <div class="col-md-4 mb-4">
          <h5>Quick Links</h5>
          <ul class="list-unstyled">
            <li><router-link to="/" class="text-white text-decoration-none">Home</router-link></li>
            <li><router-link to="/login" class="text-white text-decoration-none">Login</router-link></li>
            <li><router-link to="/register" class="text-white text-decoration-none">Register</router-link></li>
          </ul>
        </div>
        <div class="col-md-4 mb-4">
          <h5>Contact Us</h5>
          <p><i class="bi bi-telephone-fill"></i>9898989898</p>
          <p><i class="bi bi-envelope-fill"></i> admin@study</p>
          <div class="d-flex gap-3">
            <a href="#" class="text-white"><i class="bi bi-facebook"></i></a>
            <a href="#" class="text-white"><i class="bi bi-twitter"></i></a>
            <a href="#" class="text-white"><i class="bi bi-instagram"></i></a>
            <a href="#" class="text-white"><i class="bi bi-linkedin"></i></a>
          </div>
        </div>
      </div>
      <hr class="bg-secondary">
      <div class="text-center">
        <p class="mb-0">&copy; LifeSync Hospitals - Built with 💜 by AppDev Team</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
footer {
  font-size: 0.9rem;
}
</style>
