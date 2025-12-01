<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Patients</h2>
      <!-- <button class="btn btn-primary" @click="showAddModal">Add Patient</button> -->
    </div>

    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else class="table-responsive">
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Gender</th>
            <th>DOB</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="patient in patients" :key="patient.id">
            <td>{{ patient.id }}</td>
            <td>{{ patient.user ? patient.user.name : 'N/A' }}</td>
            <td>{{ patient.user ? patient.user.email : 'N/A' }}</td>
            <td>{{ patient.phone }}</td>
            <td>{{ patient.gender || '-' }}</td>
            <td>{{ patient.dob || '-' }}</td>
            <td>
              <button class="btn btn-sm btn-info me-2" @click="editPatient(patient)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deletePatient(patient.id)" v-if="isAdmin">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="patients.length === 0" class="text-center">No patients found.</p>
    </div>

    <!-- Edit Modal (Simple implementation) -->
    <div v-if="showModal" class="modal fade show d-block" tabindex="-1" role="dialog" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Patient</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
             <form @submit.prevent="updatePatient">
                <div class="mb-3">
                    <label class="form-label">Phone</label>
                    <input type="text" class="form-control" v-model="currentPatient.phone" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Gender</label>
                    <select class="form-select" v-model="currentPatient.gender">
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label">Date of Birth</label>
                    <input type="date" class="form-control" v-model="currentPatient.dob">
                </div>
                 <div class="mb-3">
                    <label class="form-label">Address</label>
                    <textarea class="form-control" v-model="currentPatient.address"></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Save changes</button>
             </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../utils/api';

const patients = ref([]);
const loading = ref(true);
const error = ref('');
const showModal = ref(false);
const currentPatient = ref({});

const isAdmin = computed(() => {
    const user = JSON.parse(localStorage.getItem('user'));
    return user && user.roles && user.roles.includes('admin');
});

const fetchPatients = async () => {
  loading.value = true;
  try {
    const response = await api.get('/patients'); // Assuming /api/patient returns list
    patients.value = response.data;
  } catch (err) {
    error.value = 'Failed to load patients.';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const deletePatient = async (id) => {
    if(!confirm('Are you sure you want to delete this patient?')) return;
    
    try {
        await api.delete(`/patient/${id}`);
        patients.value = patients.value.filter(p => p.id !== id);
    } catch (err) {
        alert('Failed to delete patient');
        console.error(err);
    }
};

const editPatient = (patient) => {
    // Clone to avoid modifying directly
    currentPatient.value = { ...patient };
    // Ensure DOB is in YYYY-MM-DD format for input type=date
    if (currentPatient.value.dob) {
        // Assuming API returns ISO string or similar, might need formatting
        // If it's already YYYY-MM-DD, fine.
    }
    showModal.value = true;
};

const closeModal = () => {
    showModal.value = false;
    currentPatient.value = {};
};

const updatePatient = async () => {
    try {
        const payload = {
            phone: currentPatient.value.phone,
            gender: currentPatient.value.gender,
            dob: currentPatient.value.dob,
            address: currentPatient.value.address,
            user_id: currentPatient.value.user_id // Required by parser?
        };
        
        // We need to send user_id because the parser requires it? 
        // Let's check the parser in patient_resource.py: parser.add_argument("user_id", type=int, required=True)
        // Yes, it is required.
        
        await api.put(`/patient/${currentPatient.value.id}`, payload);
        
        // Update local list
        const index = patients.value.findIndex(p => p.id === currentPatient.value.id);
        if (index !== -1) {
            // Update only the fields we changed, or refetch. 
            // Ideally refetch or merge.
            // For now, let's just update the fields in the list to reflect changes immediately
            patients.value[index] = { ...patients.value[index], ...payload };
        }
        closeModal();
        fetchPatients(); // Refetch to be sure (e.g. if backend does formatting)
    } catch (err) {
        alert('Failed to update patient');
        console.error(err);
    }
};

onMounted(() => {
  fetchPatients();
});
</script>
