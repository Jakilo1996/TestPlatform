import service from "~/axios";

// 模块名
const module_name = "CtApiCollection"
export function ctApiCollectionQueryByPage(data){
    return service.post(`/${module_name}/QueryByPage`,data)
}

export function ctApiCollectionQueryById(id){
    return service.get(`/${module_name}/QueryById?id=${id}`)
}

export function ctApiCollectionCreateAction(data){
    return service.post(`/${module_name}/CreateAction`,data)
}

export function ctApiCollectionUpdateAction(data){
    return service.put(`/${module_name}/UpdateAction`,data)
}

export function ctApiCollectionDeleteAction(id){
    return service.delete(`/${module_name}/DeleteAction?id=${id}`)
}

// 执行测试
export function ctApiCollectionExecuteTestAction(id){
    return service.get(`/${module_name}/ExecuteTestAction?id=${id}`)
}