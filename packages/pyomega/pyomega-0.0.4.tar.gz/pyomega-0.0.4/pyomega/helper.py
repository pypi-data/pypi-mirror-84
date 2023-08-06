import os
import json
import copy
from datetime import datetime, timedelta


def get_config():
    with open(os.path.dirname(__file__) + "/../config.json", "r") as read_file:
        config = json.load(read_file)
        config = copy.deepcopy(config)
        read_file.close()
    return config


def get_stage():
    if "ENV" in os.environ:
        stage = os.environ["ENV"]
    else:
        stage = "local"
    return stage

def get_now_str(config):

    time_format = config["time_format"]
    now = datetime.strftime(datetime.now(), time_format)

    return now

def in_list(a, b):
    for item in a:
        if item in b:
            pass
        else:
            return False
    return True

def in_required_list(required, payload):
    for item in required:
        if item in payload:
            continue
        else:
            return False
    return True

def if_empty(object):
    for key, value in object.items():
        if value == "" or value == [] or value == {}:
            return True
    return False

def make_instert_string(object, table):

    fileds = ""
    values = ""
    #var= ""

    for name, value in object.items():
        if type(value) == str:
            value = value.replace("'", "''")
            #print(value)
        fileds = fileds + name + ", "

        if type(value) == dict:
            if value == {} or value == "":
                values = values + "'{}', "

            else:
                string = json.dumps(value)
                string = string.replace("'", "''")
                value = json.loads(string)
                values = values + "'" + json.dumps(value) + "', "

        elif type(value) == bool:

            values = values + str(value) + ", "

        else:
            values = values + "'" + value + "', "


    insert_string = (
            "INSERT INTO " + table + " (" + (fileds[:-2])
            + ") VALUES (" + values[:-2] + ")")

    insert_string = insert_string.replace("'", "\'")

    print("INSERT STRING: " + insert_string)

    return insert_string


def if_request_valid(config, payload, db_object):
    print("CHECKING REQUEST VALIDITY >>>")


    required_items = copy.deepcopy(db_object)
    #print(required_items)
    required_items.pop("created_at")
    required_items.pop("updated_at")
    #required_items.pop("news_id")


    #print(payload)
    print("PAYLOAD: " + json.dumps(payload))
    print("REQUIRED ITEMS: " + json.dumps(required_items))

    try:
        for key, value in required_items.items():
            #print(key)
            if isinstance(value, type(payload[key])) == True \
                    and key in payload.keys() and len(required_items) == len(payload):
                #print(key)
                pass
            else:
                #print(key)
                return False
                break
        return True
    except:
        print(key)
        return False


def object_mapper(object, result):
    mapped_object = {}
    x = 0
    for key in object:
        if key not in ["created_at", "updated_at"]:
            mapped_object[key] = result[x]
            x += 1

    return mapped_object

def is_json(object):
    try:
        json_object = json.loads(object)
        for x, y in json_object.items():
            pass
    except:
        return False
    return True