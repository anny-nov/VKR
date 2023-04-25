import json
import time


def serialize_message(_from: str, room: str, msg: str, from_name: str) -> dict:
    timestamp = int(time.time())
    message_dict = {
        "from": _from,
        "room": room,
        "timestamp": timestamp,
        "msg": msg,
        "from_name": from_name
    }
    return message_dict


def deserialize_message(json_str: str):
    message_dict = json.loads(json_str)
    return message_dict


def deserialize_history(json_str: str):
    message_dict = json.loads(json_str)
    return message_dict


def deserialize_client_info(json_str: str):
    client_dict = json.loads(json_str)
    return client_dict

