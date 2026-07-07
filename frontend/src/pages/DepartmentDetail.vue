<template>
  <div class="department-detail" v-if="department">
    
    <section class="hero-section text-white d-flex align-items-center" :style="{ backgroundImage: `linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('/bg.jpg')` }">
      <div class="container">
        <div class="row">
          <div class="col-12 text-center">
            <h1 class="display-3 fw-bold mb-3">{{ department.title }}</h1>
            <h2 class="h4 mb-4 text-light">{{ department.tagline }}</h2>
            <p class="lead mb-4">{{ department.description }}</p>
          </div>
        </div>
      </div>
    </section>

    
    <section class="py-5">
      <div class="container">
        <div class="row">
          <div class="col-lg-8">
            
            <div class="mb-5">
              <h3 class="mb-4 text-primary">Overview</h3>
              <p class="lead text-muted">{{ department.description }}</p>
              <p>
                Choose LifeSync Hospitals for a team that prioritizes your safety first and offers comprehensive
                {{ department.title }} services.
              </p>
            </div>

            
            <div class="mb-5">
              <h3 class="mb-4 text-primary">Areas of Expertise</h3>
              <div class="row g-4">
                <div class="col-md-6" v-for="(item, index) in department.expertise" :key="index">
                  <div class="d-flex">
                    <div class="flex-shrink-0">
                      <i class="bi bi-check-circle-fill text-success fs-4"></i>
                    </div>
                    <div class="flex-grow-1 ms-3">
                      <h5 class="h6 fw-bold mb-1">{{ item.title }}</h5>
                      <p class="small text-muted mb-0">{{ item.desc }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            
            <div class="mb-5 bg-light p-4 rounded-3">
              <h3 class="mb-4 text-primary">Treatments Offered</h3>
              <div class="row g-2">
                <div class="col-md-6" v-for="treatment in department.treatments" :key="treatment">
                  <div class="d-flex align-items-center">
                    <i class="bi bi-dot fs-3 text-secondary"></i>
                    <span>{{ treatment }}</span>
                  </div>
                </div>
              </div>
            </div>

            
            <div class="mb-5">
              <h3 class="mb-4 text-primary">Our Process</h3>
              <div class="row text-center g-4">
                <div class="col-md-3" v-for="(step, index) in department.process" :key="index">
                  <div class="position-relative">
                    <div class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center mx-auto mb-3" style="width: 60px; height: 60px; font-size: 1.5rem;">
                      {{ index + 1 }}
                    </div>
                    <h6 class="fw-bold">{{ step.title }}</h6>
                    <p class="small text-muted">{{ step.desc }}</p>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </section>

    
    <section id="specialists" class="py-5 bg-light">
      <div class="container">
        <h2 class="text-center mb-5">Get to Know Our Specialists from {{ department ? department.title : departmentName }}</h2>
        
        <div v-if="loadingDoctors" class="text-center">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        
        <div v-else-if="doctors.length === 0" class="text-center text-muted">
          <p>No specialists currently listed for this department.</p>
        </div>

        <div v-else class="row g-4 justify-content-center">
          <div class="col-md-6 col-lg-3" v-for="doc in doctors" :key="doc.id">
            <div class="card h-100 border-0 shadow-sm doctor-card">
              <div class="card-body text-center p-4">
                <div class="mb-3">
                  <div class="bg-secondary rounded-circle mx-auto d-flex align-items-center justify-content-center text-white display-6" style="width: 100px; height: 100px;">
                    {{ doc.user ? doc.user.name.charAt(0) : 'D' }}
                  </div>
                </div>
                <h5 class="card-title mb-1">{{ doc.user ? doc.user.name : 'Doctor' }}</h5>
                <p class="text-primary small mb-2">{{ doc.specialization }}</p>
                <p class="card-text small text-muted mb-3 line-clamp-3">
                  {{ doc.bio || 'Experienced specialist dedicated to patient care.' }}
                </p>
                <div class="d-flex justify-content-center gap-2">
                  <router-link :to="`/doctor/${doc.id}`" class="btn btn-outline-primary btn-sm rounded-pill px-3">View Profile</router-link>
                  <router-link :to="`/doctor/${doc.id}/availability`" class="btn btn-primary btn-sm rounded-pill px-3">Check Availability</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

  </div>
  <div v-else class="container mt-5 text-center">
    <h2>Department Not Found</h2>
    <router-link to="/" class="btn btn-primary mt-3">Go Home</router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { departmentsData } from '../data/departments';
import api from '../utils/api';

const route = useRoute();
const departmentName = computed(() => route.params.name);
const department = computed(() => departmentsData[departmentName.value]);

const doctors = ref([]);
const loadingDoctors = ref(false);

const fetchDoctors = async () => {
  if (!departmentName.value) return;
  
  loadingDoctors.value = true;
  try {
    
    
    const response = await api.get('/doctors');
    const allDoctors = response.data;
    
    
    
    
    
    
    
    
    
    doctors.value = allDoctors.filter(doc => {
       
       
       if (doc.department && doc.department.name === departmentName.value) return true;
       
       
       return false; 
    });
    
    
    
    if (doctors.value.length === 0) {
       doctors.value = allDoctors.filter(doc => {
           const spec = (doc.specialization || '').toLowerCase();
           const dept = departmentName.value.toLowerCase();
           
           if (dept === 'cardiology' && spec.includes('cardio')) return true;
           if (dept === 'neurology' && spec.includes('neuro')) return true;
           if (dept === 'orthopedics' && spec.includes('ortho')) return true;
           if (dept === 'oncology' && spec.includes('onco')) return true;
           if (dept === 'pediatrics' && spec.includes('pediat')) return true;
           if (dept === 'gynecology' && spec.includes('gynec')) return true;
           if (dept === 'general surgery' && spec.includes('surg')) return true;
           if (dept === 'general medicine' && (spec.includes('physician') || spec.includes('medicine'))) return true;
           return false;
       });
    }

  } catch (err) {
    console.error("Failed to fetch doctors", err);
  } finally {
    loadingDoctors.value = false;
  }
};

onMounted(() => {
  fetchDoctors();
  if (route.hash) {
      setTimeout(() => {
        const element = document.getElementById(route.hash.slice(1));
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
    } else {
      window.scrollTo(0, 0);
    }
});

watch(() => route.params.name, (newName) => {
  fetchDoctors();
  window.scrollTo(0, 0);
});

watch(() => route.hash, (newHash) => {
    if (newHash) {
      setTimeout(() => {
        const element = document.getElementById(newHash.slice(1));
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
    }
});
</script>

<style scoped>
.hero-section {
  min-height: 600px;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  position: relative;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.doctor-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.doctor-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 .5rem 1rem rgba(0,0,0,0.15) !important;
}
</style>
