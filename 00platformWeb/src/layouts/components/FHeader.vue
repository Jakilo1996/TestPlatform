<template>
    <div class="f-header">
        <span class="logo">
            <el-icon>
                <Bell />
            </el-icon>
            jakilo的自动测试平台
        </span>
        <el-icon class="icon-btn">
            <Fold />
        </el-icon>
        <el-icon class="icon-btn">
            <Refresh />
        </el-icon>
        <div class="ml-auto flex items-center">
            <el-icon class="icon-btn">
                <FullScreen />
            </el-icon>
            <el-dropdown>
                <span class="el-dropdown-link">
                    <el-avatar :size="25" :src="circleUrl" />
                    <el-icon class="el-dropdown-link">
                        <arrow-down />
                    </el-icon>
                </span>
                <template #dropdown>
                    <div>
                        <el-dropdown-menu class="drop-down">
                            <el-dropdown-item>个人资料</el-dropdown-item>
                            <el-dropdown-item>修改密码</el-dropdown-item>
                            <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
                        </el-dropdown-menu>
                    </div>
                </template>
            </el-dropdown>

        </div>
    </div>
</template>

<script lang="ts" setup>
import { reactive, toRefs } from 'vue'
import { ElMessageBox } from 'element-plus'
import { useRouter } from "vue-router"
import  {ctLogout}  from '~/api/ctLogin'
const state = reactive({
  circleUrl:
    'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
  squareUrl:
    'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png',
  sizeList: ['small', '', 'large'] as const,
})

const { circleUrl, squareUrl, sizeList } = toRefs(state)

const router = useRouter()
function handleLogout() {
  showModal("是否要退出登录？", "warning", "").then((res) => {
    const token = localStorage.getItem('ct-token');
    console.log(token)
    if (!token) {
        console.error('Token is missing');
    }
    else {
        localStorage.removeItem('ct-token');
        ctLogout(token)
    }
    // 跳转回登录页
    router.push("/login");
    // 提示退出登录成功
    // 这里可以添加退出登录成功的提示
  });
}
function showModal(content,type,title){
    return ElMessageBox.confirm(
        content,
        title,
        {
          confirmButtonText: '确认',
          cancelButtonText: '取消',
          type,
        }
      )
}
</script>

<style>
.f-header {
    @apply flex items-center bg-indigo-700 text-light-50 fixed top-0 left-0 right-1;
    height: 64;
}

.logo {
    width: 250px;
    @apply flex justify-center items-center text-xl font-thin font-bold;
}

.icon-btn {
    @apply flex justify-center items-center;
    width: 42px;
    height: 64px;
    cursor: pointer;
}

.icon-btn:hover {
    @apply bg-indigo-600;
}

.f-header .drop-down {
    @apply flex justify-center items-center mx-5;
    height: 64px;
    cursor: pointer;
}</style>