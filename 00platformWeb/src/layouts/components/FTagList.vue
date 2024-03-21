<template>
    <div class="f-tag-list">
        <!--05 修改这两个变量-->
        <!--07 这里处理掉-->
        <el-tabs v-model="activeTab" type="card" class="flex-1" style="min-width: 100px;" @tab-remove="removeTab"
            @tab-change="changeTab" ref="tabsRef">
            <!-- v-for 表示循环，自动生成对应的面板，:closable表示为/的路径不允许屏蔽-->
            <el-tab-pane v-for="item in tabList" :closable="item.path != '/'" :key="item.path" :label="item.title"
                :name="item.path" />
        </el-tabs>
        <span class="'tag-btn'">
            <el-dropdown>
                <span class="el-dropdown-link">
                    <el-icon class="el-icon--right">
                        <arrow-down />
                    </el-icon>
                </span>    
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item @click="removeAllTab">关闭全部</el-dropdown-item>

                       <!-- <el-dropdown-item @click="removeOtherTab">关闭全部</el-dropdown-item>-->
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </span>
    </div>
    <div style="height: 44px;"></div>
</template>

<script setup>
import { ref,onMounted} from 'vue'
import { useRouter,onBeforeRouteUpdate, useRoute } from 'vue-router'
import {setObject,removeObject} from '~/utils/localStrogeOption'
const router= useRouter();
const route = useRoute();


// 定义好当前绑定的数据就是route中的path
const activeTab = ref(route.path)
//  修改js逻辑处理流程 --让它与path挂钩
const tabList = ref([
    {
        title: '首页',
        path: '/home'
    }
])
const tabsRef = ref([]); // 创建一个ref
// 初始化标签导航栏列表
function initTabList(){
    tabList.value = [{
            title: '首页',
            path: '/home'
        }]
    setObject("tabList",tabList.value);
}
initTabList();

function addTab(tab){
    if(!tab.path.endsWith("Form")){
        let noTab =  tabList.value.findIndex(t=>t.path==tab.path) == -1 //判断是不是有这个tab了
        if(noTab){
            //如果noTab为True就表示没有Tab
            tabList.value.push(tab)
        }
        // 使用 $nextTick 确保在 DOM 更新之后执行回调函数
        setObject("tabList",tabList.value)
        // this.$nextTick(() => {
        //     // 获取最新的 DOM 元素并进行操作
        //     const tabsRef = this.$refs.tabsRef;
        //     // 此时 tabsRef 包含了最新的 DOM 元素的引用，可以进行进一步操作
        //     console.log(tabsRef);
        // });       
}
}
onBeforeRouteUpdate((to)=>{
    if(!to.path.endsWith("Form")){
        activeTab.value = to.path
    addTab({
        title:to.meta.title,
        path:to.path
        }) 
    }
})
const removeTab = (t) => {
    let tabs = tabList.value
    let a = activeTab.value
    if(a == t){
        tabs.forEach((tab,index)=>{
            if(tab.path == t){
                const nextTab = tabs[index+1] || tabs[index-1]
                if(nextTab){
                    a = nextTab.path
                }
            }
        })
    }
    activeTab.value = a
    tabList.value = tabList.value.filter(tab=>tab.path != t)
    removeObject("tabList",t)
}
const changeTab = (t) => {
    console.log(t)
    if(!t.endsWith("Form")){
        activeTab.value = t
    try{
        router.push(t)
    }catch(error){
        console.log("发生异常:",error)
    }
}
}
const removeAllTab = () =>{
    initTabList();
    changeTab('/home');
}

// onMounted(() => {
//       // 组件渲染后将tabsRef绑定到el-tabs组件上
//     //   tabsRef.value = Array.from({ length: items.value.length }, (_, index) => `component${index}`);
//        // 获取 el-tabs 实例
//        // Wait for the next tick to ensure all components are rendered
//     // this.$nextTick(() => {
//     //   // Update the refs to bind them to the newly rendered components
//     // this.tabList.forEach(item => {
//     //     const refName = this.getRef(item);
//     //     this.$refs.tabsRef.$children.find(child => child.$el.getAttribute('name') === item.path).$refs[refName] = item;
//     //   });
//     // });
//   }
//     );
// const removeOtherTab = () => {
//     let a = activeTab.value;
//     // 获取el-tabs组件的实例，假设组件的ref为tabsRef
//     console.log(tabsRef);
//     const tabs = this.$refs.tabsRef;
//     const dynamicTabs = tabsInstance.$children;
//     tabs.forEach((t, index) => {
//        if(t.title !=a.title){
//         removeTab(t);
//        }
//     }
//     )
// }

</script>

<style scoped>
.f-tag-list {
    @apply fixed bg-gray-100 flex items-center px-2;
    top: 70px;
    right: 0;
    height: 44px;
    left: 260px;
    z-index: 100;
}

.tag-btn {
    @apply bg-white rounded ml-auto flex items-center justify-center px-2;
    height: 32px;
}

:deep(.el-tabs__header) {
    @apply mb-0;
}

:deep(.el-tabs__nav) {
    border: 0 !important;
}

:deep(.el-tabs__item) {
    border: 0 !important;
    height: 32px;
    line-height: 32px;
    @apply bg-white mx-1 rounded;
}

:deep(.el-tabs__nav-next),
:deep(.el-tabs__nav-prev) {
    line-height: 32px;
    height: 32px;
}

:deep(.is-disabled) {
    cursor: not-allowed;
    @apply text-gray-300;
}</style>