const { defineConfig } = require('vite');
const vue = require('@vitejs/plugin-vue');
const path = require('path');
const WindiCss = require('vite-plugin-windicss');

// https://vitejs.dev/config/
module.exports = defineConfig({
  type: 'module',  
  resolve: {
    alias: {
      "~": path.resolve(__dirname, "src") //到 src 下所有的文件都是对应的 path  ~
    }
  },
  plugins: [
    vue(),
    WindiCss()
  ], //css 样式框架
  build: {
    target: 'es2018', // 修改为支持的 ES 版本，如 es2018
    polyfillDynamicImport: false,
    outDir: 'dist',
    assetsDir: '.',
    rollupOptions: {
      output: {
        format: 'cjs' // 设置构建的格式为 CommonJS
      }
    }
  }
});
