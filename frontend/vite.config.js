import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    cors: true, // 允许跨域
    proxy: {
      '/api': {
        target: 'http://192.168.119.129:8002', // 使用局域网 IP
        changeOrigin: true
      }
    }
  },
  // 优化依赖预构建配置
  optimizeDeps: {
    include: ['vue', 'vue-router', 'element-plus', '@element-plus/icons-vue', 'axios']
  }
})
