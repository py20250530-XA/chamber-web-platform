/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./*.html', './app.js'],
  theme: {
    extend: {
      colors: { navy: '#0d3d6e', ocean: '#12558f', bright: '#1770b8', gold: '#c8a15a', paper: '#f6f6f4', ink: '#243649', muted: '#67788a' },
      fontFamily: { sans: ['Inter', 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', 'sans-serif'] },
      boxShadow: { soft: '0 12px 40px rgba(13,61,110,.07)' }
    }
  },
  plugins: []
};
