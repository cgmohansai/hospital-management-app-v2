<template>
  <div class="container mt-4">
    <div class="mb-4">
      <h2 v-if="user.role === 'admin'">Welcome Admin</h2>
      <h2 v-else-if="user.role === 'doctor'">Welcome Dr. {{ user.name }}</h2>
      <h2 v-else>Welcome {{ user.name }}</h2>
    </div>

    <!-- admin dashboard -->
    <div v-if="user.role === 'admin'" class="row">
      <div class="col-md-4">
        <div class="card text-white bg-primary mb-3">
          <div class="card-header">Manage Patients</div>
          <div class="card-body">
            <p class="card-text">View, add, edit, and delete patients.</p>
            <router-link to="/patients" class="btn btn-light">Go to Patients</router-link>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-white bg-success mb-3">
          <div class="card-header">Manage Doctors</div>
          <div class="card-body">
            <p class="card-text">Approve and manage doctors.</p>
            <router-link to="/doctors" class="btn btn-light">Go to Doctors</router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- doctor dashboard -->
    <div v-if="user.role === 'doctor'" class="row">
      <div class="col-md-6">
        <div class="card text-white bg-primary mb-3">
          <div class="card-header">My Patients</div>
          <div class="card-body">
            <p class="card-text">View your patients.</p>
            <router-link to="/patients" class="btn btn-light">View Patients</router-link>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card text-white bg-warning mb-3">
          <div class="card-header">Appointments</div>
          <div class="card-body">
            <p class="card-text">Manage your appointments.</p>
            <router-link to="/appointments" class="btn btn-light">View Appointments</router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- patient dashboard -->
    <div v-if="user.role === 'patient'" class="row">
      <div class="col-md-6">
        <div class="card text-white bg-info mb-3">
          <div class="card-header">My Profile</div>
          <div class="card-body">
            <p class="card-text">View and edit your profile.</p>
            <!-- <router-link to="/profile" class="btn btn-light">Go to Profile</router-link> -->
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card text-white bg-success mb-3">
          <div class="card-header">Book Appointment</div>
          <div class="card-body">
            <p class="card-text">Book a new appointment with a doctor.</p>
            <router-link to="/appointments" class="btn btn-light">Book Now</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const user = computed(() => {
    const userData = JSON.parse(localStorage.getItem('user'));
    return {
        name: userData ? userData.name : 'User',
        role: userData && userData.roles && userData.roles.length > 0 ? userData.roles[0] : 'guest'
    };
});
</script>
