from flask import Blueprint, request, jsonify, current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
import hashlib
import json

user = Blueprint('user', __name__)


@user.route('/getAuthInfo', methods=['POST'])
def get_info():
    user_info = g.user_info
    # 根据期望的返回值构建响应数据
    response_data = {
        "user": {
            "ID": user_info["id"],
            "CreatedAt": "0001-01-01T00:00:00Z",
            "UpdatedAt": "0001-01-01T00:00:00Z",
            "DeletedAt": None,
            "id": user_info["id"],
            "createTime": "0001-01-01T00:00:00Z",
            "updateTime": "0001-01-01T00:00:00Z",
            "username": user_info["username"],
            "password": "",
            "name": user_info["name"],
            "headImage": user_info["head_image"],
            "status": 0,
            "role": user_info["role"],
            "mail": user_info["mail"],
            "referralCode": user_info["referral_code"],
            "token": user_info["token"],
            "userId": user_info["id"]
        },
        "visitMode": "0"
    }

    # 根据期望的返回值结构构造完整的响应
    full_response = {
        "code": 0,
        "data": response_data,
        "msg": "OK"
    }

    # 使用 jsonify 返回 JSON 响应
    return jsonify(full_response)


@user.route('/updateInfo', methods=['POST'])
def update_info():
    data = request.json
    db_instance = current_app.config['db_instance']
    db_instance.execute_sync("pdo_update", "user",
                             data={"name": data['name']},
                             conditions={"id": g.user_data['id']})

    return jsonify({"code": 0, "msg": "OK"})


@user.route('/update_password', methods=['POST'])
def update_password():
    user_info = g.user_info
    data = request.json
    if not check_password_hash(user_info["password"], data["oldPassword"]):
        return jsonify({"error": "Old password is incorrect"}), 401
    user_info["password"] = generate_password_hash(data["newPassword"])
    user_info["token"] = ""  # 演示目的，表示清空token
    return jsonify({"status": "success"})


@user.route('/get_referral_code', methods=['GET'])
def get_referral_code():
    user_info = g.user_info
    return jsonify({"referralCode": user_info["referral_code"]})
