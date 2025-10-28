import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:6969",
        changeOrigin: true,
        secure: false,
        // ❌ removed rewrite — it was stripping `/api`
        // ✅ now requests to /api/... are passed directly to Flask
      },
    },
  },
});
