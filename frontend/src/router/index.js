import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import Dashboard from '../pages/Dashboard.vue'
import AppointmentList from '../pages/AppointmentList.vue'
import DoctorList from '../pages/DoctorList.vue'
import PatientList from '../pages/PatientList.vue'
import HomePage from '../pages/HomePage.vue'
import DepartmentDetail from '../pages/DepartmentDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/appointments',
    name: 'AppointmentList',
    component: AppointmentList,
    meta: { requiresAuth: true }
  },
  {
    path: '/doctors',
    name: 'DoctorList',
    component: DoctorList,
    meta: { requiresAuth: true }
  },
  {
    path: '/patients',
    name: 'PatientList',
    component: PatientList,
    meta: { requiresAuth: true }
  },
  {
    path: '/department/:name',
    name: 'DepartmentDetail',
    component: DepartmentDetail,
    meta: { requiresAuth: true }
  },
  {
    path: '/doctor/:id',
    name: 'DoctorProfile',
    component: () => import('../pages/DoctorProfile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/doctor/:id/availability',
    name: 'DoctorAvailability',
    component: () => import('../pages/DoctorAvailability.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/history',
    name: 'PatientHistory',
    component: () => import('../pages/PatientHistory.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/patients/:id/history',
    name: 'ViewPatientHistory',
    component: () => import('../pages/PatientHistory.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/consultation/:appointment_id',
    name: 'Consultation',
    component: () => import('../pages/Consultation.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'PatientProfile',
    component: () => import('../pages/PatientProfile.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      }
    }
    return { top: 0 }
  }
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token');

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'Login' });
    } else {
      next();
    }
  } else {
    // Redirect to dashboard if already logged in and trying to access login/register
    if (isAuthenticated && (to.name === 'Login' || to.name === 'Register')) {
      next({ name: 'Dashboard' });
    } else {
      next();
    }
  }
});

export default router
