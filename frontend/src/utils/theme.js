// Theme management utility
export const theme = {
  current: 'light',
  
  init() {
    const saved = localStorage.getItem('theme') || 'light'
    this.setTheme(saved)
  },
  
  setTheme(mode) {
    this.current = mode
    localStorage.setItem('theme', mode)
    document.documentElement.setAttribute('data-theme', mode)
  },
  
  toggle() {
    const newTheme = this.current === 'light' ? 'dark' : 'light'
    this.setTheme(newTheme)
    return newTheme
  },
  
  isDark() {
    return this.current === 'dark'
  }
}

