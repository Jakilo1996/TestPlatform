import service from "~/axios";


export function ctLogin(username,password){
    return service.post('/CtApiLogin',{
        username,password
    })
}

export function ctLogout(ct_token){
    return service.post('/CtApiLogout',{
        ct_token
    })
}