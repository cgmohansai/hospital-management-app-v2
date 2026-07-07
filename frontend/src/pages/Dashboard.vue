<template>
  <div class="container mt-4">
    <div class="mb-4">
      <h2 v-if="isAdmin">Welcome Admin</h2>
      <h2 v-else-if="isDoctor">Welcome Dr. {{ user.name }}</h2>
      <h2 v-else>Welcome {{ user.name }}</h2>
    </div>

    
    <div v-if="isAdmin">
      
      <div class="row mb-4">
        <div class="col-md-4">
          <div class="card text-white bg-primary mb-3 shadow-sm h-100">
            <div class="card-body d-flex flex-column justify-content-center align-items-center">
              <h1 class="display-4 fw-bold">{{ doctors.length }}</h1>
              <p class="card-text fs-5">Registered Doctors</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-success mb-3 shadow-sm h-100">
            <div class="card-body d-flex flex-column justify-content-center align-items-center">
              <h1 class="display-4 fw-bold">{{ patients.length }}</h1>
              <p class="card-text fs-5">Registered Patients</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-warning mb-3 shadow-sm h-100">
            <div class="card-body d-flex flex-column justify-content-center align-items-center">
              <h1 class="display-4 fw-bold">{{ allAppointments.length }}</h1>
              <p class="card-text fs-5">Total Appointments</p>
            </div>
          </div>
        </div>
      </div>

      
      <div class="card shadow-sm border-0">
        <div class="card-header bg-white py-3">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <ul class="nav nav-pills card-header-pills">
              <li class="nav-item">
                <a class="nav-link" :class="{ active: activeAdminTab === 'doctors' }" href="#" @click.prevent="activeAdminTab = 'doctors'">Doctors</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" :class="{ active: activeAdminTab === 'patients' }" href="#" @click.prevent="activeAdminTab = 'patients'">Patients</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" :class="{ active: activeAdminTab === 'appointments' }" href="#" @click.prevent="activeAdminTab = 'appointments'">Appointments</a>
              </li>
            </ul>
            <button v-if="activeAdminTab === 'doctors'" class="btn btn-primary" @click="showAddDoctorModal = true">
              <i class="bi bi-plus-lg"></i> Create Doctor
            </button>
          </div>
          
          
          <div class="input-group">
            <span class="input-group-text bg-light border-end-0"><i class="bi bi-search"></i></span>
            <input type="text" class="form-control border-start-0 ps-0" placeholder="Search by Name, ID, Specialization, Phone..." v-model="searchQuery">
          </div>
        </div>
        <div class="card-body">
          
          
          <div v-if="activeAdminTab === 'doctors'">
            <div class="table-responsive">
              <table class="table table-hover align-middle">
                <thead class="table-light">
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Specialization</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="doc in filteredDoctors" :key="doc.id">
                    <td>{{ doc.id }}</td>
                    <td>{{ doc.user ? doc.user.name : 'N/A' }}</td>
                    <td>{{ doc.specialization }}</td>
                    <td>
                      <span :class="doc.is_active ? 'badge bg-success' : 'badge bg-secondary'">
                        {{ doc.is_active ? 'Active' : 'Blacklisted' }}
                      </span>
                    </td>
                    <td>
                      <button class="btn btn-sm btn-outline-primary me-2" @click="editDoctor(doc)">Edit</button>
                      <button class="btn btn-sm btn-outline-warning me-2" @click="toggleDoctorStatus(doc)">
                        {{ doc.is_active ? 'Blacklist' : 'Activate' }}
                      </button>
                      <button class="btn btn-sm btn-outline-danger" @click="deleteDoctor(doc.id)">Delete</button>
                    </td>
                  </tr>
                </tbody>
              </table>
              <p v-if="filteredDoctors.length === 0" class="text-center text-muted mt-3">No doctors found matching your search.</p>
            </div>
          </div>

          
          <div v-if="activeAdminTab === 'patients'">
            <div class="table-responsive">
              <table class="table table-hover align-middle">
                <thead class="table-light">
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Phone</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="patient in filteredPatients" :key="patient.id">
                    <td>{{ patient.id }}</td>
                    <td>{{ patient.user ? patient.user.name : 'N/A' }}</td>
                    <td>{{ patient.phone }}</td>
                    <td>
                      <span :class="patient.user && patient.user.active ? 'badge bg-success' : 'badge bg-secondary'">
                        {{ patient.user && patient.user.active ? 'Active' : 'Blacklisted' }}
                      </span>
                    </td>
                    <td>
                      <button class="btn btn-sm btn-outline-primary me-2" @click="editPatient(patient)">Edit</button>
                      <button class="btn btn-sm btn-outline-warning me-2" @click="togglePatientStatus(patient)">
                        {{ patient.user && patient.user.active ? 'Blacklist' : 'Activate' }}
                      </button>
                      <button class="btn btn-sm btn-outline-danger" @click="deletePatient(patient.id)">Delete</button>
                    </td>
                  </tr>
                </tbody>
              </table>
              <p v-if="filteredPatients.length === 0" class="text-center text-muted mt-3">No patients found matching your search.</p>
            </div>
          </div>

          
          <div v-if="activeAdminTab === 'appointments'">
            <div class="table-responsive">
              <table class="table table-hover align-middle">
                <thead class="table-light">
                  <tr>
                    <th>ID</th>
                    <th>Date</th>
                    <th>Doctor</th>
                    <th>Patient</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="appt in filteredAppointments" :key="appt.id">
                    <td>{{ appt.id }}</td>
                    <td>{{ appt.date }}</td>
                    <td>{{ appt.doctor && appt.doctor.user ? appt.doctor.user.name : 'N/A' }}</td>
                    <td>{{ appt.patient && appt.patient.user ? appt.patient.user.name : 'N/A' }}</td>
                    <td>
                      <span :class="{
                        'badge bg-warning': appt.status === 'Booked',
                        'badge bg-success': appt.status === 'Completed',
                        'badge bg-danger': appt.status === 'Cancelled'
                      }">{{ appt.status }}</span>
                    </td>
                    <td>
                      <button v-if="appt.patient" class="btn btn-sm btn-outline-info" @click="viewPatientHistory(appt.patient.id)">View History</button>
                      <span v-else class="text-muted">N/A</span>
                    </td>
                  </tr>
                </tbody>
              </table>
              <p v-if="filteredAppointments.length === 0" class="text-center text-muted mt-3">No appointments found matching your search.</p>
            </div>
          </div>

        </div>
      </div>
    </div>

    
    <div v-if="isDoctor" class="row">
      <div class="col-md-12">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-white d-flex justify-content-between align-items-center">
            <ul class="nav nav-pills card-header-pills">
              <li class="nav-item">
                <a class="nav-link" :class="{ active: activeTab === 'appointments' }" href="#" @click.prevent="activeTab = 'appointments'">Upcoming Appointments</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" :class="{ active: activeTab === 'patients' }" href="#" @click.prevent="activeTab = 'patients'">My Patients</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" :class="{ active: activeTab === 'availability' }" href="#" @click.prevent="activeTab = 'availability'">Availability</a>
              </li>
            </ul>
          </div>
          <div class="card-body">
            
            
            <div v-if="activeTab === 'appointments'">
              <div class="table-responsive">
                <table class="table table-hover align-middle">
                  <thead class="table-light">
                    <tr>
                      <th>Sr No</th>
                      <th>Patient Name</th>
                      <th>Date & Time</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(appt, index) in doctorAppointments" :key="appt.id">
                      <td>{{ index + 1 }}</td>
                      <td>{{ appt.patient && appt.patient.user ? appt.patient.user.name : 'Unknown' }}</td>
                      <td>{{ appt.date }} {{ appt.time }}</td>
                      <td>
                        <span :class="statusBadgeClass(appt.status)">{{ appt.status }}</span>
                      </td>
                      <td>
                        <button v-if="appt.status === 'Booked'" class="btn btn-sm btn-primary rounded-pill px-3" @click="startConsultation(appt)">
                          Consult
                        </button>
                        <button v-else class="btn btn-sm btn-outline-secondary rounded-pill px-3" disabled>
                          {{ appt.status }}
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <p v-if="doctorAppointments.length === 0" class="text-center text-muted mt-3">No upcoming appointments.</p>
              </div>
            </div>

            
            <div v-if="activeTab === 'patients'">
               <div class="table-responsive">
                <table class="table table-hover align-middle">
                  <thead class="table-light">
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Gender</th>
                      <th>Phone</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="patient in myPatients" :key="patient.id">
                      <td>{{ patient.id }}</td>
                      <td>{{ patient.user ? patient.user.name : 'Unknown' }}</td>
                      <td>{{ patient.gender }}</td>
                      <td>{{ patient.phone }}</td>
                      <td>
                        <button class="btn btn-sm btn-outline-info rounded-pill px-3" @click="viewPatientHistory(patient.id)">
                          View History
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <p v-if="myPatients.length === 0" class="text-center text-muted mt-3">No patients found.</p>
              </div>
            </div>

            
            <div v-if="activeTab === 'availability'">
              <div class="row">
                <div class="col-md-12">
                  <div class="card shadow-sm border-0">
                    <div class="card-header bg-light">
                      <h6 class="mb-0 fw-bold">My Schedule (Next 7 Days)</h6>
                    </div>
                    <div class="card-body">
                      <div v-if="availabilitySlots.length === 0" class="text-muted text-center">No availability set.</div>
                      <div v-for="day in availabilitySlots" :key="day.date" class="mb-3 border-bottom pb-2">
                        <h6 class="text-primary">{{ day.day_name }} ({{ day.date }})</h6>
                        <div v-if="day.slots.length > 0" class="d-flex flex-wrap gap-2">
                          <span v-for="(slot, idx) in day.slots" :key="idx" 
                                :class="['badge', slot.is_booked ? 'bg-danger' : 'bg-success']">
                            {{ slot.start_time }} - {{ slot.end_time }}
                            {{ slot.is_booked ? '(Booked)' : '(Available)' }}
                          </span>
                        </div>
                        <div v-else class="text-muted small">No slots available.</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>

    
    <div v-if="isPatient" class="row align-items-center">
      <div class="col-md-6 text-center mb-4 mb-md-0">
        <h1 class="display-4 fw-bold text-primary">
          <img src="/logo.jpg" alt="Logo" class="me-2 rounded" height="60">
          LifeSync
        </h1>
        <p class="lead text-muted">Your Health, Our Priority</p>
      </div>
      <div class="col-md-6">
        <div class="card text-white bg-success mb-3 shadow-sm">
          <div class="card-header fw-bold">Book Appointment</div>
          <div class="card-body">
            <p class="card-text">Book a new appointment with a doctor.</p>
            <router-link to="/appointments" class="btn btn-light me-2">My Appointments</router-link>
            <button @click="scrollToDepartments" class="btn btn-outline-light">Book New Appointment</button>
          </div>
        </div>
      </div>
    </div>

    
    <div v-if="!isAdmin && !isDoctor && !isPatient" class="alert alert-warning">
      <p>Debug: Current User Role is "{{ user.role }}". Please contact support.</p>
    </div>

    
    <div v-if="isPatient" class="mt-5 mb-5" ref="departmentsSection">
      <h3 class="mb-4 text-primary border-bottom pb-2">Our Departments</h3>
      <div class="row g-4">
        <div class="col-md-6 col-lg-3" v-for="(dept, index) in departments" :key="index">
          <div class="card h-100 shadow-sm border-0 department-card">
            <div class="card-body text-center">
              <div class="mb-3 text-primary">
                <i class="bi bi-hospital fs-1"></i>
              </div>
              <h5 class="card-title fw-bold">{{ dept }}</h5>
              <div class="d-grid gap-2 mt-4">
                <router-link :to="`/department/${dept}`" class="btn btn-outline-primary btn-sm rounded-pill">View Details</router-link>
                <router-link :to="{ path: '/department/' + dept, hash: '#specialists' }" class="btn btn-primary btn-sm rounded-pill">View Doctors</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    
    
    <div v-if="showAddDoctorModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add New Doctor</h5>
            <button type="button" class="btn-close" @click="showAddDoctorModal = false"></button>
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

    
    <div v-if="showEditDoctorModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Doctor</h5>
            <button type="button" class="btn-close" @click="showEditDoctorModal = false"></button>
          </div>
          <div class="modal-body">
             <form @submit.prevent="updateDoctor">
                <div class="mb-3">
                    <label class="form-label">Name</label>
                    <input type="text" class="form-control" v-model="currentDoctor.name" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input type="email" class="form-control" v-model="currentDoctor.email" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Phone</label>
                    <input type="text" class="form-control" v-model="currentDoctor.phone" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Username</label>
                    <input type="text" class="form-control" v-model="currentDoctor.username" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">New Password (leave blank to keep current)</label>
                    <input type="password" class="form-control" v-model="currentDoctor.password">
                </div>
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

    
    <div v-if="showEditPatientModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Patient</h5>
            <button type="button" class="btn-close" @click="showEditPatientModal = false"></button>
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
import { computed, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../utils/api';

const router = useRouter();
const doctorAppointments = ref([]);
const activeTab = ref('appointments');

const activeAdminTab = ref('doctors');
const doctors = ref([]);
const patients = ref([]);
const allAppointments = ref([]);
const showAddDoctorModal = ref(false);
const showEditDoctorModal = ref(false);
const showEditPatientModal = ref(false);
const searchQuery = ref('');

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
const currentDoctor = ref({});
const currentPatient = ref({});

const filteredDoctors = computed(() => {
  if (!searchQuery.value) return doctors.value;
  const query = searchQuery.value.toLowerCase();
  return doctors.value.filter(doc => {
    const name = doc.user && doc.user.name ? doc.user.name.toLowerCase() : '';
    const specialization = doc.specialization ? doc.specialization.toLowerCase() : '';
    const phone = doc.phone ? doc.phone.toLowerCase() : '';
    const email = doc.user && doc.user.email ? doc.user.email.toLowerCase() : '';
    const id = doc.id.toString();
    return name.includes(query) || specialization.includes(query) || phone.includes(query) || email.includes(query) || id.includes(query);
  });
});

const filteredPatients = computed(() => {
  if (!searchQuery.value) return patients.value;
  const query = searchQuery.value.toLowerCase();
  return patients.value.filter(p => {
    const name = p.user && p.user.name ? p.user.name.toLowerCase() : '';
    const email = p.user && p.user.email ? p.user.email.toLowerCase() : '';
    const phone = p.phone ? p.phone.toLowerCase() : '';
    const id = p.id.toString();
    const dob = p.dob ? p.dob.toLowerCase() : '';
    const gender = p.gender ? p.gender.toLowerCase() : '';
    return name.includes(query) || email.includes(query) || phone.includes(query) || id.includes(query) || dob.includes(query) || gender.includes(query);
  });
});

const filteredAppointments = computed(() => {
  if (!searchQuery.value) return allAppointments.value;
  const query = searchQuery.value.toLowerCase();
  return allAppointments.value.filter(appt => {
    const patientName = appt.patient && appt.patient.user ? appt.patient.user.name.toLowerCase() : '';
    const doctorName = appt.doctor && appt.doctor.user ? appt.doctor.user.name.toLowerCase() : '';
    const status = appt.status ? appt.status.toLowerCase() : '';
    const date = appt.date ? appt.date.toLowerCase() : '';
    const id = appt.id.toString();
    return patientName.includes(query) || doctorName.includes(query) || status.includes(query) || date.includes(query) || id.includes(query);
  });
});

const user = computed(() => {
    try {
        const userData = JSON.parse(localStorage.getItem('user'));
        return {
            id: userData ? userData.id : null,
            name: userData ? userData.name : 'User',
            role: userData && userData.roles && userData.roles.length > 0 ? userData.roles[0] : 'guest'
        };
    } catch (e) {
        console.error("Error parsing user data", e);
        return { id: null, name: 'User', role: 'guest' };
    }
});

const isAdmin = computed(() => user.value.role && user.value.role.toLowerCase() === 'admin');
const isDoctor = computed(() => user.value.role && user.value.role.toLowerCase() === 'doctor');
const isPatient = computed(() => user.value.role && user.value.role.toLowerCase() === 'patient');

const myPatients = computed(() => {
  const patientsMap = new Map();
  doctorAppointments.value.forEach(appt => {
    if (appt.patient) {
      patientsMap.set(appt.patient.id, appt.patient);
    }
  });
  return Array.from(patientsMap.values());
});

const departments = [
  'Cardiology', 'Neurology', 'Orthopedics', 'Oncology',
  'Gynecology', 'Pediatrics', 'General Surgery', 'General Medicine'
];

const departmentsSection = ref(null);

const scrollToDepartments = () => {
  if (departmentsSection.value) {
    departmentsSection.value.scrollIntoView({ behavior: 'smooth' });
  }
};

const fetchDoctorAppointments = async () => {
  if (user.value.role === 'doctor') {
    try {
      const doctorsRes = await api.get('/doctors');
      const myDoctor = doctorsRes.data.find(d => d.user && d.user.id === user.value.id);
      
      if (myDoctor) {
        const apptRes = await api.get(`/appointment?doctor_id=${myDoctor.id}`);
        doctorAppointments.value = apptRes.data.sort((a, b) => new Date(a.date) - new Date(b.date));
      }
    } catch (err) {
      console.error("Failed to fetch appointments", err);
    }
  }
};

const fetchAdminData = async () => {
  if (user.value.role === 'admin') {
    try {
      const [docsRes, patientsRes, apptsRes] = await Promise.all([
        api.get('/doctors'),
        api.get('/patients'),
        api.get('/appointment')
      ]);
      doctors.value = docsRes.data;
      patients.value = patientsRes.data;
      allAppointments.value = apptsRes.data.sort((a, b) => new Date(b.date) - new Date(a.date));
    } catch (err) {
      console.error("Failed to fetch admin data", err);
    }
  }
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
        
        await api.post('/doctors', {
            user_id: newUserId,
            specialization: newDoctor.value.specialization,
            bio: newDoctor.value.bio,
            is_active: true
        });
        
        showAddDoctorModal.value = false;
        newDoctor.value = { username: '', email: '', name: '', password: '', phone: '', specialization: '', bio: '', role: 'doctor' };
        fetchAdminData();
        alert('Doctor added successfully');
    } catch (err) {
        console.error(err);
        alert('Failed to add doctor');
    }
};

const editDoctor = (doc) => {
    currentDoctor.value = { 
        id: doc.id,
        specialization: doc.specialization,
        bio: doc.bio,
        
        name: doc.user ? doc.user.name : '',
        email: doc.user ? doc.user.email : '',
        phone: doc.user ? doc.user.phone : '', 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        username: doc.user ? doc.user.username : '',
        password: ''
    };
    
    
    
    if (doc.phone) currentDoctor.value.phone = doc.phone;
    showEditDoctorModal.value = true;
};

const updateDoctor = async () => {
    try {
        const payload = {
            specialization: currentDoctor.value.specialization,
            bio: currentDoctor.value.bio,
            name: currentDoctor.value.name,
            email: currentDoctor.value.email,
            username: currentDoctor.value.username,
            
        };
        if (currentDoctor.value.password) {
            payload.password = currentDoctor.value.password;
        }
        
        if (currentDoctor.value.phone) {
            payload.phone = currentDoctor.value.phone;
        }

        await api.patch(`/doctors/${currentDoctor.value.id}`, payload);
        showEditDoctorModal.value = false;
        fetchAdminData();
        alert('Doctor updated successfully');
    } catch (err) {
        console.error(err);
        alert('Failed to update doctor');
    }
};

const toggleDoctorStatus = async (doc) => {
    if(!confirm(`Are you sure you want to ${doc.is_active ? 'blacklist' : 'activate'} this doctor?`)) return;
    try {
        await api.patch(`/doctors/${doc.id}`, { is_active: !doc.is_active });
        fetchAdminData();
    } catch (err) {
        console.error(err);
        alert('Failed to update doctor status');
    }
};

const deleteDoctor = async (id) => {
    if(!confirm('Are you sure you want to delete this doctor?')) return;
    try {
        await api.delete(`/doctors/${id}`);
        fetchAdminData();
    } catch (err) {
        console.error(err);
        alert('Failed to delete doctor');
    }
};

const editPatient = (patient) => {
    currentPatient.value = { ...patient };
    showEditPatientModal.value = true;
};

const updatePatient = async () => {
    try {
        await api.put(`/patients/${currentPatient.value.id}`, {
             phone: currentPatient.value.phone,
             gender: currentPatient.value.gender,
             dob: currentPatient.value.dob,
             address: currentPatient.value.address,
             user_id: currentPatient.value.user_id
        });
        showEditPatientModal.value = false;
        fetchAdminData();
    } catch (err) {
        console.error(err);
        alert('Failed to update patient');
    }
};

const togglePatientStatus = async (patient) => {
    const isActive = patient.user && patient.user.active;
    if(!confirm(`Are you sure you want to ${isActive ? 'blacklist' : 'activate'} this patient?`)) return;
    try {
        
        await api.patch(`/patients/${patient.id}`, { is_active: !isActive });
        fetchAdminData();
    } catch (err) {
        console.error(err);
        alert('Failed to update patient status');
    }
};

const deletePatient = async (id) => {
    if(!confirm('Are you sure you want to delete this patient?')) return;
    try {
        await api.delete(`/patients/${id}`);
        fetchAdminData();
    } catch (err) {
        console.error(err);
        alert('Failed to delete patient');
    }
};

const startConsultation = (appt) => {
  router.push(`/consultation/${appt.id}`);
};

const viewPatientHistory = (patientId) => {
  router.push(`/patients/${patientId}/history`);
};

const availabilitySlots = ref([]);

const fetchAvailability = async () => {
  if (user.value.role === 'doctor') {
    try {
       const doctorsRes = await api.get('/doctors');
       const myDoctor = doctorsRes.data.find(d => d.user && d.user.id === user.value.id);
       if(myDoctor) {
         const res = await api.get(`/doctors/${myDoctor.id}/availability`);
         availabilitySlots.value = res.data;
       }
    } catch (err) {
      console.error("Failed to fetch availability", err);
    }
  }
};

const statusBadgeClass = (status) => {
    switch(status) {
        case 'Booked': return 'badge bg-primary';
        case 'Completed': return 'badge bg-success';
        case 'Cancelled': return 'badge bg-danger';
        default: return 'badge bg-secondary';
    }
};

onMounted(() => {
  fetchDoctorAppointments();
  fetchAvailability();
  fetchAdminData();
});
</script>
