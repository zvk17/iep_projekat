from functools import wraps;
from flask_jwt_extended import verify_jwt_in_request, get_jwt;
from flask import make_response, jsonify;


def jwtRoleCheck ( userType ):
    def innerjwtRoleCheck ( function ):
        @wraps ( function )
        def decorator ( *arguments, **keywordArguments ):
            try:
                verify_jwt_in_request();
            except:
                return make_response(jsonify(msg="Missing Authorization Header"), 401);
            claims = get_jwt();
            if "userType" in claims and claims["userType"] == userType:
                return function(*arguments, **keywordArguments);
            else:
                return make_response(jsonify(msg="Missing Authorization Header"), 401);

        return decorator;

    return innerjwtRoleCheck;