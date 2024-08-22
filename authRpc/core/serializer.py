import json


class JSONSerializer:
    def dumps(self, obj):
        # 序列化对象为 JSON 字符串
        return json.dumps(obj).encode('utf-8')

    def loads(self, data):
        # 反序列化 JSON 字符串为 Python 对象
        return json.loads(data.decode('utf-8'))