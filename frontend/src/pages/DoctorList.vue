<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Doctors</h2>
      <button class="btn btn-primary" @click="showAddModal">Add Doctor</button>
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
            <th>Specialization</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="doc in doctors" :key="doc.id">
            <td>{{ doc.id }}</td>
            <td>{{ doc.user ? doc.user.name : 'N/A' }}</td>
            <td>{{ doc.user ? doc.user.email : 'N/A' }}</td>
            <td>{{ doc.specialization }}</td>
            <td>
                <span :class="doc.is_active ? 'badge bg-success' : 'badge bg-warning'">
                    {{ doc.is_active ? 'Active' : 'Pending' }}
                </span>
            </td>
            <td>
              <button class="btn btn-sm btn-success me-2" @click="approveDoctor(doc)" v-if="!doc.is_active">Approve</button>
              <button class="btn btn-sm btn-info me-2" @click="editDoctor(doc)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deleteDoctor(doc.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="doctors.length === 0" class="text-center">No doctors found.</p>
    </div>

    <!-- Add Doctor Modal -->
    <div v-if="showAddDoctorModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add New Doctor</h5>
            <button type="button" class="btn-close" @click="closeAddModal"></button>
          </div>
          <div class="modal-body">
             <form @submit.prevent="addDoctor">
                <div class="mb-3">
                    <label class="form-label">Username</label>
                    <input type="text" class="form-control" v-model="newDoctor.username" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input type="email" class="form-control" v-model="newDoctor.email" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Name</label>
                    <input type="text" class="form-control" v-model="newDoctor.name" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Password</label>
                    <input type="password" class="form-control" v-model="newDoctor.password" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Phone</label>
                    <input type="tel" class="form-control" v-model="newDoctor.phone" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Specialization</label>
                    <input type="text" class="form-control" v-model="newDoctor.specialization" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Bio</label>
                    <textarea class="form-control" v-model="newDoctor.bio"></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Create Doctor</button>
             </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Doctor</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
             <form @submit.prevent="updateDoctor">
                <div class="mb-3">
                    <label class="form-label">Specialization</label>
                    <input type="text" class="form-control" v-model="currentDoctor.specialization" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Bio</label>
                    <textarea class="form-control" v-model="currentDoctor.bio"></textarea>
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
import { ref, onMounted } from 'vue';
import api from '../utils/api';

const doctors = ref([]);
const loading = ref(true);
const error = ref('');
const showModal = ref(false);
const showAddDoctorModal = ref(false);
const currentDoctor = ref({});
const newDoctor = ref({
    username: '',
    email: '',
    name: '',
    password: '',
    phone: '',
    specialization: '',
    bio: '',
    role: 'doctor'
});

const fetchDoctors = async () => {
  loading.value = true;
  try {
    const response = await api.get('/doctors');
    doctors.value = response.data;
  } catch (err) {
    error.value = 'Failed to load doctors.';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const showAddModal = () => {
    showAddDoctorModal.value = true;
};

const closeAddModal = () => {
    showAddDoctorModal.value = false;
    newDoctor.value = {
        username: '',
        email: '',
        name: '',
        password: '',
        phone: '',
        specialization: '',
        bio: '',
        role: 'doctor'
    };
};

const addDoctor = async () => {
    try {
        const registerResponse = await api.post('/auth/register', {
            username: newDoctor.value.username,
            email: newDoctor.value.email,
            name: newDoctor.value.name,
            password: newDoctor.value.password,
            phone: newDoctor.value.phone,
            role: 'doctor'
        });
        
        const newUserId = registerResponse.data.id;
        
        // Now create doctor profile
        await api.post('/doctor', {
            user_id: newUserId,
            specialization: newDoctor.value.specialization,
            bio: newDoctor.value.bio,
            is_active: true // Admin created, so auto-active? Or false? Let's say true.
        });
        
        closeAddModal();
        fetchDoctors();
        alert('Doctor added successfully');
        
    } catch (err) {
        console.error(err);
        let msg = 'Failed to add doctor';
        if (err.response && err.response.data && err.response.data.message) {
            msg = err.response.data.message;
        }
        alert(msg);
    }
};

const approveDoctor = async (doc) => {
    if(!confirm(`Approve Dr. ${doc.user ? doc.user.name : ''}?`)) return;
    try {
        await api.patch(`/doctor/${doc.id}`, { is_active: true });
        // Update local state
        doc.is_active = true;
    } catch (err) {
        alert('Failed to approve doctor');
        console.error(err);
    }
};

const deleteDoctor = async (id) => {
    if(!confirm('Are you sure you want to delete this doctor?')) return;
    try {
        await api.delete(`/doctor/${id}`);
        doctors.value = doctors.value.filter(d => d.id !== id);
    } catch (err) {
        alert('Failed to delete doctor');
        console.error(err);
    }
};

const editDoctor = (doc) => {
    currentDoctor.value = { ...doc };
    showModal.value = true;
};

const closeModal = () => {
    showModal.value = false;
    currentDoctor.value = {};
};

const updateDoctor = async () => {
    try {
        await api.patch(`/doctor/${currentDoctor.value.id}`, {
            specialization: currentDoctor.value.specialization,
            bio: currentDoctor.value.bio
        });
        
        const index = doctors.value.findIndex(d => d.id === currentDoctor.value.id);
        if (index !== -1) {
            doctors.value[index] = { ...doctors.value[index], ...currentDoctor.value };
        }
        closeModal();
    } catch (err) {
        alert('Failed to update doctor');
        console.error(err);
    }
};

onMounted(() => {
  fetchDoctors();
});
</script>
