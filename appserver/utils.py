import uuid
import json
import hashlib


def get_uuid():
    return uuid.uuid4().hex


def md5encode(str):
    return hashlib.md5(str).hexdigest()


def obj_array_to_json(results, name):
    items = []
    for item in results:
        items.append(item.to_dict())
    return {name: items}


def obj_to_json(result, name):
    return {name: result.to_dict()}
