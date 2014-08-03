import uuid
import json

def get_uuid():
    return uuid.uuid4().hex


class JsonEncoder(json.JSONEncoder):
    def default(self,obj):
        d = {}
        d[obj.__class__.__name__] = {}
        d[obj.__class__.__name__].update(obj.__dict__)
        return d


class JsonDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self,object_hook=self.dict2object)

    def dict2object(self,d):
        if'__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            class_ = getattr(module,class_name)
            args = dict((key.encode('ascii'), value) for key, value in d.items()) 
            inst = class_(**args) 
        else:
            inst = d
        return inst

