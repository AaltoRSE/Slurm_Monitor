import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import dotenv from "dotenv";
import { dirname, basename } from "node:path";

// Load environment variables from .env file
dotenv.config();

const currentDir = dirname(fileURLToPath(import.meta.url)); // Current directory
const parentDir = basename(dirname(currentDir)); // Parent's parent directory

process.env.VITE_BASE_URL =
  process.env.VITE_BASE_URL || `/pun/dev/${parentDir}`;

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
