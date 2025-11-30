// Simple i18n utility
const translations = {
  en: {
    // HomePage
    welcome: 'Welcome to',
    hospitalName: 'MedCare Hospital',
    tagline: 'Your Health, Our Priority',
    getStarted: 'Get Started',
    learnMore: 'Learn More',
    services: 'Our Services',
    about: 'About Us',
    contact: 'Contact',
    features: {
      title: 'Why Choose Us',
      care: '24/7 Care',
      careDesc: 'Round-the-clock medical assistance',
      experts: 'Expert Doctors',
      expertsDesc: 'Experienced medical professionals',
      technology: 'Advanced Technology',
      technologyDesc: 'State-of-the-art medical equipment',
      support: 'Patient Support',
      supportDesc: 'Comprehensive care and support'
    },
    // Auth
    login: 'Login',
    signup: 'Sign Up',
    logout: 'Logout',
    username: 'Username',
    email: 'Email',
    password: 'Password',
    confirmPassword: 'Confirm Password',
    name: 'Full Name',
    phone: 'Phone Number',
    role: 'Role',
    rolePatient: 'Patient',
    roleDoctor: 'Doctor',
    doctorApprovalNote: 'Note: Doctor accounts require admin approval before activation.',
    rememberMe: 'Remember Me',
    forgotPassword: 'Forgot Password?',
    haveAccount: 'Already have an account?',
    noAccount: "Don't have an account?",
    createAccount: 'Create Account',
    signIn: 'Sign In',
    // Common
    home: 'Home',
    language: 'Language',
    theme: 'Theme'
  },
  es: {
    welcome: 'Bienvenido a',
    hospitalName: 'Hospital MedCare',
    tagline: 'Tu Salud, Nuestra Prioridad',
    getStarted: 'Comenzar',
    learnMore: 'Saber Más',
    services: 'Nuestros Servicios',
    about: 'Acerca de',
    contact: 'Contacto',
    features: {
      title: 'Por Qué Elegirnos',
      care: 'Atención 24/7',
      careDesc: 'Asistencia médica las 24 horas',
      experts: 'Doctores Expertos',
      expertsDesc: 'Profesionales médicos experimentados',
      technology: 'Tecnología Avanzada',
      technologyDesc: 'Equipamiento médico de última generación',
      support: 'Apoyo al Paciente',
      supportDesc: 'Atención y apoyo integral'
    },
    login: 'Iniciar Sesión',
    signup: 'Registrarse',
    logout: 'Cerrar Sesión',
    username: 'Nombre de Usuario',
    email: 'Correo Electrónico',
    password: 'Contraseña',
    confirmPassword: 'Confirmar Contraseña',
    name: 'Nombre Completo',
    phone: 'Número de Teléfono',
    role: 'Rol',
    rolePatient: 'Paciente',
    roleDoctor: 'Doctor',
    doctorApprovalNote: 'Nota: Las cuentas de doctor requieren aprobación del administrador antes de la activación.',
    rememberMe: 'Recordarme',
    forgotPassword: '¿Olvidaste tu contraseña?',
    haveAccount: '¿Ya tienes una cuenta?',
    noAccount: '¿No tienes una cuenta?',
    createAccount: 'Crear Cuenta',
    signIn: 'Iniciar Sesión',
    home: 'Inicio',
    language: 'Idioma',
    theme: 'Tema'
  },
  fr: {
    welcome: 'Bienvenue à',
    hospitalName: 'Hôpital MedCare',
    tagline: 'Votre Santé, Notre Priorité',
    getStarted: 'Commencer',
    learnMore: 'En Savoir Plus',
    services: 'Nos Services',
    about: 'À Propos',
    contact: 'Contact',
    features: {
      title: 'Pourquoi Nous Choisir',
      care: 'Soins 24/7',
      careDesc: 'Assistance médicale 24h/24',
      experts: 'Médecins Experts',
      expertsDesc: 'Professionnels médicaux expérimentés',
      technology: 'Technologie Avancée',
      technologyDesc: 'Équipement médical de pointe',
      support: 'Soutien aux Patients',
      supportDesc: 'Soins et soutien complets'
    },
    login: 'Connexion',
    signup: "S'inscrire",
    logout: 'Déconnexion',
    username: "Nom d'utilisateur",
    email: 'E-mail',
    password: 'Mot de Passe',
    confirmPassword: 'Confirmer le Mot de Passe',
    name: 'Nom Complet',
    phone: 'Numéro de Téléphone',
    role: 'Rôle',
    rolePatient: 'Patient',
    roleDoctor: 'Médecin',
    doctorApprovalNote: 'Note: Les comptes de médecin nécessitent l\'approbation de l\'administrateur avant l\'activation.',
    rememberMe: 'Se Souvenir de Moi',
    forgotPassword: 'Mot de Passe Oublié?',
    haveAccount: 'Vous avez déjà un compte?',
    noAccount: "Vous n'avez pas de compte?",
    createAccount: 'Créer un Compte',
    signIn: 'Se Connecter',
    home: 'Accueil',
    language: 'Langue',
    theme: 'Thème'
  }
}

export const i18n = {
  current: 'en',
  
  init() {
    const saved = localStorage.getItem('language') || 'en'
    this.setLanguage(saved)
  },
  
  setLanguage(lang) {
    if (translations[lang]) {
      this.current = lang
      localStorage.setItem('language', lang)
      document.documentElement.setAttribute('lang', lang)
    }
  },
  
  t(key) {
    const keys = key.split('.')
    let value = translations[this.current]
    
    for (const k of keys) {
      value = value?.[k]
    }
    
    return value || key
  },
  
  getAvailableLanguages() {
    return Object.keys(translations)
  }
}

