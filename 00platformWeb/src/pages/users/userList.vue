<template>
    <el-card shadow="never" class="border-0">
        <!-- 新增|刷新 -->
        <div class="flex items-center justify-between mb-4">
            <!--新增窗口弹窗-->
            <el-button type="primary" size="small" @click="handleCreate">新增</el-button>
            <el-tooltip effect="dark" content="刷新数据" placement="top">
                <el-button text>
                    <el-icon :size="20">
                        <Refresh />
                    </el-icon>
                </el-button>
            </el-tooltip>
        </div>
        <el-table :data="tableData" stripe style="width: 100%" v-loading="loading" :default-sort="{ prop: 'id' }">
            <el-table-column type="selection" width="55" />
            <el-table-column prop="id" label="用户id" sortable/>
            <el-table-column prop="username" label="用户名" />
            <el-table-column prop="create_time" label="创建时间" sortable />
            <el-table-column label="角色" :formatter="formatRoles"/>
            <el-table-column label="操作" width="180" align="center">
                <template #default="scope">
                    <el-button type="primary" size="small" text @click="handleEdit(scope.row)">修改</el-button>
                    <el-popconfirm title="是否要删除该用户？" confirmButtonText="确认" cancelButtonText="取消"
                        @confirm="handleDelete(scope.row.id)">
                        <template #reference>
                            <el-button text type="primary" size="small">删除</el-button>
                        </template>
                    </el-popconfirm>
                </template>
            </el-table-column>
        </el-table>
        <!-- <el-button @click="toggleSelection()">Clear selection</el-button>以后再说 -->
        <!--加入分页控件-->
        <div class="flex items-center justify-center mt-5">
            <el-pagination background layout="prev, pager, next" v-model:hide-on-single-page="paginationTag" :total="total"
                v-model:current-page="currentPage" :page-size="limit" :pager-count="11" @current-change="getData"
                @prev-click="currentPage -= 1" @next-click:="currentPage += 1" />
        </div>

        <!--弹出窗口-->
        <el-dialog v-model="outerVisible" title="用户操作">
            <div class="window">
                <el-form ref="formRef" :model="form" class="w-350px] " label-width="100px" :rules="rules">
                    <el-form-item prop="username" label="用户名" class="label-wrap">
                        <el-input class="w-100 m-2" v-model="form.username">
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="password" label="新密码" class="label-wrap">
                        <el-input type="password" class="w-100 m-2" v-model="form.password" show-password>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="conPassword" label="确认密码" class="label-wrap">
                        <el-input type="password" class="w-100 m-2" v-model="form.conPassword" show-password>
                        </el-input>
                    </el-form-item>
                    <el-form-item label="角色" class="label-wrap" prop="role" @change="changeRole">
                        <el-select v-model="form.role" class="w-100 m-2">
                            <el-option label="管理员" value="0" />
                            <el-option label="普通测试人员" value="1" />
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                        <div class="dialog-footer">
                            <el-button @click="outerVisible = false">取消</el-button>
                            <el-button type="primary" @click="onAddUser">
                                确认
                            </el-button>
                        </div>
                    </el-form-item>
                </el-form>
            </div>
        </el-dialog>
    </el-card>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ctGetUserList,ctCreateUserAction,ctDelectUser,CtUpdateUserAction } from '~/api/ctUser'
import { ElNotification } from 'element-plus' //提示弹窗
const tableData = ref([])
const loading = ref(false)
const outerVisible = ref(false) //添加用户控件是否可见

//分页控件定义
const currentPage = ref(1)
var total = ref(0)
// 控制数据仅有一页显示
let paginationTag = ref(true)
const limit = 10

// 0 新增 非0表示修改
const editId = ref(0)

 //定义一个全局ID，用来给修改去传递id 
 const id = ref(0)

//定义一个角色，用来存放角色的id
const roleParam = ref(0)


//处理 role 与显示的关系
function formatRoles(row){
  return row.role == 0?"管理员":"普通测试人员"
}


getData();
function getData() {
    loading.value = true
    ctGetUserList(limit, currentPage.value).then(
        (res) => {
            if (res.status == 200){
                console.log(res);
            if (res.data.data.total) {
                // console.log('res.data.data.user_data');
                total = res.data.data.total;
                if (total <= limit) {
                    console.log(total);
                    console.log(paginationTag);
                    paginationTag = false;
                }
                // console.log('res.data.data.user_data');
                // console.log(res.data.data.user_data);
                tableData.value = res.data.data.user_data;
                console.log(tableData.value)
            }
        }}
    ).catch((err) => {
        console.log(err);
    }).finally(()=>{
        loading.value = false;
    });
    // 分页查询？确定一页多少条 举例 10条
    // 第一页 1 -10  第二页 11-20 
    // 前端能告诉后端什么？ 点击是多少页 ，每页需要展示多少条（固定）？
    // 每次点击按钮，都是重新查询。
    // sql语句 11-20   找到一个公式  通过页数和条数，找到到底要从哪里开始找
}



const form = reactive({
    username: '',
    password: '',
    role: ''

})
const validatePass2 = (rule, value, callback) => {
    if (value !== form.password) {
        callback(new Error("确认密码与原密码不匹配!"))
    } else {
        callback()
    }
}
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
    ],
    conPassword: [
        { validator: validatePass2, trigger: 'blur' },
        { required: true, message: '确认密码不能为空', trigger: 'blur' },
        { min: 3, max: 15, message: '请输入 3 到 15 位的密码', trigger: 'blur' },
    ],
    role:[
        {
            required: true,
            message: '请选择一个角色',
            trigger: 'change',
        }
    ]
}
const formRef = ref(null);

const onsubmit = () =>{
    const fun  = editId.value ==0 ?ctCreateUserAction(form.username, form.password, form.role) :CtUpdateUserAction(id.value,form.username, form.password, form.role);
    return fun
}
const onAddUser = () => {
    formRef.value.validate(
        (vaild) => {
            if (!vaild) {
                console.log("未通过表单验证");
                return false; //前端如果不想让代码继续执行，直接 return false
            } else {
                console.log('通过校验');
                //校验通过后，发送请求 axios
                onsubmit().then(
                    (res) => {
                        console.log(res);
                        if (res.data.code == 200) {
                            ElNotification({
                                title: 'Success',
                                message: '创建用户成功',
                                type: 'success',
                                position: 'top-right',
                                offset: 100,
                            })
                        } else {
                            ElNotification({
                                title: 'Error',
                                message: res.data.message,
                                type: 'error',
                                position: 'top-right',
                                offset: 100,
                            })
                        }
                    }
                ).catch((err) => {
                    console.log(err);
                });
            }
        }
    )
}
   
const handleCreate=()=>{
  //清空页面
  resetForm({
    username: '',
    password: '',
    role: ''
  })
  // 确认当前操作是新增
  editId.value = 0
  //打开弹窗
  outerVisible.value = true
}
//编辑操作 
// 将自动读取编辑的行信息
function resetForm(row=false){
 if(row){
  for (const key in form){
    form[key] = row[key]
  }
 }
}
//编辑方法
const handleEdit =(row)=>{
  editId.value =row.id
  id.value = row.id
  roleParam.value = row.role
  row.password = ""
  resetForm(row)
  form.role = formatRoles(row)
  outerVisible.value = true
}

function changeRole(){
  roleParam.value = form.role
}

const handleDelete = (id)=>{
  loading.value =true
  ctDelectUser(id).then(res=>{
   getData()
  }).catch((err) => {
            console.log(err);}
            ).finally(()=>{
                loading.value = false
                });
}


</script>
<style>
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.text {
    font-size: 14px;
}

.item {
    margin-bottom: 18px;
}

.box-card {
    width: 480px;
}
</style>