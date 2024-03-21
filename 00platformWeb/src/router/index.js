import { createRouter, createWebHashHistory } from "vue-router"
import Statistisc from '~/pages/statistics/statistics.vue' // 此处~在 vite.config.js中定义
import About from '~/pages/about.vue' // 对象的方式 首字母一定要大写
import NotFound from '~/pages/404.vue'
import Login from '~/pages/login.vue'
import Home from '~/layouts/home.vue'
import ServerError from "~/pages/serverError.vue";
import UserList from '~/pages/users/userList.vue'
import ApiProjectList from "~/pages/api_test/apiProjectList.vue";
import ApiProjectForm from "~/pages/api_test/apiProjectForm.vue";
import ApiModuleForm from "~/pages/api_test/apiModuleForm.vue";
import ApiModuleList from "~/pages/api_test/apiModuleList.vue";
import ApiInfoList from "~/pages/api_test/apiInfoList.vue";
import ApiInfoForm from "~/pages/api_test/apiInfoForm.vue";
import ApiCollectionList from "~/pages/api_test/apiCollectionList.vue";
import ApiCollectionForm from "~/pages/api_test/apiCollectionForm.vue";
import service from "~/axios";


// 用于管理当前页面的所有路由
const routes = [
  {
    path: '/',
    redirect: '/login'
  }, {
    path: "/login",
    component: Login 
  },
  {
    path: "/serverErr",
    component: ServerError 
  },
  {
    path: '/home',
    component: Home,
    children: [
      {
        path: '/',
        component: Statistisc,
        meta: {
          title: '后台首页',
          requiresAuth: true
        }
      },
      {
        path: '/Users',
        component: UserList,
        meta: {
          title: '用户列表页',
          requiresAuth: true
        }
      },
      {
        path: '/ApiProjectList',
        component: ApiProjectList,
        meta: {
          title: '项目列表',
          requiresAuth: true
        }
      },{
        path: "/ApiProjectForm",
        component: ApiProjectForm,
        meta: {
            title: "项目操作",
            requiresAuth: true
        }
    }, {
        path: "/ApiModuleList",
        component: ApiModuleList,
        meta: {
            title: "模块列表",
            requiresAuth: true
        }
    }, {
        path: "/ApiModuleForm",
        component: ApiModuleForm,
        meta: {
            title: "模块操作",
            requiresAuth: true
        }
    }, {
        path: "/ApiInfoList",
        component: ApiInfoList,
        meta: {
            title: "接口信息维护",
            requiresAuth: true
        }
    }, {
        path: "/ApiInfoForm",
        component: ApiInfoForm,
        meta: {
            title: "接口信息编辑",
            requiresAuth: true
        }
    }, {
        path: "/ApiCollectionList",
        component: ApiCollectionList,
        meta: {
            title: "测试集合套件",
            requiresAuth: true
        }
    }, {
        path: "/ApiCollectionForm",
        component: ApiCollectionForm,
        meta: {
            title: "测试集合套件操作",
            requiresAuth: false
        }
    }, {
      path: '/about',
      component: About
    },
    ]
  },
  // 最后匹配不到的 都返回 404 !!!
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  },
]

const router = createRouter({
  // 4. 内部提供了 history 模式的实现。为了简单起见，我们在这里使用 hash 模式。
  history: createWebHashHistory(),
  routes, // `routes: routes` 的缩写
})
//导航判断逻辑
router.beforeEach((to, from, next) => {
  // 检查路由是否需要身份验证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查用户是否已经登录
    const token = localStorage.getItem('ct-token')
    if (!token) {
      next('/login');
    }
    else {
      service.defaults.headers.common['Authorization'] = token;
      next();
    }
  }
  else {
    next();
  }
})


export default router;