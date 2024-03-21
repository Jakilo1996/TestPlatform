<template>
    <div>
        <h1>开发中，敬请期待</h1>
    </div>
    <div>
        <el-button class="bg-blue-300" @click ="addCount()" >{{count}}</el-button>
        <el-button class="bg-gray-500" @click ="addCount2()" >{{form2.count1}}</el-button>
    </div>
</template>

<script setup>
import { ref ,reactive} from 'vue'
// 可以被响应的对象
let count = ref(1);

function addCount(){
    // count ++;
    count.value ++;
    console.log(count);
    return count;
}

const form2 = reactive({count1:2})
function addCount2(){
    console.log(form2);
    form2.count1++;
    return form2;
}
</script>