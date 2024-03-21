import service from "~/axios";

// 模块名 - 和后台对应
const module_name = "CtApiModule"

// 标准 - 增删改查接口调用
export function ctApiModuleQueryByPage(data) {
    return service.post(`/${module_name}/QueryByPage`, data)
}

export function ctApiModuleQueryById(id) {
    return service.get(`/${module_name}/QueryById?id=${id}`)
}

export function ctApiModuleCreateAction(data) {
    return service.post(`/${module_name}/CreateAction`, data)
}

export function ctApiModuleUpdateAction(data) {
    return service.put(`/${module_name}/UpdateAction`, data)
}

export function ctApiModuleDeleteAction(id){
    return service.delete(`/${module_name}/DeleteAction?id=${id}`)
}
// 拓展其他方法