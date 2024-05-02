from flask import request, jsonify, make_response, current_app, g,abort
from ..tools import functions


def authenticate(ctoken=None):

    if not ctoken:
        abort(401, 'token缺失')
    get_token = functions.GlobalManager()
    token = get_token.get_value("token", ctoken)

    if not token:
        abort(401, '登录已过期或无效的 token')

        # 检查 token 是否有效
    db_instance = current_app.config['db_instance']
    result = db_instance.execute_sync("pdo_get", "user",
                                      fields=["id", "username", "password", "name",
                                              "head_image", "status", "role", "mail", "referral_code", "token"],
                                      conditions={"token": token})

    if not result:
        abort(1003, '账号或密码错误')
    user_data = result[0]
    if user_data['status'] != 1:
        abort(1004, '账号或密码错误')
    # 为之后的请求处理提供全局的用户信息数据
    g.user_info = user_data
