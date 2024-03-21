import service from "~/axios";

// 模块名
const module_name = "CtApiHistory"
export function ctApiHistoryQueryByPage(data){
    return service.post(`/${module_name}/QueryByPage`,data)
}

export function ctApiHistoryQueryById(id){
    return service.get(`/${module_name}/QueryById?id=${id}`)
}

export function ctApiHistoryCreateAction(data){
    return service.post(`/${module_name}/CreateAction`,data)
}

export function ctApiHistoryUpdateAction(data){
    return service.put(`/${module_name}/UpdateAction`,data)
}

export function ctApiHistoryDeleteAction(id){
    return service.delete(`/${module_name}/DeleteAction?id=${id}`)
}
