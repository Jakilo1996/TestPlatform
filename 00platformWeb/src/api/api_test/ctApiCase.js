import service from "~/axios";

// 模块名
const module_name = "CtApiCase"
export function ctApiCaseQueryByPage(data){
    return service.post(`/${module_name}/QueryByPage`,data)
}

export function ctApiCaseQueryById(id){
    return service.get(`/${module_name}/QueryById?id=${id}`)
}

export function ctApiCaseCreateAction(data){
    return service.post(`/${module_name}/CreateAction`,data)
}

export function ctApiCaseUpdateAction(data){
    return service.put(`/${module_name}/UpdateAction`,data)
}

export function ctApiCaseDeleteAction(id){
    return service.delete(`/${module_name}/DeleteAction?id=${id}`)
}

// 拓展其他方法
export function ctQueryApiCaseByID(c_id){
    return service.get(`/${module_name}/getDataByColId?collection_id=${c_id}`)
}