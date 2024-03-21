import service from "~/axios";

// 模块名
const module_name = "CtApiInfo"
export function ctApiInfoQueryByPage(data){
    return service.post(`/${module_name}/QueryByPage`,data)
}

export function ctApiInfoQueryById(id){
    return service.get(`/${module_name}/QueryById?id=${id}`)
}

export function ctApiInfoCreateAction(data){
    return service.post(`/${module_name}/CreateAction`,data)
}

export function ctApiInfoUpdateAction(data){
    return service.put(`/${module_name}/UpdateAction`,data)
}

export function ctApiInfoDeleteAction(id){
    return service.delete(`/${module_name}/DeleteAction?id=${id}`)
}

// 拓展其他方法
// 1.调试请求方法
export function ctApiInfodoDebugRequest(data){
    return service.post(`/${module_name}/DebugExecuteAction`,data)
}