import { defineConfig } from 'vite';
export default {
  build: {
    sourcemap: true,
    outDir: '../docs'
  },
  server: {
    host: true,
    port: 3000
  }
}
