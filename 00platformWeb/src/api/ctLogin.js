import service from "~/axios";


export function ctLogin(username,password){
    return service.post('/CtLogin',{
        username,password
    })
}

export function ctLogout(ct_token){
    return service.post('/CtLogout',{
        ct_token
    })
}