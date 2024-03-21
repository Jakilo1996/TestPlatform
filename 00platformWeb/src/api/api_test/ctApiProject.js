import service from "~/axios";

// 模块名
const module_name = "CtApiProject"
export function ctApiProjectQueryByPage(data){
    return service.post(`/${module_name}/QueryByPage`,data)
}

export function ctApiProjectQueryById(id){
    return service.get(`/${module_name}/QueryById?id=${id}`)
}

export function ctApiProjectCreateAction(data){
    return service.post(`/${module_name}/CreateAction`,data)
}

export function ctApiProjectUpdateAction(data){
    return service.put(`/${module_name}/UpdateAction`,data)
}

export function ctApiProjectDeleteAction(id){
    return service.delete(`/${module_name}/DeleteAction?id=${id}`)
}

// 拓展其他方法
export function queryAllApiProject(){
    return service.get(`/${module_name}/QueryAll`)
}