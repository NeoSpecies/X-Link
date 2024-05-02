from ..auth import authenticate
from flask import request, jsonify, current_app
from ..tools import PathMatcher


def before_request(no_auth=None):
    ctoken = request.headers.get('token')
    path_matcher = PathMatcher(current_app.config["NO_AUTH"])
    if not path_matcher.match(request.path):
        auth_response = authenticate(ctoken)
        if auth_response:
            return auth_response
