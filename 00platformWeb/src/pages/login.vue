<template>
    <div>
        <el-row class=" bg-indigo-200">
            <el-col :lg="24" class="flex justify-center">登录页面</el-col>
        </el-row>
    </div>
    <div>
        <el-row class="login-container">
            <!-- min-h-screen 占满整个屏幕-->
            <!-- flex:创建一个弹性区域，用于根据元素自适应大小 -->
            <!--items-center 垂直居中-->
            <!-- justfy--center 水平居中-->
            <!-- flex-col 按行分开-->
            <!-- font-blod 加粗 text-4xl 放大字体 text-light-50 字体颜色 mb-4:间隔-->
            <!-- text-gray-300 调整颜色 space-x-2 左右边距 my-5 与上方间距-->
            <el-col :lg="16" class="left flex-col">
                <div>
                    <div>欢迎光临</div>
                    <div>欢迎来到 jakilo 的测试开发平台</div>
                </div>
            </el-col>
            <el-col :lg="8" class="right">
                <h2>欢迎登录</h2>
                <div>
                    <span class="line"></span>
                    <span>账号密码登录</span>
                    <span class="line"></span>
                </div>
                <el-form ref="formRef" :model="form" class="w-[250px]" :rules="rules">
                    <el-form-item prop="username">
                        <el-input v-model="form.username" placeholder="请输入用户名">
                            <template #prefix> <el-icon class="el-input__icon">
                                    <User />
                                </el-icon> </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="password">
                        <el-input v-model="form.password" type="password" placeholder="请输入密码">
                            <template #prefix> <el-icon class="el-input__icon">
                                    <Lock />
                                </el-icon> </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmit" color='#626aef' class="w-[100px]" round>登录</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ctLogin } from '~/api/ctLogin'
import { ElNotification } from 'element-plus' //提示弹窗
import router from '~/router/index' //导入路由


// import { User, Lock } from '@element-plus/icons-vue'
// do not use same name with ref
const form = reactive({
    username: '',
    password: '',
})

const rules = {
    // 第一步，表单上加上 :rules = rules 表示启用 script 里面的规则，第二个 rules 表示我们自己定义的规则
    // 第二步 在需要校验的组件上 写上 prop =
    // 第三步 定义相关的规则
    username: [
        { required: true, message: '用户名不能为空', trigger: 'blur' },
        { min: 3, max: 15, message: '请输入 3 到 15 位的用户名', trigger: 'blur' },
    ],
    password: [
        { required: true, message: '密码不能为空', trigger: 'blur' },
        { min: 3, max: 15, message: '请输入 3 到 15 位的密码', trigger: 'blur' },
    ]
}

const formRef = ref(null);

const onSubmit = () => {
    // 响应式
    // 回调函数。。。 执行一遍后结果 可以当做参数传递
    formRef.value.validate((vaild) => {  //formRef.value.validate 将进行表单验证，并且接受一个回调函数作为参数，validate会将表单验证的结果vaild（布尔值）作为实参，传递给回调函数的形参vaild,并执行回调函数
        if (!vaild) {
            console.log("未通过表单验证");
            return false; //前端如果不想让代码继续执行，直接 return false
        } else {
            console.log('通过校验');
            //校验通过后，发送请求 axios
            ctLogin(form.username, form.password).then((res) => {
                console.log(res);
                if (res.status == 200 && res.data.data.token != null) {
                    localStorage.setItem('ct-token', res.data.data.token); // 设置  登录成功token
                    router.push("/home"); // 通过路由跳转                    
                } else {
                    ElNotification({
                        title: 'Error',
                        message: '登录失败',
                        type: 'error',
                        position: 'top-right',
                        offset: 100,
                    })
                }
            }).catch((err) => {
                ElNotification({
                    title: '错误',
                    message: '登录出现错误，请联系系统管理员',
                    type: 'error',
                    duration: 2000
                })
                return false
            });

        }
    })
}
</script>

<style>
.login-container {
    @apply min-h-screen bg-indigo-400;
}

.login-container .left,
.login-container .right {
    @apply flex items-center justify-center;
}

.login-container .right {
    @apply bg-indigo-50 flex-col;
}

.left>div>div:first-child {
    @apply font-bold text-4xl text-light-50 mb-4;
}

.left>div>div:last-child {
    @apply text-light-50;
}

.right>h2 {
    @apply font-bold text-3xl text-gray-800 mb-4;
}

.right>div {
    @apply flex items-center justify-center text-gray-300 space-x-2 my-5;
}

.right .line {
    @apply h-[1px] w-16 bg-gray-300;
}
</style>  