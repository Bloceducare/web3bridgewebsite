module.exports = {
  darkMode: 'class',
  content: ['./src/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  theme: {
    screens: {
      sm: '480px',
      md: '768px',
      lg: '976px',
      xl: '1440px',
    },
    colors: {
      primary: '#FA0101',
      base: '#111111',
      base90: '#151515',
      white: '#ffffff',
      white10: '#D0D0D0',
      white60: '#737373',
      white50: '#A1A1A1',
      background10: '#E5E5E5',
    },
    fontFamily: {
      primary: ['DM Sans', 'sans-serif'],
      secondary: ['Poppins', 'sans-serif'],
    },
    extend: {},
  },
  plugins: [],
}
