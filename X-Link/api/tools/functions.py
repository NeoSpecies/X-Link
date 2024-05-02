import uuid
import hashlib

from flask import jsonify


class TokenManager:
    @staticmethod
    def generate_token(length=32):
        # 生成指定长度的随机字符串作为 token
        return uuid.uuid4().hex[:length]

    @staticmethod
    def generate_ctoken(user_id):
        # 使用用户ID生成 cToken
        ctoken = uuid.uuid4().hex + "-" + hashlib.md5(f"userId{user_id}".encode()).hexdigest()
        return ctoken


class GlobalManager:
    global_variable = {}  # 定义全局变量为一个空字典

    @classmethod
    def get_global_variable(cls):
        """获取全局变量的值"""
        return cls.global_variable

    def get_value(cls, column, key):
        """获取全局变量的值"""
        if column in cls.global_variable and key in cls.global_variable[column]:
            return cls.global_variable[column][key]
        else:
            return None

    @classmethod
    def set_global_variable(cls, value):
        """设置全局变量的值"""
        cls.global_variable = value

    @classmethod
    def add_value(cls, column, key, value):
        """向全局变量添加用户"""
        cls.global_variable[column][key] = value

    @classmethod
    def remove_value(cls, column, key):
        """从全局变量中删除用户"""
        if column in cls.global_variable and key in cls.global_variable[column]:
            del cls.global_variable[column][key]
        else:
            return None

    @classmethod
    def update_value(cls, column, key, value):
        """更新用户信息"""
        if column in cls.global_variable and key in cls.global_variable[column]:
            cls.global_variable[column][key] = value
        else:
            return None


class PathMatcher:
    def __init__(self, paths):
        self.paths = paths

    def match(self, request_path):
        for path in self.paths:
            if '[*]' in path:
                pattern_path = path.split('[*]')[0]
                if request_path.startswith(pattern_path):
                    return True
            elif request_path == path:
                return True
        return False
