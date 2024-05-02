from flask import Blueprint, request, jsonify, current_app,g
from ..tools import functions
import psutil
import secrets
from datetime import datetime
from uuid import uuid4
import hashlib
import json

system = Blueprint('system', __name__)


# 模拟的用户数据库和令牌存储
# 登录
@system.route('/login', methods=['POST'])
def login():
    r_data = request.json
    db_instance = current_app.config['db_instance']
    result = db_instance.execute_sync("pdo_get", "user",
                                      fields=["id", "username", "password", "name",
                                              "head_image", "status", "role", "mail", "referral_code", "token"],
                                      conditions={"username": r_data['username']})
    if not result:
        return jsonify({"code": 1003, "msg": "账号或密码错误"}), 200
    user_data = result[0]
    if r_data['password'] != user_data['password']:
        return jsonify({"code": 1003, "msg": "停用或未激活"}), 200

    if user_data['status'] != 1:
        return jsonify({"code": 1004, "msg": "停用或未激活"}), 200
    token_gen = functions.TokenManager()
    if not user_data['token']:
        # 如果token不存在，则生成一个新的token
        token = token_gen.generate_token()
        # 将新生成的token存储到数据库中
        db_instance.execute_sync("pdo_update", "user",
                                 data={"token": token},
                                 conditions={"id": user_data['id']})
    cToken = token_gen.generate_ctoken(user_data['id'])
    global_manager = functions.GlobalManager()  # 实例化 GlobalManager 类
    if "token" not in global_manager.get_global_variable():  # 调用 get_global_variable 方法的返回值
        global_manager.set_global_variable({"token": {}})
    global_manager.add_value("token", cToken, user_data['token'])
    data = {
        "code": 0,
        "data": {
            "ID": user_data['id'],
            "CreatedAt": "0001-01-01T00:00:00Z",
            "UpdatedAt": "0001-01-01T00:00:00Z",
            "DeletedAt": None,
            "id": user_data['id'],
            "createTime": "2023-11-08T20:22:15.3906832+08:00",
            "updateTime": "2024-01-30T04:40:00.823281558Z",
            "username": user_data['username'],
            "password": "",
            "name": user_data['name'],
            "headImage": "",
            "status": 1,
            "role": 1,
            "mail": user_data['mail'],
            "referralCode": "",
            "token": cToken,
            "userId": user_data['id']
        },
        "msg": "OK"
    }

    return jsonify(data), 200


@system.route('/logout', methods=['POST'])
def logout():
    authorization_header = request.headers.get('token')
    global_manager = functions.GlobalManager()  # 实例化 GlobalManager 类
    global_manager.remove_value("token", authorization_header)
    data = {
        "code": 0,
        "data": {},
        "msg": "OK"
    }
    return jsonify(data), 200


@system.route('/moduleConfig/getByName', methods=['POST'])
def get_by_name():
    data = request.get_json()
    name = data['name']

    db_instance = current_app.config['db_instance']
    result = db_instance.execute_sync("pdo_get", "module_config",
                                      fields=["value_json"],
                                      conditions={"name": name})
    if not result:
        return jsonify({"code": 1003, "msg": "账号或密码错误"}), 200
    panel = {
        "code": 0,
        "data": json.loads(result[0]['value_json']),
        "msg": "OK"
    }

    return jsonify(panel)


@system.route('/moduleConfig/save', methods=['POST'])
def save():
    data = request.get_json()
    db_instance = current_app.config['db_instance']
    result = db_instance.execute_sync("pdo_update", "module_config",
                                      data={"value_json": json.dumps(data['value'])},
                                      conditions={"user_id": g.user_info['id'],"name":data["name"]})
    if not result:
        return jsonify({"code": 1003, "msg": "没有返回值"}), 200
    return jsonify({"code": 0, "msg": "OK"})


@system.route('/monitor/getCpuState', methods=['POST'])
def getCpuState():
    cpu_info = {}
    # 获取核心数量
    cpu_info["coreCount"] = psutil.cpu_count(logical=False)

    # 获取CPU数量
    cpu_info["cpuNum"] = psutil.cpu_count(logical=True)

    # 获取CPU型号
    cpu_info["model"] = "Unknown"
    try:
        with open("/proc/cpuinfo") as f:
            lines = f.readlines()
            for line in lines:
                if "model name" in line:
                    cpu_info["model"] = line.split(":")[1].strip()
                    break
    except FileNotFoundError:
        pass

    # 获取CPU使用率
    cpu_info["usages"] = psutil.cpu_percent(percpu=True)

    data = {
        "code": 0,
        "data": cpu_info,
        "msg": "OK"
    }
    return jsonify(data)


@system.route('/monitor/getDiskUsage', methods=['POST'])
def getDiskUsage():
    data = request.json  # 获取POST请求的JSON数据
    path = data.get("path", "/")  # 从JSON数据中提取路径参数，默认为根路径 "/"

    try:
        disk_usage = psutil.disk_usage(path)
        result = {
            "code": 0,
            "data": {
                "total": disk_usage.total,
                "free": disk_usage.free,
                "used": disk_usage.used,
                "usedPercent": disk_usage.percent
            },
            "msg": "OK"
        }
    except Exception as e:
        result = {
            "code": -1,
            "data": {
                "total": None,
                "free": None,
                "used": None,
                "usedPercent": None
            },
            "msg": str(e)
        }

    return jsonify(result)


@system.route('/monitor/getMemonyState', methods=['POST'])
def getMemonyState():
    memory = psutil.virtual_memory()
    data = {
        "code": 0,
        "data": {
            "total": memory.total,
            "free": memory.available,
            "used": memory.used,
            "usedPercent": memory.used / memory.total * 100
        },
        "msg": "OK"
    }
    return jsonify(data)


@system.route('/monitor/getDiskStateByPath', methods=['POST'])
def getDiskStateByPath():
    data = request.json  # 获取POST请求的JSON数据
    path = data.get("path", "/")  # 从JSON数据中提取路径参数，默认为根路径 "/"

    try:
        disk_usage = psutil.disk_usage(path)
        result = {
            "code": 0,
            "data": {
                "mountpoint": path,
                "total": disk_usage.total,
                "used": disk_usage.used,
                "free": disk_usage.free,
                "usedPercent": disk_usage.percent
            },
            "msg": "OK"
        }
    except Exception as e:
        result = {
            "code": -1,
            "data": {
                "mountpoint": path,
                "total": None,
                "used": None,
                "free": None,
                "usedPercent": None
            },
            "msg": str(e)
        }

    return jsonify(result)
