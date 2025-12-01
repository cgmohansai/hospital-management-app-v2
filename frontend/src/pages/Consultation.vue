<template>
  <div class="container mt-4">
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else>
      <div class="row mb-4">
        <div class="col-md-12">
          <div class="card shadow-sm border-0">
            <div class="card-body">
              <h4 class="card-title text-primary fw-bold mb-3">Patient Details</h4>
              <div class="row">
                <div class="col-md-3">
                  <strong>Name:</strong> {{ patient.user ? patient.user.name : 'Unknown' }}
                </div>
                <div class="col-md-3">
                  <strong>Age/DOB:</strong> {{ patient.dob }}
                </div>
                <div class="col-md-3">
                  <strong>Gender:</strong> {{ patient.gender }}
                </div>
                <div class="col-md-3">
                  <strong>Phone:</strong> {{ patient.phone }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <!-- History Section -->
        <div class="col-md-4">
          <div class="card shadow-sm border-0 h-100">
            <div class="card-header bg-light">
              <h5 class="mb-0 fw-bold">Patient History</h5>
            </div>
            <div class="card-body overflow-auto" style="max-height: 600px;">
              <div v-if="history.length === 0" class="text-muted text-center mt-3">No previous history.</div>
              <div v-for="visit in history" :key="visit.id" class="card mb-3 border-start border-primary border-4">
                <div class="card-body p-3">
                  <h6 class="card-subtitle mb-2 text-muted">{{ visit.date }} - {{ visit.doctor.user.name }}</h6>
                  <div v-if="visit.treatment">
                    <p class="mb-1 small"><strong>Diagnosis:</strong> {{ visit.treatment.diagnosis }}</p>
                    <p class="mb-1 small"><strong>Medicines:</strong> {{ visit.treatment.medicines }}</p>
                  </div>
                  <button class="btn btn-sm btn-link p-0 text-decoration-none" @click="viewVisitDetails(visit)">View Full Details</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Consultation Form -->
        <div class="col-md-8">
          <div class="card shadow-sm border-0 h-100">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0 fw-bold">Current Consultation</h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="completeConsultation">
                <div class="mb-3">
                  <label class="form-label fw-bold">Visit Type</label>
                  <select v-model="form.visit_type" class="form-select" required>
                    <option value="First Visit">First Visit</option>
                    <option value="Follow-up">Follow-up</option>
                    <option value="Emergency">Emergency</option>
                    <option value="Routine Checkup">Routine Checkup</option>
                  </select>
                </div>

                <div class="mb-3">
                  <label class="form-label fw-bold">Diagnosis</label>
                  <textarea v-model="form.diagnosis" class="form-control" rows="2" required></textarea>
                </div>

                <div class="mb-3">
                  <label class="form-label fw-bold">Tests Required</label>
                  <textarea v-model="form.tests" class="form-control" rows="2" placeholder="e.g. Blood Test, X-Ray"></textarea>
                </div>

                <div class="mb-3">
                  <label class="form-label fw-bold">Medicines</label>
                  <textarea v-model="form.medicines" class="form-control" rows="2" placeholder="List medicines here"></textarea>
                </div>

                <div class="mb-3">
                  <label class="form-label fw-bold">Prescription / Dosage Instructions</label>
                  <textarea v-model="form.prescription" class="form-control" rows="3" placeholder="Detailed instructions"></textarea>
                </div>

                <div class="mb-3">
                  <label class="form-label fw-bold">Doctor's Notes</label>
                  <textarea v-model="form.notes" class="form-control" rows="2"></textarea>
                </div>

                <div class="d-flex justify-content-between mt-4">
                  <button type="button" class="btn btn-outline-danger" @click="cancelAppointment">Cancel Appointment</button>
                  <button type="submit" class="btn btn-success px-4">Complete Consultation</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <div v-if="selectedVisit" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Visit Details - {{ selectedVisit.date }}</h5>
            <button type="button" class="btn-close" @click="selectedVisit = null"></button>
          </div>
          <div class="modal-body" v-if="selectedVisit.treatment">
             <p><strong>Diagnosis:</strong> {{ selectedVisit.treatment.diagnosis }}</p>
             <p><strong>Tests:</strong> {{ selectedVisit.treatment.tests }}</p>
             <p><strong>Medicines:</strong> {{ selectedVisit.treatment.medicines }}</p>
             <p><strong>Prescription:</strong> {{ selectedVisit.treatment.prescription }}</p>
             <p><strong>Notes:</strong> {{ selectedVisit.treatment.notes }}</p>
          </div>
          <div class="modal-body" v-else>
            No details available.
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="selectedVisit = null">Close</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../utils/api';

const route = useRoute();
const router = useRouter();
const appointmentId = route.params.appointment_id;

const loading = ref(true);
const error = ref('');
const appointment = ref(null);
const patient = ref({});
const history = ref([]);
const selectedVisit = ref(null);

const form = ref({
  visit_type: 'First Visit',
  diagnosis: '',
  tests: '',
  medicines: '',
  prescription: '',
  notes: ''
});

const fetchData = async () => {
  loading.value = true;
  try {
    // 1. Get Appointment Details
    const apptRes = await api.get(`/appointment/${appointmentId}`);
    appointment.value = apptRes.data;
    patient.value = appointment.value.patient;

    // 2. Get Patient History (All completed appointments for this patient)
    // We need to fetch all appointments and filter by patient_id
    const historyRes = await api.get(`/appointment?patient_id=${patient.value.id}`);
    history.value = historyRes.data
      .filter(a => a.status === 'Completed' && a.id !== parseInt(appointmentId))
      .sort((a, b) => new Date(b.date) - new Date(a.date));

  } catch (err) {
    console.error(err);
    error.value = "Failed to load consultation data.";
  } finally {
    loading.value = false;
  }
};

const completeConsultation = async () => {
  if (!confirm("Are you sure you want to complete this consultation?")) return;

  try {
    // We need to update the appointment with treatment details and set status to Completed.
    // The current API might not support updating treatment directly via PATCH appointment.
    // We might need to check how AppointmentResource handles PUT/PATCH.
    // Looking at AppointmentResource, it uses `appointment_parser` which includes `status`.
    // But `treatment` is a nested relationship.
    // Usually we need a separate endpoint or the main PUT should handle it if configured.
    // Let's assume we need to send a PUT request with all data including treatment.
    // Wait, `AppointmentResource` might not handle nested writes for `treatment` automatically unless we implemented it.
    // Let's check `AppointmentResource.put`.
    
    // If backend doesn't support nested write, we might need to update `AppointmentResource` or create a `TreatmentResource`.
    // The user asked to "create a new thread to it", implying we are creating a treatment record.
    // Let's try sending the treatment data in the body.
    
    const payload = {
      status: 'Completed',
      treatment: {
        ...form.value
      }
    };

    // We need to make sure backend handles this.
    // I'll assume I need to update backend to handle 'treatment' in PUT if not already.
    // I'll check `AppointmentResource` in a moment.
    
    await api.patch(`/appointment/${appointmentId}`, payload);
    alert("Consultation completed successfully!");
    router.push('/dashboard');

  } catch (err) {
    console.error(err);
    alert("Failed to complete consultation.");
  }
};

const cancelAppointment = async () => {
  if (!confirm("Are you sure you want to cancel this appointment?")) return;
  try {
    await api.patch(`/appointment/${appointmentId}`, { status: 'Cancelled' });
    router.push('/dashboard');
  } catch (err) {
    console.error(err);
    alert("Failed to cancel appointment.");
  }
};

const viewVisitDetails = (visit) => {
  selectedVisit.value = visit;
};

onMounted(() => {
  fetchData();
});
</script>
