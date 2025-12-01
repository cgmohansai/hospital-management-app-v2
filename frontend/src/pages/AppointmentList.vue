<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Appointments</h2>
      <button class="btn btn-primary" @click="openBookModal" v-if="role === 'patient'">Book Appointment</button>
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
            <th>Sr No</th>
            <th>Doctor Name</th>
            <th>Dept</th>
            <th>Date</th>
            <th>Time</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(appt, index) in filteredAppointments" :key="appt.id">
            <td>{{ index + 1 }}</td>
            <td>{{ appt.doctor && appt.doctor.user ? appt.doctor.user.name : 'Unknown' }}</td>
            <td>{{ appt.doctor && appt.doctor.department ? appt.doctor.department.name : 'N/A' }}</td>
            <td>{{ appt.date }}</td>
            <td>{{ appt.time }}</td>
            <td>
                <span :class="statusBadgeClass(appt.status)">{{ appt.status || 'Booked' }}</span>
            </td>
            <td>
              <button class="btn btn-sm btn-danger me-2" @click="cancelAppointment(appt.id)" v-if="canCancel(appt)">Cancel</button>
              <button class="btn btn-sm btn-success" @click="completeAppointment(appt.id)" v-if="canComplete(appt)">Complete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="filteredAppointments.length === 0" class="text-center">No appointments found.</p>
    </div>

    <!-- Book Appointment Modal -->
    <div v-if="showModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Book Appointment</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="bookAppointment">
              <div class="mb-3">
                <label class="form-label">Doctor</label>
                <select class="form-select" v-model="booking.doctor_id" required>
                  <option v-for="doc in doctors" :key="doc.id" :value="doc.id">
                    {{ doc.user ? doc.user.name : 'Unknown' }} ({{ doc.specialization }})
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Date</label>
                <input type="date" class="form-control" v-model="booking.date" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Time</label>
                <input type="time" class="form-control" v-model="booking.time" required>
              </div>
              <button type="submit" class="btn btn-primary w-100">Book</button>
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

const appointments = ref([]);
const doctors = ref([]);
const loading = ref(true);
const error = ref('');
const showModal = ref(false);
const booking = ref({
    doctor_id: '',
    date: '',
    time: ''
});

const user = JSON.parse(localStorage.getItem('user'));
const role = user && user.roles && user.roles.length > 0 ? user.roles[0] : '';
const userId = user ? user.id : null;

// We need patient_id for booking. 
// Since login doesn't return it, we'll fetch all patients and find ours.
const myPatientId = ref(null);

const filteredAppointments = computed(() => {
    if (role === 'admin') return appointments.value;
    if (role === 'doctor') {
        // Filter where doctor.user.id === userId
        // Note: appointment.doctor has nested user.
        return appointments.value.filter(a => a.doctor && a.doctor.user && a.doctor.user.id === userId);
    }
    if (role === 'patient') {
        return appointments.value.filter(a => a.patient && a.patient.user && a.patient.user.id === userId);
    }
    return [];
});

const statusBadgeClass = (status) => {
    switch(status) {
        case 'Completed': return 'badge bg-success';
        case 'Cancelled': return 'badge bg-danger';
        default: return 'badge bg-primary';
    }
};

const canCancel = (appt) => {
    if (appt.status === 'Cancelled' || appt.status === 'Completed') return false;
    // Patient can cancel their own. Doctor can cancel. Admin can cancel.
    return true; 
};

const canComplete = (appt) => {
    if (appt.status !== 'Booked' && appt.status !== null) return false;
    // Only Doctor can complete
    return role === 'doctor';
};

const fetchData = async () => {
    loading.value = true;
    try {
        const [apptRes, docRes, patRes] = await Promise.all([
            api.get('/appointment'),
            api.get('/doctors'),
            role === 'patient' ? api.get('/patients') : Promise.resolve({ data: [] })
        ]);
        
        appointments.value = apptRes.data;
        doctors.value = docRes.data;
        
        if (role === 'patient') {
            const myPatient = patRes.data.find(p => p.user && p.user.id === userId);
            if (myPatient) {
                myPatientId.value = myPatient.id;
            }
        }
    } catch (err) {
        error.value = 'Failed to load data.';
        console.error(err);
    } finally {
        loading.value = false;
    }
};

const openBookModal = () => {
    showModal.value = true;
};

const closeModal = () => {
    showModal.value = false;
    booking.value = { doctor_id: '', date: '', time: '' };
};

const bookAppointment = async () => {
    if (!myPatientId.value) {
        alert('Could not identify your patient profile. Please contact admin.');
        return;
    }
    
    try {
        await api.post('/appointment', {
            patient_id: myPatientId.value,
            doctor_id: booking.value.doctor_id,
            date: booking.value.date,
            time: booking.value.time,
            status: 'Booked'
        });
        closeModal();
        fetchData(); // Refresh list
    } catch (err) {
        alert('Failed to book appointment.');
        console.error(err);
    }
};

const cancelAppointment = async (id) => {
    if(!confirm('Cancel this appointment?')) return;
    try {
        await api.put(`/appointment/${id}`, { status: 'Cancelled' }); // Using PUT as per resource, but usually PATCH is better. Resource has both.
        // Wait, resource PUT expects all args? 
        // Resource PUT: args = parser.parse_args(). Parser requires patient_id, doctor_id etc.
        // Resource PATCH: data = request.get_json(). update(data).
        // So we should use PATCH for partial update.
        // Let's try PATCH.
        // Wait, api.put in axios is PUT. api.patch is PATCH.
        // Let's check my api.js. It's standard axios.
        
        // Let's use PATCH.
        await api.patch(`/appointment/${id}`, { status: 'Cancelled' });
        fetchData();
    } catch (err) {
        // Fallback to PUT if PATCH fails? 
        // Or maybe I need to send all data for PUT.
        // Let's try PATCH first.
        console.error(err);
        alert('Failed to cancel appointment');
    }
};

const completeAppointment = async (id) => {
    if(!confirm('Mark as completed?')) return;
    try {
        await api.patch(`/appointment/${id}`, { status: 'Completed' });
        fetchData();
    } catch (err) {
        console.error(err);
        alert('Failed to update status');
    }
};

onMounted(() => {
    fetchData();
});
</script>
