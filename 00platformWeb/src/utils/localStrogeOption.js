// localStroge下的某个 key 的对应 value 是Object

// 从localStorage中获取对象
export function getObject(key) {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : null;
  }
  
// 保存对象到localStorage中
export function setObject(key, object) {
  localStorage.setItem(key, JSON.stringify(object));
}

// 更新对象的某个 key
export function updateObject(key,k,v){
    let _object = getObject(key);
    _object[k] = v
    setObject(key,_object)
}
// 删除localStorage中某个key对应array对象的一个键值对
export function removeObject(key,k) {
    let values= getObject(key);
    let copy_values = getObject(key);
    values.forEach((key,v)=>{
        if(key===k){
            delete copy_values[k];
        }
    }
    )
    setObject(key,copy_values);
}

// 清空localStorage中的所有数据
export function clearObject(key) {
  localStorage.removeItem(key);
}
