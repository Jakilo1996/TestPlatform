
import service from "~/axios";

// 模块名
const module_name = "CtApiUser"
export function ctGetUserList(per_page,currentPage){
    // 参数格式如下：url？参数 1=,参数 2=xxx
    return service.get(`/${module_name}/GetList?per_page=${per_page}&current_page=${currentPage}`)
}

export function ctDelectUser(id){
    // 参数格式如下：url？参数 1=,参数 2=xxx
    return service.delete(`/${module_name}/DeleteAction?id=${id}`)
}

export function ctCreateUserAction(username,password,role){
    return service.post(`/${module_name}/CreateAction`,{
        username,password,role
    })
}

export function CtUpdateUserAction(id,username,password,role){
    return service.put(`/${module_name}/UpdateAction`,{
        id,username,password,role
    })
}