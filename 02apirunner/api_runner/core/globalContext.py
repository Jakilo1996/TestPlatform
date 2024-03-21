class GContext:  # 类继承
    _dic = {}  # 内置属性，外部不可修改

    def set_dict(self, key: str, value):  # 函数 -- PI*r*r
        self._dic[key] = value

    def get_dict(self, key: str):
        return self._dic[key]

    def set_by_dict(self, dic: dict) -> None:
        self._dic.update(dic)

    def show_dict(self) -> dict:
        return self._dic
