<template>
  <div class="medical-icons">
    <!-- Heart Icon -->
    <svg v-if="type === 'heart'" class="icon heart-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" 
            :fill="color" 
            :stroke="strokeColor"
            stroke-width="1.5"/>
    </svg>
    
    <!-- Stethoscope Icon -->
    <svg v-if="type === 'stethoscope'" class="icon stethoscope-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M19 10c0 2.76-2.24 5-5 5s-5-2.24-5-5V6c0-1.1.9-2 2-2h6c1.1 0 2 .9 2 2v4z" 
            :fill="color"
            :stroke="strokeColor"
            stroke-width="1.5"/>
      <path d="M14 10c0 1.1-.9 2-2 2s-2-.9-2-2V8h4v2z" :fill="color"/>
      <circle cx="16" cy="18" r="2" :fill="color" :stroke="strokeColor" stroke-width="1.5"/>
      <path d="M14 18h4" :stroke="strokeColor" stroke-width="2" stroke-linecap="round"/>
    </svg>
    
    <!-- Doctor Icon -->
    <svg v-if="type === 'doctor'" class="icon doctor-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="12" cy="8" r="4" :fill="color" :stroke="strokeColor" stroke-width="1.5"/>
      <path d="M6 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2" :stroke="strokeColor" stroke-width="1.5" stroke-linecap="round"/>
      <path d="M12 12v4M10 14h4" :stroke="strokeColor" stroke-width="2" stroke-linecap="round"/>
    </svg>
    
    <!-- Nurse Icon -->
    <svg v-if="type === 'nurse'" class="icon nurse-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="12" cy="8" r="4" :fill="color" :stroke="strokeColor" stroke-width="1.5"/>
      <path d="M6 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2" :stroke="strokeColor" stroke-width="1.5" stroke-linecap="round"/>
      <circle cx="12" cy="12" r="1.5" :fill="strokeColor"/>
    </svg>
    
    <!-- Hospital Icon -->
    <svg v-if="type === 'hospital'" class="icon hospital-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M3 21h18M5 21V7l8-4v18M19 21V11l-6-4" :stroke="strokeColor" stroke-width="2" stroke-linecap="round"/>
      <path d="M9 9v6M6 12h6" :stroke="strokeColor" stroke-width="2" stroke-linecap="round"/>
    </svg>
  </div>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    required: true,
    validator: (value) => ['heart', 'stethoscope', 'doctor', 'nurse', 'hospital'].includes(value)
  },
  color: {
    type: String,
    default: 'currentColor'
  },
  strokeColor: {
    type: String,
    default: 'currentColor'
  }
})
</script>

<style scoped>
.medical-icons {
  display: inline-block;
}

.icon {
  width: 100%;
  height: 100%;
  transition: transform 0.3s ease;
}

.heart-icon {
  animation: heartbeat 2s ease-in-out infinite;
}

@keyframes heartbeat {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.stethoscope-icon:hover,
.doctor-icon:hover,
.nurse-icon:hover,
.hospital-icon:hover {
  transform: scale(1.1);
}
</style>

