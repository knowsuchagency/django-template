import path from "path"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  // Always use /static/ for consistency
  base: '/static/',
  build: {
    manifest: true,
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, "src/main.tsx"),
      },
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/accounts": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/_allauth": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/admin": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  appType: 'spa',
})
