import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
export default defineConfig({
  plugins: [vue()],
  resolve: { alias: { vue: "vue/dist/vue.esm-bundler.js" } },  // cho phép template dạng chuỗi
  server: { proxy: { "/api": "http://localhost:8000" } },
});
