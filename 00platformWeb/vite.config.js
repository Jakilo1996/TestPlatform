import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import WindiCss from 'vite-plugin-windicss'


// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias:{
      "~": path.resolve(__dirname,"src") //到 src 下所有的文件都是对应的 path  ~
    }
  },
  plugins: [
    vue(),
    WindiCss()], //css 样式框架
})