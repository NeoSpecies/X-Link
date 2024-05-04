from flask import Blueprint, request, jsonify, g, current_app
import json

panel = Blueprint('panel', __name__)


@panel.route('/userConfig/get', methods=['POST'])
def get_user_config():
    db_instance = current_app.config['db_instance']
    result = db_instance.execute_sync("pdo_get", "user_config",
                                      fields=["user_id", "panel_json", "search_engine_json"],
                                      conditions={"user_id": g.user_info['id']})
    if not result:
        return jsonify({"code": 1003, "msg": "账号或密码错误"}), 200

    data = {
        "userId": result[0]['user_id'],
        "panel": json.loads(result[0]['panel_json']),
        "searchEngine": result[0]['search_engine_json']
    }
    panel = {
        "code": 0,
        "data": data,
        "msg": "OK"
    }
    return jsonify(panel)


@panel.route('/userConfig/set', methods=['POST'])
def set_user_config():
    data = request.json
    db_instance = current_app.config['db_instance']
    db_instance.execute_sync("pdo_update", "user_config",
                             data={"panel_json": json.dumps(data['panel'])},
                             conditions={"user_id": g.user_info['id']})
    return jsonify({"code": 0, "msg": "OK"})


@panel.route('/item_icon_group/edit', methods=['POST'])
def edit_item_icon_group():
    user_info = g.user_info
    data = request.json
    # 这里应该添加数据验证和转换逻辑
    # ...

    # 根据请求数据处理修改或创建逻辑
    if "id" in data and data["id"]:
        # 修改逻辑
        # ...
        return jsonify({'message': 'Item updated'})
    else:
        # 创建逻辑
        # ...
        return jsonify({'message': 'Item created'})


@panel.route('/itemIconGroup/getList', methods=['POST'])
def get_list_item_icon_group():
    user_info = g.user_info
    db_instance = current_app.config['db_instance']
    result = db_instance.execute_sync("pdo_get", "item_icon_group",
                                      fields=["Created_at", "Updated_at", "Deleted_at", "id", "icon", "title",
                                              "description", "sort", "user_id"],
                                      conditions={"ORDER BY": [
                                          {"sort": "asc"}
                                      ], "user_id": user_info['id']})
    if not result:
        return jsonify({"code": 1003, "msg": "未查询到"}), 200
    groups_json = {
        "code": 0,
        "data": {
            "count": 0,
            "list": result
        },
        "msg": "OK"
    }
    return jsonify(groups_json)


@panel.route('/item_icon_group/delete', methods=['DELETE'])
def delete_item_icon_group():
    user_info = g.user_info
    data = request.json
    # 模拟删除逻辑
    # ...
    return jsonify({'message': 'Deleted'})


@panel.route('/itemIconGroup/saveSort', methods=['POST'])
def save_sort_item_icon_group():
    data = request.get_json()
    print(data)
    db_instance = current_app.config['db_instance']
    for item in data['sortItems']:
        result = db_instance.execute_sync("pdo_update", "item_icon_group",
                                          data={"sort": item["sort"]},
                                          conditions={"id": item["id"]})
    return jsonify({"code": 0, "msg": "OK"})


@panel.route('/itemIcon/saveSort', methods=['POST'])
def itemIcon_saveSort():
    data = request.get_json()
    data["item_icon_group_id"] = data["itemIconGroupId"]
    del data['itemIconGroupId']
    db_instance = current_app.config['db_instance']
    for item in data['sortItems']:
        result = db_instance.execute_sync("pdo_update", "item_icon",
                                          data={"sort": item["sort"]},
                                          conditions={"id": item["id"]})
    return jsonify({"code": 0, "msg": "OK"})


@panel.route('/itemIcon/getListByGroupId', methods=['POST'])
def get_list_by_groupid():
    user_info = g.user_info
    data = request.json
    db_instance = current_app.config['db_instance']
    result = db_instance.execute_sync("pdo_get", "item_icon",
                                      fields=["id", "created_at", "updated_at", "deleted_at", "icon_json", "title",
                                              "url", "lan_url", "description", "open_method", "sort",
                                              "item_icon_group_id", "user_id"],
                                      conditions={"user_id": user_info['id'],
                                                  "item_icon_group_id": data["itemIconGroupId"]})
    if not result:
        return jsonify({"code": 1003, "msg": "账号或密码错误"}), 200
    # 遍历查询结果
    for item in result:
        # 将icon_json从字符串转换为字典
        item['icon'] = json.loads(item['icon_json'])
    data = {
        "code": 0,
        "data": {
            "count": 0,
            "list": result
        },
        "msg": "OK"
    }
    return jsonify(data)


@panel.route('/itemIcon/edit', methods=['POST'])
def save_itemIcon_edit():
    data = request.get_json()
    data['icon_json'] = json.dumps(data['icon'])
    data["item_icon_group_id"] = data["itemIconGroupId"]
    data["open_method"] = data["openMethod"]
    del data['icon']
    del data['itemIconGroupId']
    del data['openMethod']
    db_instance = current_app.config['db_instance']
    result = db_instance.execute_sync("pdo_update", "item_icon",
                                      data=data,
                                      conditions={"id": data["id"], "user_id": g.user_info['id']})
    if not result:
        return jsonify({"code": 1003, "msg": "没有返回值"}), 200
    data = {
        "code": 0,
        "data": {
            "ID": 0,
            "CreatedAt": "0001-01-01T00:00:00Z",
            "UpdatedAt": "0001-01-01T00:00:00Z",
            "DeletedAt": None,
            "id": 29,
            "createTime": "2023-11-16T13:21:32.131853507Z",
            "updateTime": "2023-11-29T11:30:37.5950868+08:00",
            "icon": {
                "itemType": 2,
                "src": "/getFiles/2024/4/26/5a981f60167dad4c38abf68747f66ffe.png",
                "text": "",
                "backgroundColor": "#2a2a2a6b"
            },
            "title": "Sun-Panel",
            "url": "https://github.com/hslr-s/sun-panel",
            "lanUrl": "",
            "description": "一个NAS导航面板",
            "openMethod": 2,
            "sort": 1,
            "itemIconGroupId": 1,
            "userId": 3,
            "user": {
                "ID": 0,
                "CreatedAt": "0001-01-01T00:00:00Z",
                "UpdatedAt": "0001-01-01T00:00:00Z",
                "DeletedAt": None,
                "id": 0,
                "createTime": "0001-01-01T00:00:00Z",
                "updateTime": "0001-01-01T00:00:00Z",
                "username": "",
                "password": "",
                "name": "",
                "headImage": "",
                "status": 0,
                "role": 0,
                "mail": "",
                "referralCode": "",
                "token": "",
                "userId": 0
            }
        },
        "msg": "OK"
    }
    return jsonify(data)


@panel.route('/users/getList', methods=['POST'])
@panel.route('/users/getPublicVisitUser', methods=['POST'])
def getPublicVisitUser():
    user_info = g.user_info
    data = request.json
    db_instance = current_app.config['db_instance']
    result = db_instance.execute_sync("pdo_get", "user",
                                      fields=["id", "username", "password", "name",
                                              "head_image", "status", "role", "mail", "referral_code", "token"],
                                      conditions={})
    if not result:
        return jsonify({"code": 1003, "msg": "账号或密码错误"}), 200
    data = {
        "code": 0,
        "data": {
            "count": 0,
            "list": result
        },
        "msg": "OK"
    }
    return jsonify(data)
