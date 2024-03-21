<template>
    <!-- 搜索表单 -->
    <el-form ref="searchFormRef" :inline="true" :model="searchForm" class="demo-form-inline">
        <el-form-item label="集合名称">
            <el-input v-model="searchForm.collection_name" placeholder="根据集合名称筛选" />
        </el-form-item>
        <el-form-item label="项目">
            <el-select v-model="searchForm.project_id" placeholder="项目" clearable>
                <el-option v-for="project in projectList" :key="project.id" :label="project.project_name"
                    :value="project.id" />
            </el-select>
        </el-form-item>
        <!-- 这里可以根据需要添加其他搜索条件 -->
        <el-row class="mb-4" type="flex" justify="end">
            <el-button type="primary" @click="loadData()">查询</el-button>
            <el-button type="warning" @click="onDataForm(-1)">新增数据</el-button>
        </el-row>
    </el-form>
    <!-- END 搜索表单 -->

    <!-- 数据表格 -->
    <el-table :data="tableData" style="width: 100%;" max-height="500">
        <!-- 数据列 -->
        <!-- 默认情况下，如果单元格内容过长，会占用多行显示。 若需要单行显示可以使用 show-overflow-tooltip -->
        <el-table-column v-for="col in columnList" :prop="col.prop" :label="col.label" :key="col.prop"
            show-overflow-tooltip="true" />

        <!-- 操作 -->
        <el-table-column fixed="right" label="操作">
            <template #default="scope">
                <el-button link type="primary" size="small" @click.prevent="onDataForm(scope.$index)">
                    编辑
                </el-button>
                <el-button link type="primary" size="small" @click.prevent="onDelete(scope.$index)">
                    删除
                </el-button>
                <el-button link type="primary" size="small" @click.prevent="onExecuteTest(scope.$index)">
                    执行测试
                </el-button>
                <el-button link type="primary" size="small" @click.prevent="showApiHistorysDialog(scope.$index)">
                    执行记录
                </el-button>
            </template>
        </el-table-column>
    </el-table>
    <!-- END 数据表格 -->

    <!-- 分页 -->
    <div class="demo-pagination-block">
        <div class="demonstration"></div>
        <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :page-sizes="[10, 20, 30, 50]"
            layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange"
            @current-change="handleCurrentChange" />
    </div>
    <!-- END 分页 -->

    <!-- 弹窗 - 弹窗加载执行记录 -->
    <el-dialog v-model="apiHistoryDialogFormVisible" title="执行记录">
        <el-form-item>
            <el-table :data="apiHistoryList" style="width: 100%">
                <el-table-column prop="id" label="用例编号" style="width: 5%" />
                <el-table-column prop="create_time" label="执行时间" style="width: 30%" show-overflow-tooltip="true" />
                <el-table-column prop="history_desc" label="执行情况简述" style="width: 60%" show-overflow-tooltip="true" />
                <el-table-column fixed="right" label="操作" style="width: 5%">
                    <template #default="scope">
                        <el-button type="primary" size="small" @click.prevent="showApiHistory(scope.$index)">
                            查看测试报告
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-form-item>

        <el-form-item>
            <el-pagination :current-page="currentApiHistoryPage" :page-size="apiHistoryPageSize" :total="apiHistoryTotal"
                @current-change="handleApiHistoryCurrentChange"></el-pagination>
        </el-form-item>
    </el-dialog>
</template>

<script lang="ts" setup>
import { ref, reactive } from "vue"
import { ctApiCollectionQueryByPage, ctApiCollectionDeleteAction, ctApiCollectionExecuteTestAction } from '~/api/api_test/ctApiCollection.js' // 不同页面不同的接口
import { useRouter } from "vue-router";
const router = useRouter()

// 分页参数
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 搜索功能 - 筛选表单
const searchStatus = ref(false) // 是否应用搜索表单
const searchForm = reactive({ "collection_name": "", "project_id": "" })

// 表格列 - 不同页面不同的列
const columnList = ref([
    { prop: "id", label: '集合编号' },
    { prop: "collection_name", label: '集合名称' },
    // 其他列
])

// 表格数据
const tableData = ref([])

// 加载页面数据
const loadData = () => {
    let searchData = searchForm
    searchData["page"] = currentPage.value
    searchData["pageSize"] = pageSize.value

    ctApiCollectionQueryByPage(searchData).then((res: { data: { data; total: number; msg: string }; }) => {
        tableData.value = res.data.data.data
        total.value = res.data.data.total
    })
}
loadData()

// 变更页大小
const handleSizeChange = (val: number) => {
    console.log("页大小变化:" + val)
    pageSize.value = val
    loadData()
}

// 变更页码
const handleCurrentChange = (val: number) => {
    console.log("页码变化:" + val)
    currentPage.value = val
    loadData()
}


// 打开表单 （编辑/新增）
const onDataForm = (index: number) => {
    let params_data = {}
    if (index >= 0) {
        params_data = {
            id: tableData.value[index]["id"]
        }
    }
    router.push({
        path: '/ApiCollectionForm', // 不同页面不同的表单路径
        query: params_data
    });
}

// 删除数据
const onDelete = (index: number) => {
    ctApiCollectionDeleteAction(tableData.value[index]["id"]).then((res: {}) => {
        loadData()
    })
}

// 执行测试
const onExecuteTest = (index: number) => {
    ctApiCollectionExecuteTestAction(tableData.value[index]["id"]).then((res: {}) => {
        console.log(res)
    })
}

// 其他功能拓展
// 1. 加载项目
import { queryAllApiProject } from "~/api/api_test/ctApiProject.js"; // 不同页面不同的接口
const projectList = ref([{
    id: 0,
    project_name: '',
    project_desc: ''
}]);
function getProjectList() {
    queryAllApiProject().then((res) => {
        projectList.value = res.data.data.data;
    });
}
getProjectList();

// 执行记录加载
import { ctApiHistoryQueryByPage} from "~/api/api_test/ctApiHistory.js"; // 不同页面不同的接口
const apiHistoryList = ref([] as any[]); // 关联的接口
const currentApiHistoryPage = ref(1) // 页码
const apiHistoryPageSize = ref(5) // 每页大小
const apiHistoryTotal = ref(0)
const apiHistoryDialogFormVisible = ref(false) // 是否展示弹窗
const currentCollectionId = ref(0) // 当前展示的执行记录关联的 collectionId
const showApiHistorysDialog = (index: number) => {
    apiHistoryDialogFormVisible.value = true
    apiHistoryTotal.value = 0
    apiHistoryPageSize.value = 5
    currentApiHistoryPage.value = 1
    apiHistoryList.value = []
    currentCollectionId.value = tableData.value[index]["id"]
    loadApiHistorys()
}

// 根据分页参数 加载数据
function loadApiHistorys() {
    let searchData = {}
    searchData["collection_id"] = currentCollectionId.value
    searchData["page"] = currentApiHistoryPage.value
    searchData["pageSize"] = apiHistoryPageSize.value
    ctApiHistoryQueryByPage(searchData).then((res: { data: { data; total: number; msg: string } }) => {
        console.log(res.data.data)
        apiHistoryList.value = res.data.data.data;
        apiHistoryTotal.value = res.data.data.total
    })
}
// 翻页
const handleApiHistoryCurrentChange = (val: number) => {
    console.log("页码变化:" + val)
    currentApiHistoryPage.value = val
    loadApiHistorys()
}
// 展示具体测试报告
const showApiHistory = (index: number) => {
    // 注意： 这个地方的测试报告服务器地址，是需要根据后端服务器修改的，这里写死了，后面要改成配置文件
    var report_id = apiHistoryList.value[index]["history_detail"]
    window.open("http://127.0.0.1:5000/ApiHistory/"+report_id+"/index.html", '_blank');
}
</script>

<style scoped>
.demo-pagination-block+.demo-pagination-block {
    margin-top: 10px;
}

.demo-pagination-block .demonstration {
    margin-bottom: 16px;
}
</style>

