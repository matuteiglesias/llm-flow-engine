module.exports = {
    content: [
      "./src/**/*.{js,ts,jsx,tsx}", // Make sure Tailwind scans your components
    ],
    theme: {
      extend: {},
    },
    plugins: [require("@tailwindcss/forms")],
  }
  