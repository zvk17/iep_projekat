from flask import Flask, request, jsonify, make_response;
from sqlalchemy import and_;
from models import database, User, UserType;
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, create_refresh_token, get_jwt, get_jwt_identity;
from configuration import Configuration;
import validation;

application = Flask ( __name__ );
application.config.from_object ( Configuration );
#database.init_app ( application );
jwt = JWTManager ( application );


@application.route ( "/register", methods = ["POST"] )
def register ():
    if (request.json is None):
        return make_response(jsonify(message="Field jmbg is missing."), 400);

    jmbg = request.json.get("jmbg", "");
    forename = request.json.get("forename", "");
    surname = request.json.get("surname", "");
    email = request.json.get("email", "");
    password = request.json.get("password", "");

    if (len(jmbg) == 0):
        return make_response(jsonify(message="Field jmbg is missing."),  400);
    if (len(forename) == 0):
        return make_response(jsonify(message="Field forename is missing."), 400);
    if (len(surname) == 0):
        return make_response(jsonify(message="Field surname is missing."), 400);
    if (len(email) == 0):
        return make_response(jsonify(message="Field email is missing."), 400);
    if (len(password) == 0):
        return make_response(jsonify(message="Field password is missing."), 400);

    if (not validation.checkJmbg(jmbg)):
        return make_response(jsonify(message="Invalid jmbg."), 400);

    if (not validation.checkEmail(email)):
        return make_response(jsonify(message="Invalid email."), 400);

    if (not validation.checkPassword(password)):
        return make_response(jsonify(message="Invalid password."), 400);

    user = User.query.filter(User.email == email).first();
    if (not not user):
        return  make_response(jsonify(message="Email already exists."), 400);

    newUser = User(
        jmbg= jmbg,
        email=email,
        password=password,
        forename=forename,
        surname=surname,
        userType=UserType.ELECTION_OFFICIAL
    );
    database.session.add(newUser);
    database.session.commit();

    return make_response("", 200);

@application.route ( "/login", methods = ["POST"] )
def login ( ):
    if (request.json is None):
        return make_response(jsonify(message="Field email is missing."), 400);

    email = request.json.get("email", "");
    password = request.json.get("password", "");

    if (len(email) == 0):
        return make_response(jsonify(message="Field email is missing."), 400);
    if (len(password) == 0):
        return make_response(jsonify(message="Field password is missing."), 400);

    if (not validation.checkEmail(email)):
        return make_response(jsonify(message="Invalid email."), 400);

    user = User.query.filter(and_(User.email == email, User.password == password)).first();
    if (not user):
        return make_response(jsonify(message="Invalid credentials."), 400);

    additionalClaims = {
        "forename": user.forename,
        "surname": user.surname,
        "userType": user.userType,
        "jmbg": user.jmbg,
        "email": user.email
    }
    accessToken = create_access_token(identity=user.email, additional_claims=additionalClaims);
    refreshToken = create_refresh_token(identity=user.email, additional_claims=additionalClaims);

    #na linuxu pravi problem
    if (isinstance(accessToken, bytes)):
        accessToken = accessToken.decode("utf-8");
    if (isinstance(refreshToken, bytes)):
        refreshToken = refreshToken.decode("utf-8");
    print(accessToken)
    print(type(accessToken))
    return make_response(jsonify(accessToken = accessToken,refreshToken = refreshToken), 200);




@application.route ( "/refresh", methods = ["POST"] )
@jwt_required ( refresh = True )
def refresh ( ):
    identity = get_jwt_identity();
    refreshClaims = get_jwt();
    additionalClaims = {
        "forename": refreshClaims["forename"],
        "surname": refreshClaims["surname"],
        "userType": refreshClaims["userType"],
        "jmbg": refreshClaims["jmbg"],
        "email": refreshClaims["email"]
    }
    accessToken = create_access_token(identity=identity, additional_claims=additionalClaims);
    #linux problem
    if (isinstance(accessToken, bytes)):
        accessToken = accessToken.decode("utf-8");
    return make_response (jsonify(accessToken = accessToken), 200 );

@application.route ( "/delete", methods = ["POST"] )
@jwt_required ( )
def delete ( ):
    if (request.json is None):
        return make_response(jsonify(message="Field email is missing."), 400);

    email = request.json.get("email", "");
    if (len(email) == 0):
        return make_response(jsonify(message="Field email is missing."), 400);
    if (not validation.checkEmail(email)):
        return make_response(jsonify(message="Invalid email."), 400);

    user = User.query.filter(User.email == email).first();
    if (user is None):
        return make_response(jsonify(message="Unknown user."), 400);

    database.session.delete(user);
    database.session.commit();

    return make_response("", 200);
@application.route("/", methods =  ["GET"])
def index():
    return make_response("Hello Authentication", 200);

if ( __name__ == "__main__" ):
    database.init_app ( application );
    application.run ( debug = True, host="0.0.0.0", port = 7000 );
