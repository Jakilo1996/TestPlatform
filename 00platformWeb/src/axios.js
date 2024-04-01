import axios from 'axios'
import { ref, reactive } from "vue";
import { ElLoading, ElMessage, ElNotification } from 'element-plus'
import router from '~/router/index'

const service = axios.create({
  // baseURL: "http://127.0.0.1:5000", // 本地配置
  // baseURL: "http:/47.109.47.162:80/", // 测试版本配置,记得末尾要加/
})
// 请求拦截器
// 响应拦截器
service.interceptors.response.use(response => {
  // 对响应数据做些什么
  console.log(response.data)
  if (response.status === 201) {
    // 如果响应中包含一个 redirect，清除本地localStorage 中的ct-token
    localStorage.removeItem('ct-token');
    console.log("clean ct-token");
    // 跟随重定向
    // router.push('/login');
  }
  else {
    if (response.data.msg != null) {
      ElNotification({
        title: response.data.msg,
        type: 'success',
        duration: 1000
      })
      return response;
    }
  }
}, error => {
  if (error.code === "ERR_NETWORK") {
    // ERR_NETWORK，则重定向到登录页面
    router.push('/serverErr');
  }
  // 对响应错误做些什么
  console.log(error.status)
  console.log(error)
  return Promise.reject(error);
}
);
export default service;