module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
    "./views/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    screens: {
      sm: "480px",
      md: "768px",
      lg: "976px",
      xl: "1440px",
    },
    fontFamily: {
      primary: ["DM Sans", "sans-serif"],
      secondary: ["Poppins", "sans-serif"],
    },
    extend: {
      colors: {
        primary: "#FA0101",
        base: "#111111",
        base90: "#151515",
        white: "#ffffff",
        white10: "#D0D0D0",
        white20: "#CFCFCF",
        white60: "#737373",
        white50: "#A1A1A1",
      },
      boxShadow: {
        "2xl": "0px 4px 48px rgba(32, 51, 160, 0.08)",
      },
      animation: {
        spin: "spin 2s linear infinite",
      },
    },
  },
  plugins: [],
};
