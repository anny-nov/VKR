import json
from typing import Dict
import time


def serialize_message(_from: str, room: str, msg: str, from_name: str) -> dict:
    """
    Serialize a message into a JSON string.
    Args:
        from_: The sender of the message.
        room: The room the message was sent to.
        timestamp: The timestamp of the message.
        msg: The message text.
    Returns:
        A JSON string representing the message.
    """
    timestamp = int(time.time())
    message_dict = {
        "from": _from,
        "room": room,
        "timestamp": timestamp,
        "msg": msg,
        "from_name": from_name
    }
    return message_dict


def deserialize_message(json_str: str): #-> Dict[str, str]:
    """
    Deserialize a JSON string into a message dictionary.
    Args:
        json_str: The JSON string representing the message.
    Returns:
        A dictionary containing the message fields.
    """
    message_dict = json.loads(json_str)
    return message_dict

def deserialize_history(json_str: str):
    message_dict = json.loads(json_str)
    return message_dict

def deserialize_client_info(json_str: str):
    client_dict = json.loads(json_str)
    return client_dict


#def get_room_info(self, json_str: str):
#    message_dict = json.loads(json_str)
#    print("room from json   ", message_dict.get("room", ""))
#    return message_dict.get("room", "")
