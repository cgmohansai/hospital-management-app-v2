<template>
  <div class="home-page">
    <section id="hero" class="hero-section text-white d-flex align-items-center">
      <div class="container text-center text-md-start">
        <div class="row align-items-center">
          <div class="col-md-8">
            <h1 class="display-4 fw-bold mb-3">Life Sync</h1>
            <h2 class="h3 mb-4">Best Multi-Speciality Hospital in Chennai, India</h2>
            <p class="lead mb-4">
              Health is our top priority. Conveniently located in the heart of Avadi, Chennai's prime IT
              and residential hub, we bring together highly experienced doctors, advanced medical technology,
              and a compassionate care team to ensure you receive the right treatment at the right time.
            </p>
            <div class="d-flex gap-3 justify-content-center justify-content-md-start">
              <a href="#directions" class="btn btn-light btn-lg px-4">Directions</a>
              <router-link to="/appointments" class="btn btn-primary btn-lg px-4">
                Book Appointment
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="services" class="py-5 bg-primary bg-opacity-10">
      <div class="container">
        <h2 class="text-center mb-5">Our Services</h2>
        <div class="row g-4">
          <div
            v-for="service in serviceFeatures"
            :key="service.title"
            class="col-md-4 col-lg-2"
          >
            <div class="card h-100 feature-card text-center border-0 shadow-sm">
              <div class="card-body d-flex flex-column align-items-center justify-content-center">
                <i :class="['fs-1', 'text-primary', service.icon]" class="mb-3"></i>
                <h6 class="card-title mb-1">{{ service.title }}</h6>
                <p v-if="service.subtitle" class="card-text small text-muted mb-0">
                  {{ service.subtitle }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="coe" class="py-5">
      <div class="container">
        <div class="row mb-5">
          <div class="col-lg-8 mx-auto text-center">
            <h2 class="mb-3">Center of Excellence</h2>
            <p class="text-muted mb-0">
              At LifeSync, we provide advanced medical services with centres of excellence in Cardiology,
              Orthopedics, Neurology, Gastroenterology, General Surgery, and Critical Care, providing
              comprehensive care under one roof.
            </p>
          </div>
        </div>
        <div class="row g-3">
          <div
            v-for="dept in departments"
            :key="dept"
            class="col-md-6 col-lg-3"
          >
            <div class="card h-100 border-0 shadow-sm hover-shadow">
              <div class="card-body d-flex align-items-center">
                <div class="flex-grow-1">
                  <h6 class="mb-0">{{ dept }}</h6>
                  <router-link :to="`/department/${dept}`" class="small text-decoration-none text-primary stretched-link">
                    View detail
                  </router-link>
                </div>
                <i class="bi bi-chevron-right text-muted"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="stats" class="py-5 bg-danger text-white">
      <div class="container">
        <div class="row text-center g-4">
          <div
            v-for="stat in hospitalStats"
            :key="stat.label"
            class="col-6 col-md-2"
            :class="stat.offsetClass"
          >
            <h3 class="fw-bold">{{ stat.value }}</h3>
            <p class="mb-0">{{ stat.label }}</p>
          </div>
        </div>
      </div>
    </section>

    <section id="facilities" class="py-5 bg-info bg-opacity-10">
      <div class="container">
        <h2 class="text-center mb-5">Facilities</h2>
        <div class="row">
          <div class="col-md-10 mx-auto">
            <div class="row g-3">
              <div
                v-for="facility in facilities"
                :key="facility"
                class="col-md-4 col-6"
              >
                <div class="d-flex align-items-center">
                  <i class="bi bi-check-circle-fill text-success me-2"></i>
                  <span>{{ facility }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="testimonials" class="py-5 bg-danger bg-opacity-10">
      <div class="container">
        <div class="row g-5">
          <div class="col-md-6" v-for="testimonial in testimonials" :key="testimonial.name">
            <h3 class="mb-4">Patient Testimonials</h3>
            <div class="card border-0 shadow-sm bg-light">
              <div class="card-body p-4">
                <p class="fst-italic mb-3">"{{ testimonial.message }}"</p>
                <div class="d-flex align-items-center">
                  <div
                    class="bg-secondary rounded-circle me-3"
                    style="width: 40px; height: 40px;"
                  ></div>
                  <div>
                    <h6 class="mb-0">{{ testimonial.name }}</h6>
                    <small class="text-muted">{{ testimonial.role }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>  
        </div>
      </div>
    </section>

    <section id="faq" class="py-5 bg-light">
      <div class="container">
        <h2 class="text-center mb-5">Frequently Asked Questions</h2>
        <div class="accordion col-md-8 mx-auto" id="faqAccordion">
          <div
            class="accordion-item"
            v-for="(faq, index) in faqs"
            :key="faq.question"
          >
            <h2 class="accordion-header" :id="`heading-${index}`">
              <button
                class="accordion-button collapsed"
                type="button"
                data-bs-toggle="collapse"
                :data-bs-target="`#collapse-${index}`"
                aria-expanded="false"
                :aria-controls="`collapse-${index}`"
              >
                {{ faq.question }}
              </button>
            </h2>
            <div
              :id="`collapse-${index}`"
              class="accordion-collapse collapse"
              :aria-labelledby="`heading-${index}`"
              data-bs-parent="#faqAccordion"
            >
              <div class="accordion-body">
                {{ faq.answer }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../utils/api';

const serviceFeatures = ref([
  { title: 'Experienced Doctors', icon: 'bi-people-fill', subtitle: 'Loading...' },
  { title: 'Family Card', icon: 'bi-card-heading' },
  { title: 'Second Opinion', icon: 'bi-chat-quote-fill' },
  { title: 'Home Health Care', icon: 'bi-house-heart-fill' },
  { title: 'Health Check-ups', icon: 'bi-clipboard-pulse' }
]);

const departments = [
  'Cardiology',
  'Neurology',
  'Orthopedics',
  'Oncology',
  'Gynecology',
  'Pediatrics',
  'General Surgery',
  'General Medicine'
];

const hospitalStats = [
  { label: 'Beds', value: '5500+', offsetClass: 'offset-md-1' },
  { label: 'ICU Beds', value: '1636+' },
  { label: 'Cath Labs', value: '23+' },
  { label: 'Surgeries', value: '100000+' },
  { label: 'Operation Theaters', value: '150+' }
];

const facilities = [
  '400 Beds',
  '250 ICU Beds',
  '20 Operating Rooms',
  '70 Consultation Rooms',
  '200+ Consultants',
  '20 Emergency Beds',
  '24/7 Cathlab',
  '260 Slice CT Scan Machine',
  '2.5 Tesla MRI',
  'Dexa Scan',
  'Sonography',
  'X-Ray'
];

const testimonials = [
  {
    name: 'Ram',
    role: 'Patient',
    message:
      'The care I received at LifeSync was exceptional. The doctors were knowledgeable and the staff was very supportive during my recovery.'
  }
];

const faqs = [
  {
    question: 'How do I book an appointment?',
    answer: 'You can book an appointment online through our website or by calling our helpline.'
  },
  {
    question: 'What insurance plans do you accept?',
    answer: 'We accept a wide range of insurance plans. Please contact our billing department for details.'
  },
  {
    question: 'Do you offer emergency services?',
    answer: 'Yes, we have a 24/7 emergency department equipped to handle all medical emergencies.'
  }
];

onMounted(async () => {
  try {
    const response = await api.get('/doctors');
    serviceFeatures.value[0].subtitle = `${response.data.length}+ Doctors`;
  } catch (err) {
    console.error('Failed to fetch doctor count', err);
    serviceFeatures.value[0].subtitle = '50+ Doctors';
  }
});
</script>

<style scoped>
.hero-section {
  background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('/bg.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  min-height: 600px;
}

.feature-card,
.hover-shadow {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover,
.hover-shadow:hover {
  transform: translateY(-4px);
  box-shadow: 0 .5rem 1rem rgba(0, 0, 0, 0.15) !important;
}
</style>
