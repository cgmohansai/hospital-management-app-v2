<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm sticky-top">
    <div class="container">
      <router-link class="navbar-brand d-flex align-items-center fw-bold text-primary" to="/">
        <img src="/logo.jpg" alt="Logo" class="me-2 rounded" height="30">
        LifeSync
      </router-link>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav mx-auto mb-2 mb-lg-0">
          
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle custom-dropdown-toggle" href="#" id="findDoctorDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Find a Doctor
            </a>
            <div class="dropdown-menu p-3" aria-labelledby="findDoctorDropdown" style="min-width: 600px;">
              <div class="d-flex flex-row">
                <ul class="list-unstyled me-4 mb-0" v-for="(column, colIndex) in departmentColumns" :key="colIndex">
                  <li v-for="(dept, index) in column" :key="index">
                    <router-link class="dropdown-item rounded" :to="`/department/${dept}`">{{ dept }}</router-link>
                  </li>
                </ul>
              </div>
            </div>
          </li>

          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle custom-dropdown-toggle" href="#" id="specialistsDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Specialists
            </a>
            <div class="dropdown-menu p-3" aria-labelledby="specialistsDropdown" style="min-width: 600px;">
              <div class="d-flex flex-row">
                <ul class="list-unstyled me-4 mb-0" v-for="(column, colIndex) in departmentColumns" :key="colIndex">
                  <li v-for="(dept, index) in column" :key="index">
                    <router-link class="dropdown-item rounded" :to="`/department/${dept}#specialists`">{{ dept }}</router-link>
                  </li>
                </ul>
              </div>
            </div>
          </li>

          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle custom-dropdown-toggle" href="#" id="discoverDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Discover LifeSync
            </a>
            <ul class="dropdown-menu" aria-labelledby="discoverDropdown">
              <li><router-link class="dropdown-item" to="/#hero">Home</router-link></li>
              <li><router-link class="dropdown-item" to="/#services">Services</router-link></li>
              <li><router-link class="dropdown-item" to="/#coe">Center of Excellence</router-link></li>
              <li><router-link class="dropdown-item" to="/#stats">Key Stats</router-link></li>
              <li><router-link class="dropdown-item" to="/#facilities">Facilities</router-link></li>
              <li><router-link class="dropdown-item" to="/#testimonials">Testimonials</router-link></li>
              <li><router-link class="dropdown-item" to="/#faq">FAQ</router-link></li>
            </ul>
          </li>
        </ul>

        <!-- Right Side -->
        <div class="d-flex align-items-center">
          <router-link v-if="!isAuthenticated" to="/login" class="btn btn-primary px-4 me-3 rounded-pill">
            Book Appointment
          </router-link>

          <!-- User Menu -->
          <div class="dropdown" v-if="isAuthenticated">
            <a class="nav-link dropdown-toggle text-dark" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="bi bi-person-circle fs-5 me-1"></i> {{ username }}
            </a>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
              <li><router-link class="dropdown-item" to="/dashboard">Dashboard</router-link></li>
              <li v-if="isPatient"><router-link class="dropdown-item" to="/profile">Edit Profile</router-link></li>
              <li v-if="isPatient"><router-link class="dropdown-item" to="/history">History</router-link></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item text-danger" href="#" @click.prevent="logout">Logout</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// -- State --

// List of all medical departments available in the hospital
const departments = ref([
  'Cardiology', 'Neurology', 'Orthopedics', 'Oncology',
  'Gynecology', 'Pediatrics', 'General Surgery', 'General Medicine'
]);

// -- Computed Properties --

// Check if user is logged in based on token presence
const isAuthenticated = computed(() => !!localStorage.getItem('token'));

// Get current username from local storage
const username = computed(() => {
  const user = JSON.parse(localStorage.getItem('user'));
  return user ? user.username : '';
});

// Check if the current user has the 'patient' role
const isPatient = computed(() => {
  const user = JSON.parse(localStorage.getItem('user'));
  return user && user.roles && user.roles.includes('patient');
});

// Split departments into chunks (columns) for better UI display in dropdowns
// This creates a multi-column layout for long lists
const departmentColumns = computed(() => {
  const itemsPerColumn = 6;
  const columns = [];
  for (let i = 0; i < departments.value.length; i += itemsPerColumn) {
    columns.push(departments.value.slice(i, i + itemsPerColumn));
  }
  return columns;
});

// -- Methods --

const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  router.push('/login').then(() => {
      window.location.reload();
  });
};
</script>

<style scoped>
.navbar {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.nav-link {
  font-weight: 500;
  color: #333;
}
.nav-link:hover {
  color: #0d6efd;
}
.dropdown-item:active {
  background-color: #0d6efd;
}
.custom-dropdown-toggle {
  border: 2px solid #0d6efd; /* Blue border */
  border-radius: 20px;       /* Rounded corners */
  padding: 5px 15px;         /* Padding for better look */
  margin: 0 5px;             /* Spacing between buttons */
  transition: all 0.3s ease; /* Smooth transition */
}
.custom-dropdown-toggle:hover, .custom-dropdown-toggle[aria-expanded="true"] {
  background-color: #0d6efd;
  color: white !important;
}
</style>
