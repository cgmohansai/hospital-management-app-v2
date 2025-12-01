<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-primary text-white">
            <h4 class="mb-0">Edit Profile</h4>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center my-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>

            <div v-else-if="error" class="alert alert-danger">
              {{ error }}
            </div>

            <form v-else @submit.prevent="updateProfile">
              <div class="mb-3">
                <label class="form-label fw-bold">Name</label>
                <input type="text" class="form-control" v-model="form.name" required>
              </div>

              <div class="mb-3">
                <label class="form-label fw-bold">Email</label>
                <input type="email" class="form-control" v-model="form.email" required>
              </div>

              <div class="mb-3">
                <label class="form-label fw-bold">Phone</label>
                <input type="tel" class="form-control" v-model="form.phone" required>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-bold">Date of Birth</label>
                  <input type="date" class="form-control" v-model="form.dob">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-bold">Gender</label>
                  <select class="form-select" v-model="form.gender">
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label fw-bold">Address</label>
                <textarea class="form-control" v-model="form.address" rows="3"></textarea>
              </div>

              <div class="mb-3">
                <label class="form-label fw-bold">New Password (leave blank to keep current)</label>
                <input type="password" class="form-control" v-model="form.password" placeholder="********">
              </div>

              <div class="d-flex justify-content-between mt-4">
                <button type="button" class="btn btn-outline-secondary" @click="$router.back()">Cancel</button>
                <button type="submit" class="btn btn-primary px-4">Save Changes</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../utils/api';

const router = useRouter();
const loading = ref(true);
const error = ref('');
const patientId = ref(null);

const form = ref({
  name: '',
  email: '',
  phone: '',
  dob: '',
  gender: '',
  address: '',
  password: ''
});

const fetchProfile = async () => {
  loading.value = true;
  try {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) {
      router.push('/login');
      return;
    }

    // Find patient profile
    const patientsRes = await api.get('/patients');
    const myPatient = patientsRes.data.find(p => p.user && p.user.id === user.id);

    if (myPatient) {
      patientId.value = myPatient.id;
      form.value.name = myPatient.user.name;
      form.value.email = myPatient.user.email;
      form.value.phone = myPatient.phone;
      form.value.dob = myPatient.dob;
      form.value.gender = myPatient.gender;
      form.value.address = myPatient.address;
    } else {
      error.value = "Patient profile not found.";
    }
  } catch (err) {
    console.error(err);
    error.value = "Failed to load profile.";
  } finally {
    loading.value = false;
  }
};

const updateProfile = async () => {
  if (!patientId.value) return;

  try {
    const payload = {
      name: form.value.name,
      email: form.value.email,
      phone: form.value.phone,
      dob: form.value.dob,
      gender: form.value.gender,
      address: form.value.address
    };

    if (form.value.password) {
      payload.password = form.value.password;
    }

    await api.put(`/patients/${patientId.value}`, payload);
    
    // Update local storage user name if changed
    const user = JSON.parse(localStorage.getItem('user'));
    if (user && user.name !== form.value.name) {
      user.name = form.value.name;
      localStorage.setItem('user', JSON.stringify(user));
      // Force reload to update navbar name or use a state store
      window.location.reload(); 
    } else {
        alert('Profile updated successfully');
        router.push('/dashboard');
    }

  } catch (err) {
    console.error(err);
    alert('Failed to update profile.');
  }
};

onMounted(() => {
  fetchProfile();
});
</script>
