<template>
  <el-form ref="ruleFormRef" :inline="false" :model="apiInfo" :rules="rules" class="demo-form-inline">
    <el-form-item>
      <el-col :span="18">
        <el-input v-model="apiInfo.api_name" placeholder="输入名称" prop="api_name" />
      </el-col>
      <el-col :span="3">
        <el-select v-model="apiInfo.project_id" placeholder="项目" @change="projectChange" clearable>
          <el-option v-for="project in projectList" :key="project.id" :label="project.project_name" :value="project.id" />
        </el-select>
      </el-col>
      <el-col :span="3">
        <el-select v-model="apiInfo.module_id" placeholder="模块" clearable>
          <el-option v-for="module_info in moduleList" :key="module_info.id" :label="module_info.module_name"
            :value="module_info.id" /></el-select>
      </el-col>
    </el-form-item>
    <el-form-item>
      <el-col :span="3">
        <el-select v-model="apiInfo.request_method" placeholder="请求方式" style="width: 115px">
          <el-option label="POST" value="POST" />
          <el-option label="GET" value="GET" />
          <el-option label="DELETE" value="DELETE" />
          <el-option label="PUT" value="PUT" />
        </el-select>
      </el-col>
      <el-col :span="17">
        <el-input v-model="apiInfo.request_url" placeholder="请求URL" />
      </el-col>
      <el-col :span="1"></el-col>
      <el-col :span="3"><el-button type="primary" @click="debugRequest">请求(调试)</el-button></el-col>
    </el-form-item>
    <!-- 请求参数 -->
    <el-form-item>
      <el-tabs class="demo-tabs" v-model="tabActiveName">
        <el-tab-pane label="URL参数" name="URL参数">
          <el-table :data="apiInfo.request_params" style="width: 100%" max-height="250">
            <el-table-column prop="key" label="参数名" style="width: 40%" />
            <el-table-column prop="value" label="参数值" style="width: 40%" />
            <el-table-column fixed="right" label="删除" style="width: 20%">
              <template #default="scope">
                <el-button link type="primary" size="small" @click.prevent="deleteParams(scope.$index)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-input v-model="requestParams.key" placeholder="输入参数名" style="width: 40%" />
          <el-input v-model="requestParams.value" placeholder="输入参数值" style="width: 40%" />
          <el-button style="width: 20%" @click="onAddParams">添加</el-button>
        </el-tab-pane>
        <el-tab-pane label="请求头Header" name="请求头Header">
          <el-table :data="apiInfo.request_headers" style="width: 100%" max-height="250">
            <el-table-column prop="key" label="请求头名称" style="width: 40%" />
            <el-table-column prop="value" label="请求头内容" style="width: 40%" />
            <el-table-column fixed="right" label="删除" style="width: 20%">
              <template #default="scope">
                <el-button link type="primary" size="small" @click.prevent="deleteHeaders(scope.$index)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-input v-model="requestHeaders.key" placeholder="输入请求头名称" style="width: 40%" />
          <el-input v-model="requestHeaders.value" placeholder="输入请求头内容" style="width: 40%" />
          <el-button style="width: 20%" @click="onAddHeaders">添加</el-button>
        </el-tab-pane>
        <el-tab-pane label="请求Body" name="请求Body">
          <el-tabs class="demo-tabs" model-value="form-data">
            <el-tab-pane label="form-data" name="form-data">
              <el-table :data="apiInfo.request_form_datas" style="width: 100%" max-height="250">
                <el-table-column prop="key" label="表单参数名" style="width: 40%" />
                <el-table-column prop="value" label="表单参数值" style="width: 40%" />
                <el-table-column fixed="right" label="删除" style="width: 20%">
                  <template #default="scope">
                    <el-button link type="primary" size="small" @click.prevent="deleteBodyFormDatas(scope.$index)">
                      删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
              <el-input v-model="requestBodyFormDatas.key" placeholder="输入表单参数名" style="width: 40%" />
              <el-input v-model="requestBodyFormDatas.value" placeholder="输入表单参数值" style="width: 40%" />
              <el-button style="width: 20%" @click="onAddBodyFormDatas">添加</el-button>
            </el-tab-pane>
            <el-tab-pane label="x-www-form-data" name="x-www-form-data">
              <el-table :data="apiInfo.request_www_form_datas" style="width: 100%" max-height="250">
                <el-table-column prop="key" label="表单参数名" style="width: 40%" />
                <el-table-column prop="value" label="表单参数值" style="width: 40%" />
                <el-table-column fixed="right" label="删除" style="width: 20%">
                  <template #default="scope">
                    <el-button link type="primary" size="small" @click.prevent="deleteBodyWwwFormDatas(scope.$index)">
                      删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
              <el-input v-model="requestBodyWwwFormDatas.key" placeholder="输入表单参数名" style="width: 40%" />
              <el-input v-model="requestBodyWwwFormDatas.value" placeholder="输入表单参数值" style="width: 40%" />
              <el-button style="width: 20%" @click="onAddBodyWwwFormDatas">添加</el-button>
            </el-tab-pane>
            <el-tab-pane label="json" name="json">
              <el-input v-model="apiInfo.requests_json_data" type="textarea" :rows="10" placeholder="请输入内容" />
            </el-tab-pane>
          </el-tabs>
        </el-tab-pane>
        <el-tab-pane label="执行前事件(pre)" name="执行前事件(pre)">
          <el-row :rows="15">
            <el-col :span="17">
              <el-input v-model="apiInfo.pre_request" type="textarea" :rows="15" placeholder="执行前事件（数据加密、数据库查询等等）" />
            </el-col>
            <el-col :span="1" />
            <el-col :span="6">
              <el-link href="https://hctestedu.com" target="_blank" type="danger" style="width: 100%">执行前脚本编写说明书</el-link>
              <el-link type="success" style="width: 100%" @click="code_pre_sql">数据库操作</el-link>
            </el-col>
          </el-row>
        </el-tab-pane>
        <el-tab-pane label="执行后事件(post)" name="执行后事件(post)">
          <el-row :rows="15">
            <el-col :span="17">
              <el-input v-model="apiInfo.post_request" type="textarea" :rows="15" placeholder="执行后事件（断言、数据提取等等）" />
            </el-col>
            <el-col :span="1" />
            <el-col :span="6">
              <el-link href="https://hctestedu.com" target="_blank" type="danger" style="width: 100%">执行后脚本编写说明书</el-link>
              <el-link type="success" style="width: 100%" @click="code_jsonAssert">json数据断言</el-link>
              <el-link type="success" style="width: 100%" @click="code_statusCodeAssert">响应状态码断言</el-link>
              <el-link type="success" style="width: 100%" @click="code_headerAssert">响应头断言</el-link>
              <el-link type="success" style="width: 100%" @click="code_json_vars">json数据提取</el-link>
            </el-col>
          </el-row>
        </el-tab-pane>
        <el-tab-pane label="DEBUG变量定义" name="DEBUG变量定义">
          <el-table :data="apiInfo.debug_vars" style="width: 100%" max-height="250">
            <el-table-column prop="key" label="变量名" style="width: 40%" />
            <el-table-column prop="value" label="变量值" style="width: 40%" />
            <el-table-column fixed="right" label="删除" style="width: 20%">
              <template #default="scope">
                <el-button link type="primary" size="small" @click.prevent="deleteVars(scope.$index)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-input v-model="debugVars.key" placeholder="输入变量名" style="width: 40%" />
          <el-input v-model="debugVars.value" placeholder="输入变量值" style="width: 40%" />
          <el-button style="width: 20%" @click="onAddVars">添加</el-button>
        </el-tab-pane>
        <el-tab-pane label="调试输出内容" name="调试输出内容">
          <el-input v-model="debugArea" type="textarea" :rows="10" placeholder="接口调用输出内容" disabled />
        </el-tab-pane>
      </el-tabs>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">保存</el-button>
      <el-button type="primary" @click="onCancel">取消</el-button>
    </el-form-item>
  </el-form>
</template>
    
<script lang="ts" setup>
import { reactive, ref } from "vue";
import { ctApiInfoQueryById, ctApiInfoCreateAction, ctApiInfoUpdateAction } from '~/api/api_test/ctApiInfo.js' // 不同页面不同的接口; // 不同页面不同的接口
import type { FormInstance, FormRules } from 'element-plus';
import { useRouter } from "vue-router";
const router = useRouter();
// 表单实例
const ruleFormRef = ref<FormInstance>();
const apiInfo = reactive({
  id: 0,
  project_id: 0,
  module_id: 0,
  api_name: "",
  request_method: "",
  request_url: "",
  request_params: [] as any[],
  request_headers: [] as any[],
  debug_vars: [] as any[],
  request_form_datas: [] as any[], // 请求中的 form-data
  request_www_form_datas: [] as any[], // 请求中的 x-www-form-data
  request_json_data: "", // 请求中的 json 数据
  pre_request: "", // 执行前事件
  post_request: "", // 执行后事件
});
// 1. 加载项目
import { queryAllApiProject } from "~/api/api_test/ctApiProject.js"; // 不同页面不同的接口
// 不同页面不同的接口
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
// 2. 加载模块
import { ctApiModuleQueryByPage } from "~/api/api_test/ctApiModule.js"; // 不同页面不同的接口
// 不同页面不同的接口
const moduleList = ref([{
  id: 0,
  module_name: '',
  module_desc: ''
}]);
function getModuleList() { // 根据项目加载模块
  ctApiModuleQueryByPage({
    "project_id": apiInfo.project_id,
    "page": 1,
    "pageSize": 999999
  }).then((res) => {
    moduleList.value = res.data.data.data;
  });
}
const projectChange = (value: number) => { // 项目变动触发
  getModuleList()
}

// 3. 如果有id参数，说明是编辑，需要获取数据
const loadData = async (id: number) => {
  const res = await ctApiInfoQueryById(id)
  // 不同的页面，不同的表单字段 (注意这里的res.data.data.xxx，xxx是接口返回的字段，不同的接口，字段不同)
  // 注意:此处将 后台的json字符串转变为对象
  const resData = res.data.data.data[0];
  console.log(resData);
  apiInfo.id = resData.id
  apiInfo.project_id = resData.project_id
  apiInfo.module_id = resData.module_id
  apiInfo.api_name = resData.api_name
  apiInfo.request_method = resData.request_method
  apiInfo.request_url = resData.request_url
  apiInfo.request_params = JSON.parse(resData.request_params) //将json对象转换为json字符串，传给后端,
  apiInfo.request_headers = JSON.parse(resData.request_headers)
  apiInfo.debug_vars = JSON.parse(resData.debug_vars)
  apiInfo.request_form_datas = JSON.parse(resData.request_form_datas) // 请求中的 form-data
  apiInfo.request_www_form_datas = JSON.parse(resData.request_www_form_datas) // 请求中的 x-www-form-data
  apiInfo.request_json_data = resData.requests_json_data // 请求中的 json 数据
  apiInfo.pre_request = resData.pre_request // 执行前事件
  apiInfo.post_request = resData.post_request // 执行后事件
}
let query_id = router.currentRoute.value.query.id
apiInfo.id = query_id ? Number(query_id) : 0
if (apiInfo.id > 0) {
  loadData(apiInfo.id)
  getModuleList()
}

// 4. 表单操作
// 表单验证规则 - 不同的页面，不同的校验规则
const rules = reactive<any>({
  api_name: [
    { required: true, message: '必填项', trigger: 'blur' }
  ],
  module_desc: [
    { required: true, message: '必填项', trigger: 'blur' }
  ]
});
const onSubmit = () => {
  console.log(apiInfo)
  // 提交之前记得把数组修改为json字符串
  let data = {
    id: apiInfo.id,
    project_id: apiInfo.project_id,
    module_id: apiInfo.module_id,
    api_name: apiInfo.api_name,
    request_method: apiInfo.request_method,
    request_url: apiInfo.request_url,
    request_params: JSON.stringify(apiInfo.request_params), //将json对象转换为json字符串，传给后端,
    request_headers: JSON.stringify(apiInfo.request_headers),
    debug_vars: JSON.stringify(apiInfo.debug_vars),
    request_form_datas: JSON.stringify(apiInfo.request_form_datas), // 请求中的 form-data
    request_www_form_datas: JSON.stringify(apiInfo.request_www_form_datas), // 请求中的 x-www-form-data
    request_json_data: apiInfo.requests_json_data, // 请求中的 json 数据
    pre_request: apiInfo.pre_request, // 执行前事件
    post_request: apiInfo.post_request, // 执行后事件
  }

  if (apiInfo.id > 0) {
    ctApiInfoUpdateAction(data).then((res: { data: { code: number; msg: string; }; }) => {
      if (res.data.code == 200) {
        router.push('/ApiInfoList') // 跳转回列表页面 - 不同的页面，不同的路径
      }
    })
  } else {
    ctApiInfoCreateAction(data).then((res: { data: { code: number; msg: string } }) => {
      if (res.data.code == 200) {
        router.push('/ApiInfoList') // 跳转回列表页面 - 不同的页面，不同的路径
      }
    });
  }

};

const onCancel = () => {
  router.push('/ApiInfoList')
};

// 5. 发起调试请求
import { ctApiInfodoDebugRequest } from "~/api/api_test/ctApiInfo.js"
const debugArea = ref(null)
const tabActiveName = ref("URL参数");
const debugRequest = () => {
  // console.log("debugRequest!");
  // console.log(apiInfo);
  tabActiveName.value = "调试输出内容";
  ctApiInfodoDebugRequest(apiInfo).then((res) => {
    console.log(res)
    debugArea.value = res.request.response
  })
};

// 6. requestParams 请求url参数
const requestParams = reactive({
  key: "",
  value: "",
});

const deleteParams = (index: number) => {
  apiInfo.request_params.splice(index, 1);
};

const onAddParams = () => {
  // 保存起来
  apiInfo.request_params.push({
    key: requestParams.key,
    value: requestParams.value,
  });
  // 置空
  requestParams.key = "";
  requestParams.value = "";
};

// requestHeaders 请求头信息
const requestHeaders = reactive({
  key: "",
  value: "",
});

const deleteHeaders = (index: number) => {
  apiInfo.request_headers.splice(index, 1);
};

const onAddHeaders = () => {
  // 保存起来
  apiInfo.request_headers.push({
    key: requestHeaders.key,
    value: requestHeaders.value,
  });
  // 置空
  requestHeaders.key = "";
  requestHeaders.value = "";
};

// debugVars 变量定义
const debugVars = reactive({
  key: "",
  value: "",
});

const deleteVars = (index: number) => {
  apiInfo.debug_vars.splice(index, 1);
};

const onAddVars = () => {
  // 保存起来
  apiInfo.debug_vars.push({
    key: debugVars.key,
    value: debugVars.value,
  });
  // 置空
  debugVars.key = "";
  debugVars.value = "";
};

// requestBodyFormDatas 变量定义
const requestBodyFormDatas = reactive({
  key: "",
  value: "",
});

const deleteBodyFormDatas = (index: number) => {
  apiInfo.request_form_datas.splice(index, 1);
};

const onAddBodyFormDatas = () => {
  // 保存起来
  apiInfo.request_form_datas.push({
    key: requestBodyFormDatas.key,
    value: requestBodyFormDatas.value,
  });
  // 置空
  requestBodyFormDatas.key = "";
  requestBodyFormDatas.value = "";
};

// requestBodyWwwFormDatas 变量定义
const requestBodyWwwFormDatas = reactive({
  key: "",
  value: "",
});

const deleteBodyWwwFormDatas = (index: number) => {
  apiInfo.request_www_form_datas.splice(index, 1);
};

const onAddBodyWwwFormDatas = () => {
  // 保存起来
  apiInfo.request_www_form_datas.push({
    key: requestBodyWwwFormDatas.key,
    value: requestBodyWwwFormDatas.value,
  });
  // 置空
  requestBodyWwwFormDatas.key = "";
  requestBodyWwwFormDatas.value = "";
};

// 代码段 - SQL处理
const code_pre_sql = () => {
  let code = `
      result = sql_exec('mysql',{
          'host': 'shop-xo.hctestedu.com',
          'user': 'api_test',
          'password': 'Aa9999!',
          'db': 'shopxo_hctested'
      },"SELECT * FROM \`sxo_user\` where username='{{accounts}}'")
      # 加密后的用户名
      context.update({'assert_userinfo': result[0]})`;
  apiInfo.pre_request += code;
};
// 代码段 - json断言
const code_jsonAssert = () => {
  console.log("jsonAssert!");
  let code = `\nassert step['response'].json()['你要判断的数据'] == '断言值', '断言提示语句`;
  apiInfo.post_request += code;
};
// 代码段 - 响应状态码断言
const code_statusCodeAssert = () => {
  let code = "\nassert step['response'].status_code == '断言值', '断言提示语句";
  apiInfo.post_request += code;
};
// 代码段 - 响应头断言
const code_headerAssert = () => {
  let code =
    "\nassert step['response'].headers['你要判断的头名称'] == '断言值', '断言提示语句";
  apiInfo.post_request += code;
};
// 代码段 - json数据提取
const code_json_vars = () => {
  console.log("jsonPath!");
  let code = `\ncontext.update({'你要提取的变量名': step['response'].json()['你要提取的数据']})`;
  apiInfo.post_request += code;
};
</script>
    
<style>
/* .demo-form-inline .el-input {
      --el-input-width: 220px;
  } */
</style>
    