<template>
     <el-result
        icon="warning"
        title="404页面"
        sub-title="抱歉，您的页面走丢了"
      >
        <template #extra>
          <el-button type="primary" @click="$router.push('/')">回到首页</el-button> <!-- 定义了回到首页的逻辑 -->
        </template>
      </el-result>
</template>