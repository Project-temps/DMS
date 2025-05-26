/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./ui/static/templates/dashboard.html',],
  theme: {
    extend: {},
  },
  plugins: [require('flowbite/plugin')],
}

