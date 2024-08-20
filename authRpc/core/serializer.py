import json


class JSONSerializer:
    def serialize(self, obj):
        if isinstance(obj, dict):
            return json.dumps(obj).encode('utf-8')
        return obj

    def deserialize(self, s):
        try:
            return json.loads(s.decode('utf-8'))
        except ValueError:
            return s