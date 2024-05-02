import os
import uuid

from flask import Blueprint, request, send_file, make_response, current_app, jsonify, send_from_directory

file = Blueprint('file', __name__)


@file.route('/uploadImg/', methods=['POST'], strict_slashes=False)
def uploadImg():
    # 检查请求是否包含文件
    if 'imgfile' not in request.files:
        return 'No file uploaded', 400

    file = request.files['imgfile']
    # 检查文件是否具有文件名
    if file.filename == '':
        return 'No selected file', 400

    # 生成随机文件名
    filename = str(uuid.uuid4().hex) + os.path.splitext(file.filename)[1]
    # 保存文件到指定位置
    file.save(os.path.join(current_app.config["ROOT_DIR"], current_app.config['UPLOAD_FOLDER'], filename))

    # 返回文件访问地址
    data = {
        "code": 0,
        "data": {
            "imageUrl": f'/api/static/{filename}'
        },
        "msg": "OK"
    }
    return jsonify(data), 200
