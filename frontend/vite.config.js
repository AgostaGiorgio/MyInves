import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    // Use 'static' instead of the default 'assets' to avoid clashing with the
    // SPA route /assets (Assets page and asset detail).
    assetsDir: 'static',
  },
})
