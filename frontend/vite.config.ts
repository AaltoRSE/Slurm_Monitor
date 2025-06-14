import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import dotenv from "dotenv";

// Load environment variables from .env file
dotenv.config();

process.env.VITE_BASE_URL = process.env.VITE_BASE_URL || `./`;

// https://vite.dev/config/
export default defineConfig({
  base: process.env.VITE_BASE_URL,
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
});
