import { createApp } from 'vue'
// import './style.css' 注释掉自带的 css 内容，不然会和其他样式冲突
import App from './App.vue'
import ElememtPlus from "element-plus" //导入 element-plusui
import 'element-plus/dist/index.css' 
import router from './router'
import 'virtual:windi.css'

const  app = createApp(App)
app.use(ElememtPlus) //使用 element-plus
app.use(router) //使用定义的 router

 // 如果您正在使用CDN引入，请删除下面一行。 挂载所有的图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.mount('#app')
// createApp(App).mount('#app')
// 创建一个 app 对象 ，挂载到 id 名叫 app 的标签下面

 