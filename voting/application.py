import csv;
import io;
import json;
from datetime import datetime

from flask import Flask, request, jsonify, make_response;
from flask_jwt_extended import JWTManager, get_jwt;
from redis import Redis;
from sqlalchemy import and_;

from UserType import UserType;
from configuration import Configuration;
from authorization_decorator import jwtRoleCheck;
from models import Participant, Election, database, ElectionParticipant;
import validation;

application = Flask ( __name__ );
application.config.from_object ( Configuration );
jwt = JWTManager ( application );


@application.route ( "/vote", methods = ["POST"] )
@jwtRoleCheck(UserType.ELECTION_OFFICIAL)
def vote():
    claims = get_jwt();
    jmbg = claims["jmbg"];
    if ( not ("file" in request.files) ):
        return make_response(jsonify(message = "Field file is missing."), 400);
    file = request.files["file"];
    content = file.stream.read ( ).decode ( "utf-8" );
    stream = io.StringIO(content);
    reader = csv.reader(stream);

    voteList = [];
    lineNumber = 0;
    now = datetime.now();
    #print("readin")
    for row in reader:
        if (len(row) != 2):
            return make_response(jsonify(message=f"Incorrect number of values on line {lineNumber}."), 400);
        elif ( ( not validation.allDigits(row[1]) ) or (not  (int(row[1]) > 0) ) ):
            return make_response(jsonify(message=f"Incorrect poll number on line {lineNumber}."), 400);
        else:
            vote = {
                "guid": row[0],
                "pollNumber": int(row[1]),
                "datetime": now.isoformat(),
                "jmbg": jmbg
            };
            voteList.append(vote);
            lineNumber = lineNumber + 1;
    print("redis start")
    i = 0;
    with Redis (host = Configuration.REDIS_HOST) as redis:
        print("connected to redis")
        #print(redis)
        for vote in voteList:
            v = jsonify(vote).get_data()
            redis.rpush(Configuration.REDIS_VOTE_LIST, json.dumps(vote));
    #print(f"Number of lines: {lineNumber}");
    #redis slanje na server
    return make_response("", 200);
@application.route("/", methods =  ["GET"])
def index():
    return make_response("Hello Authentication", 200);

if ( __name__ == "__main__" ):
    database.init_app ( application );
    application.run ( debug = True, host = "0.0.0.0", port = 7000 );