<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">Medical History</h2>
      <button v-if="visits.length > 0" class="btn btn-success" @click="exportToCSV">
        <i class="bi bi-file-earmark-spreadsheet me-2"></i>Export to CSV
      </button>
    </div>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else class="row">
      <div class="col-md-12">
        <div class="card shadow-sm border-0">
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover align-middle">
                <thead class="table-light">
                  <tr>
                    <th>Date</th>
                    <th>Doctor</th>
                    <th>Department</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="visit in visits" :key="visit.id">
                    <td>{{ visit.date }}</td>
                    <td>{{ visit.doctor && visit.doctor.user ? visit.doctor.user.name : 'Unknown' }}</td>
                    <td>{{ visit.doctor && visit.doctor.department ? visit.doctor.department.name : 'N/A' }}</td>
                    <td>
                      <span :class="statusBadgeClass(visit.status)">{{ visit.status }}</span>
                    </td>
                    <td>
                      <button class="btn btn-sm btn-outline-primary rounded-pill px-3" @click="viewDetails(visit)">
                        View Details
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
              <p v-if="visits.length === 0" class="text-center text-muted mt-3">No medical history found.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    
    <div v-if="selectedVisit" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Visit Details - {{ selectedVisit.date }}</h5>
            <button type="button" class="btn-close" @click="closeDetails"></button>
          </div>
          <div class="modal-body">
            <div class="row mb-3">
              <div class="col-md-6">
                <strong>Doctor:</strong> {{ selectedVisit.doctor && selectedVisit.doctor.user ? selectedVisit.doctor.user.name : 'Unknown' }}
              </div>
              <div class="col-md-6">
                 <strong>Department:</strong> {{ selectedVisit.doctor && selectedVisit.doctor.department ? selectedVisit.doctor.department.name : 'N/A' }}
              </div>
            </div>
            
            <hr>

            <div v-if="selectedVisit.treatment">
              <div class="mb-3">
                <h6 class="fw-bold text-secondary text-uppercase small ls-1">Diagnosis</h6>
                <p>{{ selectedVisit.treatment.diagnosis || 'No diagnosis recorded.' }}</p>
              </div>
              
              <div class="mb-3">
                <h6 class="fw-bold text-secondary text-uppercase small ls-1">Tests Done</h6>
                <p>{{ selectedVisit.treatment.tests || 'No tests recorded.' }}</p>
              </div>

              <div class="mb-3">
                <h6 class="fw-bold text-secondary text-uppercase small ls-1">Prescription / Medicines</h6>
                <p>{{ selectedVisit.treatment.prescription || 'No prescription recorded.' }}</p>
              </div>

              <div class="mb-3">
                <h6 class="fw-bold text-secondary text-uppercase small ls-1">Doctor's Notes</h6>
                <p>{{ selectedVisit.treatment.notes || 'No notes available.' }}</p>
              </div>
            </div>
            <div v-else class="text-center text-muted py-4">
              <p>No treatment details available for this visit.</p>
            </div>

          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDetails">Close</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../utils/api';

const visits = ref([]);
const loading = ref(true);
const error = ref('');
const selectedVisit = ref(null);

const user = JSON.parse(localStorage.getItem('user'));
const userId = user ? user.id : null;

const route = useRoute();
const routePatientId = route.params.id;

const fetchHistory = async () => {
  loading.value = true;
  try {
    let patientIdToFetch = null;

    if (routePatientId) {
      
      patientIdToFetch = routePatientId;
    } else {
      
      const patientsRes = await api.get('/patients');
      const myPatient = patientsRes.data.find(p => p.user && p.user.id === userId);
      if (myPatient) {
        patientIdToFetch = myPatient.id;
      }
    }
    
    if (!patientIdToFetch) {
      error.value = "Patient profile not found.";
      return;
    }

    
    const apptRes = await api.get(`/appointment?patient_id=${patientIdToFetch}`);
    
    visits.value = apptRes.data.filter(a => a.status === 'Completed').sort((a, b) => new Date(b.date) - new Date(a.date));
    
  } catch (err) {
    console.error(err);
    error.value = "Failed to load medical history.";
  } finally {
    loading.value = false;
  }
};

const viewDetails = (visit) => {
  selectedVisit.value = visit;
};

const closeDetails = () => {
  selectedVisit.value = null;
};

const statusBadgeClass = (status) => {
    switch(status) {
        case 'Completed': return 'badge bg-success';
        case 'Cancelled': return 'badge bg-danger';
        default: return 'badge bg-primary';
    }
};

onMounted(() => {
  fetchHistory();
});

const exportToCSV = () => {
  if (visits.value.length === 0) return;

  
  const headers = ['Date', 'Doctor', 'Department', 'Diagnosis', 'Tests', 'Medicines', 'Notes'];
  
  
  const rows = visits.value.map(visit => {
    const doctorName = visit.doctor && visit.doctor.user ? visit.doctor.user.name : 'Unknown';
    const department = visit.doctor && visit.doctor.department ? visit.doctor.department.name : 'N/A';
    const diagnosis = visit.treatment ? visit.treatment.diagnosis : '';
    const tests = visit.treatment ? visit.treatment.tests : '';
    const medicines = visit.treatment ? visit.treatment.medicines : '';
    const notes = visit.treatment ? visit.treatment.notes : '';
    
    
    const escape = (field) => {
      if (field === null || field === undefined) return '';
      const stringField = String(field);
      if (stringField.includes(',') || stringField.includes('"') || stringField.includes('\n')) {
        return `"${stringField.replace(/"/g, '""')}"`;
      }
      return stringField;
    };

    return [
      escape(visit.date),
      escape(doctorName),
      escape(department),
      escape(diagnosis),
      escape(tests),
      escape(medicines),
      escape(notes)
    ].join(',');
  });

  
  const csvContent = [headers.join(','), ...rows].join('\n');

  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', `medical_history_${new Date().toISOString().split('T')[0]}.csv`);
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
</script>

<style scoped>
.ls-1 {
  letter-spacing: 1px;
}
</style>
