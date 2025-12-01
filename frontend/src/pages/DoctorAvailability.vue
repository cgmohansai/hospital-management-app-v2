<template>
  <div class="container mt-5">
    <h2 class="mb-4 text-center">Check Availability</h2>
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="availability.length > 0">
      <div class="row g-4">
        <div class="col-md-4 col-lg-3" v-for="(day, index) in availability" :key="index">
          <div class="card h-100 shadow-sm border-0">
            <div class="card-header bg-light text-center">
              <h5 class="mb-0">{{ day.day_name }}</h5>
              <small class="text-muted">{{ formatDate(day.date) }}</small>
            </div>
            <div class="card-body">
              <div v-if="day.slots.length === 0" class="text-center text-muted small">
                No slots available
              </div>
              <div v-else class="d-grid gap-2">
                <button 
                  v-for="(slot, sIndex) in day.slots" 
                  :key="sIndex"
                  class="btn btn-sm"
                  :class="getSlotClass(slot)"
                  :disabled="slot.is_booked || bookingLoading"
                  @click="selectSlot(day.date, slot)"
                >
                  {{ formatTime(slot.start_time) }} - {{ formatTime(slot.end_time) }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Booking Confirmation Modal (Simplified as a section for now) -->
      <div v-if="selectedSlot" class="fixed-bottom bg-white shadow-lg p-4 border-top" style="z-index: 1050;">
        <div class="container">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h5 class="mb-1">Confirm Booking</h5>
              <p class="mb-0 text-muted">
                {{ formatDate(selectedDate) }} at {{ formatTime(selectedSlot.start_time) }}
              </p>
            </div>
            <div class="d-flex gap-2">
              <button class="btn btn-outline-secondary" @click="selectedSlot = null">Cancel</button>
              <button class="btn btn-primary" @click="bookAppointment" :disabled="bookingLoading">
                <span v-if="bookingLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Confirm Booking
              </button>
            </div>
          </div>
          <div v-if="error" class="alert alert-danger mt-3 mb-0">{{ error }}</div>
        </div>
      </div>
    </div>

    <div v-else class="text-center">
      <p>No availability found for this doctor.</p>
      <button @click="$router.go(-1)" class="btn btn-primary">Go Back</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../utils/api';

const route = useRoute();
const router = useRouter();
const availability = ref([]);
const loading = ref(true);
const bookingLoading = ref(false);
const error = ref('');

const selectedSlot = ref(null);
const selectedDate = ref(null);

const fetchAvailability = async () => {
  try {
    const response = await api.get(`/doctors/${route.params.id}/availability`);
    availability.value = response.data;
  } catch (err) {
    console.error("Failed to fetch availability", err);
  } finally {
    loading.value = false;
  }
};

const formatDate = (dateStr) => {
  const options = { month: 'short', day: 'numeric' };
  return new Date(dateStr).toLocaleDateString(undefined, options);
};

const formatTime = (timeStr) => {
  // timeStr is HH:MM
  const [hours, minutes] = timeStr.split(':');
  const date = new Date();
  date.setHours(hours);
  date.setMinutes(minutes);
  return date.toLocaleTimeString(undefined, { hour: 'numeric', minute: '2-digit' });
};

const getSlotClass = (slot) => {
  if (slot.is_booked) return 'btn-danger text-white opacity-75';
  if (selectedSlot.value === slot) return 'btn-primary';
  return 'btn-outline-success';
};

const selectSlot = (date, slot) => {
  selectedDate.value = date;
  selectedSlot.value = slot;
  error.value = '';
};

const bookAppointment = async () => {
  if (!selectedSlot.value || !selectedDate.value) return;
  
  bookingLoading.value = true;
  error.value = '';
  
  try {
    const user = JSON.parse(localStorage.getItem('user'));
    // We need patient_id. Assuming user object has it or we need to fetch it.
    // Actually, backend expects patient_id.
    // If user is patient, we need their patient_id.
    // Let's assume we can get it from /users/me or similar, or it's in localStorage.
    // In Login.vue, we store user details. Let's check if patient_id is there.
    // Login.vue stores: id, username, email, name, roles.
    // It does NOT store patient_id.
    // We need to fetch patient profile or assume patient_id = user.id (which is NOT true based on models).
    // Patient model has user_id.
    
    // Quick fix: Fetch current user's patient profile first.
    // Or, update Login to return patient_id.
    // Or, fetch /patients?user_id=...
    
    // Let's try to fetch patient details using user_id from localStorage
    const patientsResponse = await api.get('/patients'); // This returns all patients. Not ideal.
    // We need to filter by user_id.
    // But PatientListResource doesn't support filtering by user_id yet?
    // Let's check PatientListResource.
    
    // Ideally, we should have an endpoint /patients/me or similar.
    // For now, let's fetch all and find. (Inefficient but works for small scale)
    const myPatient = patientsResponse.data.find(p => p.user.id === user.id);
    
    if (!myPatient) {
      error.value = "Could not find patient profile. Please contact support.";
      return;
    }

    await api.post('/appointment', {
      patient_id: myPatient.id,
      doctor_id: route.params.id,
      date: selectedDate.value,
      time: selectedSlot.value.start_time,
      status: 'Booked'
    });
    
    alert('Appointment booked successfully!');
    router.push('/appointments');
    
  } catch (err) {
    console.error(err);
    error.value = err.response?.data?.message || 'Failed to book appointment.';
  } finally {
    bookingLoading.value = false;
  }
};

onMounted(() => {
  fetchAvailability();
});
</script>
