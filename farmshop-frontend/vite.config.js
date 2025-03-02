import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'  // ✅ Import nécessaire pour configurer l'alias

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),  // ✅ Alias `@` pointe vers `src/`
    },
  },
})
