<template>
    <div class="f-menu">
        <el-menu default-active="2" class="el-menu-vertical-demo" @select="handleSelect">
            <template v-for="(item, index ) in asideMenus" :key="index">
                <el-sub-menu v-if="item.child && item.child.length > 0" :index="item.name">
                    <template #title>
                        <el-icon>
                            <component :is="item.icon"></component>
                        </el-icon>
                        <span>{{ item.name }}</span>
                    </template>
                    <el-menu-item v-for="(item2, index2) in item.child" :key="index2" :index="item2.frontpath">
                        <el-icon>
                            <component :is="item2.icon"></component>
                        </el-icon>
                        <span>{{ item2.name }}</span>
                    </el-menu-item>
                </el-sub-menu>
                <el-menu-item v-else :index="item.frontpath">
                    <el-icon>
                        <component :is="item.icon"></component>
                    </el-icon>
                    <span>{{ item.name }}</span>

                </el-menu-item>
            </template>
        </el-menu>
    </div>
</template>
<script setup>
import { useRouter } from 'vue-router'
const router = useRouter();
const handleSelect = (e) => {
    // console.log(e);
    router.push(e); //直接通过路由跳转
}
const asideMenus = [
{
        'name': '首页',
        'icon': 'HomeFilled',
        'frontpath': '/home',
    },
    {
        'name': '测试环境',
        'icon': 'Tools',
        'child': [
            {
                'name': '公共接口参数',
                'icon': 'Notification',
                'frontpath': '/about',
            }
        ]
    }, {
        'name': '接口自动测试',
        'icon': 'Expand',
        'frontpath': '/ApiProjectList',
        'child':[
            {
                "name":"API 项目管理",
                'icon': 'Position',
                "frontpath":"/ApiProjectList"
            },
            {
                "name":"API 模块管理",
                'icon': 'Connection',
                "frontpath":"/ApiModuleList"
            },
            {
                "name":"API 信息维护",
                'icon': 'Filter',
                "frontpath":"/ApiInfoList"
            },
            {
                "name":"API 测试集合列表",
                'icon': 'Link',
                "frontpath":"/ApiCollectionList"
            }
        ]
    },
    {
        'name': 'App自动测试',
        'icon': 'Iphone',
        'frontpath': '/about',
        'child':[
            {
                "name":"App 项目管理",
                'icon': 'Cellphone',
                "frontpath":"/about"
            },
            {
                "name":"App 模块管理",
                'icon': 'VideoPlay',
                "frontpath":"/about"
            },
            {
                "name":"App 测试信息维护",
                'icon': 'Film',
                "frontpath":"/about"
            },
            {
                "name":"App 测试集合列表",
                'icon': 'Camera',
                "frontpath":"/about"
            }
        ]
    },{
        'name': 'Web自动测试',
        'icon': 'ChromeFilled',
        'frontpath': '/about',
        'child':[
            {
                'icon': 'Edit',
                "name":"Web项目管理",
                "frontpath":"/about"
            },
            {
                'icon': 'Platform',
                "name":"Web模块管理",
                "frontpath":"/about"
            },
            {
                'icon': 'PictureFilled',
                "name":"Web测试信息维护",
                "frontpath":"/about"
            },
            {
                'icon': 'PictureRounded',
                "name":"Web测试集合列表",
                "frontpath":"/about"
            }
        ]
    },{
        'name': '测试报告',
        'icon': 'Document',
        'child': [
            {
                'name': '测试报告',
                'icon': 'CopyDocument',
                'frontpath': '/about',
            },
            {
                'name': '测试日志',
                'icon': 'Reading',
                'frontpath': '/about',
            }
        ]
    },
    {
        'name': '系统日志',
        'icon': 'SetUp',
        'child': [
            {
                'name': '系统日志',
                'icon': 'DocumentChecked',
                'frontpath': '/about',
            }
        ]
    },
    {
        'name': '系统管理',
        'icon': 'Setting',
        'child': [
            {
                'name': '用户管理',
                'icon': 'User',
                'frontpath': '/Users',
            }
        ]
    },  
]

</script>

<!--01 bottom 表示到底部的距离，其他同理，shadow表示阴影 ，fixed表示滚动时自己不动 overflow: auto;长度问题可以自动滚动-->

<style>
.f-menu {
    width: 250px;
    top: 64px;
    bottom: 0;
    left: 0;
    overflow: auto;
    @apply shadow-md fixed bg-light-50;
}
</style>