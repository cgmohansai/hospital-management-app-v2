<template>
  <div class="container mt-5" v-if="doctor">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow-sm border-0">
          <div class="card-body p-5">
            <div class="text-center mb-4">
              <div class="bg-secondary rounded-circle mx-auto d-flex align-items-center justify-content-center text-white display-1 mb-3" style="width: 150px; height: 150px;">
                {{ doctor.user ? doctor.user.name.charAt(0) : 'D' }}
              </div>
              <h2 class="fw-bold">{{ doctor.user ? doctor.user.name : 'Doctor' }}</h2>
              <p class="text-primary fs-5">{{ doctor.specialization }}</p>
            </div>

            <div class="mb-4">
              <h5 class="fw-bold text-secondary text-uppercase small ls-1">Bio</h5>
              <p class="text-muted">{{ doctor.bio || 'No bio available.' }}</p>
            </div>

            <div class="row mb-4">
              <div class="col-md-6">
                <h5 class="fw-bold text-secondary text-uppercase small ls-1">Experience</h5>
                <p>{{ doctor.experience || 'N/A' }}</p>
              </div>
              <div class="col-md-6">
                <h5 class="fw-bold text-secondary text-uppercase small ls-1">Qualification</h5>
                <p>{{ doctor.qualification || 'N/A' }}</p>
              </div>
            </div>

            <div class="d-grid gap-2 d-md-flex justify-content-md-center">
              <button @click="$router.go(-1)" class="btn btn-outline-secondary px-4 rounded-pill">Go Back</button>
              <router-link :to="`/doctor/${doctor.id}/availability`" class="btn btn-primary px-4 rounded-pill">Check Availability</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else-if="loading" class="text-center mt-5">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <div v-else class="text-center mt-5">
    <h3>Doctor not found</h3>
    <button @click="$router.go(-1)" class="btn btn-primary mt-3">Go Back</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../utils/api';

const route = useRoute();
const doctor = ref(null);
const loading = ref(true);

const fetchDoctor = async () => {
  try {
    const response = await api.get(`/doctors/${route.params.id}`);
    doctor.value = response.data;
  } catch (err) {
    console.error("Failed to fetch doctor details", err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchDoctor();
});
</script>

<style scoped>
.ls-1 {
  letter-spacing: 1px;
}
</style>
