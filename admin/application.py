from flask import Flask, request, jsonify, make_response;
from flask_jwt_extended import JWTManager;
from sqlalchemy import and_;


from datetime import datetime;

from models import Participant, Election, database, ElectionParticipant, InvalidVote, ValidVote;
import validation;
from UserType import UserType;
from configuration import Configuration;
from authorization_decorator import jwtRoleCheck;


from results import calculateResults

application = Flask ( __name__ );
application.config.from_object ( Configuration );
jwt = JWTManager ( application );

@application.route ( "/createParticipant", methods = ["POST"] )
@jwtRoleCheck(UserType.ADMIN)
def createParticipant():
    if (request.json is None):
        return make_response(jsonify(message="Field name is missing."), 400);
    name = request.json.get("name", "");
    individual = request.json.get("individual", None);


    if (len(name) == 0):
        return make_response(jsonify(message="Field name is missing."),  400);
    if (not validation.checkBool(individual)):
        return make_response(jsonify(message="Field individual is missing."), 400);

    if (len(name) > 256):
        return make_response(jsonify(message="Invalid name."),  400);

    newParticipant = Participant(
        name = name,
        individual = individual
    );
    database.session.add(newParticipant);
    database.session.commit();
    return make_response(jsonify(id=newParticipant.id), 200);


@application.route ( "/getParticipants", methods = ["GET"] )
@jwtRoleCheck(UserType.ADMIN)
def getParticipants():
    participants = Participant.query.all();
    participantList = [];
    for participant in participants:
        participantList.append(
            participant.toDict()
        );
    return make_response(jsonify(participants = participantList), 200);

@application.route ( "/createElection", methods = ["POST"] )
@jwtRoleCheck(UserType.ADMIN)
def createElection():
    if (request.json is None):
        return make_response(jsonify(message="Field start is missing."), 400);

    start = request.json.get("start", "");
    end = request.json.get("end", "");
    individual = request.json.get("individual", None);
    participants = request.json.get("participants", "");


    if (len(start) == 0):
        return make_response(jsonify(message="Field start is missing."),  400);
    if (len(end) == 0):
        return make_response(jsonify(message="Field end is missing."), 400);
    if (not validation.checkBool(individual)):
        return make_response(jsonify(message="Field individual is missing."),  400);
    if (isinstance(participants,str)):
        return make_response(jsonify(message="Field participants is missing."), 400);

    start = validation.parseIsoDateTime(start);
    end = validation.parseIsoDateTime(end);
    print(start)
    print(end)
    if (start is None) or (end is None):
        return make_response(jsonify(message="Invalid date and time."), 400);
    if (start >= end):
        return make_response(jsonify(message="Invalid date and time."), 400);
    #da li je vec zauzet termin
    # if (StartA <= EndB)  and  (EndA >= StartB)
    elections = Election.query.filter(and_(Election.start <= end, Election.end >= start)).first();
    if not (elections is None):
        return make_response(jsonify(message="Invalid date and time."), 400);

    if (not isinstance(participants,list)):
        return make_response(jsonify(message="Invalid participants."), 400);

    if (len(participants) < 2):
        return make_response(jsonify(message="Invalid participants."), 400);


    for p in participants:
        if not isinstance(p, int):
            return make_response(jsonify(message="Invalid participants."), 400);
        participandDB = Participant.query.filter( and_(Participant.id == p, Participant.individual == individual)).first();
        if participandDB is None:
            return make_response(jsonify(message="Invalid participants."), 400);

    newElection = Election(
        start = start,
        end = end,
        individual = individual,
        participantNumber = len(participants)
    );
    database.session.add(newElection);
    database.session.commit();
    idElection = newElection.id;
    i = 1;
    pollList = [];
    newElectionParticipantList = [];
    for p in participants:
        newElectionParticipant = ElectionParticipant(
            pollNumber = i,
            electionId = idElection,
            participantId = p
        );
        pollList.append(i);
        newElectionParticipantList.append(newElectionParticipant);
        i = i + 1;

    database.session.add_all(newElectionParticipantList);
    database.session.commit();
    return make_response(jsonify(pollNumbers = pollList), 200);



@application.route ( "/getElections", methods = ["GET"] )
@jwtRoleCheck(UserType.ADMIN)
def getElections():
    elections = Election.query.all();
    electionList = [];
    for election in elections:
        electionList.append(
            election.toDict()
        );
    return make_response(jsonify(elections = electionList), 200);

@application.route ( "/getResults", methods = ["GET"] )
@jwtRoleCheck(UserType.ADMIN)
def getResults():
    #return make_response(jsonify(message="Field id is missing."), 400);
    id = request.args.get("id");
    print(f"id: {id}");
    if ( (id is None) or (len(id) == 0) ):
        return make_response(jsonify(message = "Field id is missing."), 400);
    if (not validation.allDigits(id)):
        return make_response(jsonify(message = "Election does not exists."), 400);
    election = Election.query.filter(Election.id == id).first();
    if (election is None):
        return make_response(jsonify(message="Election does not exist."), 400);
    now = datetime.now();
    if (election.end > now):
        return make_response(jsonify(message="Election is ongoing."), 400);

    validVotes = ValidVote.query.filter(ValidVote.electionId == id);
    participants = election.participants;
    #print(participants)
    results = calculateResults(election, participants, validVotes)
    #print(results)
    invalidVotes = InvalidVote.query.filter(InvalidVote.electionId == id);
    invalidVotesList = [invalidVote.toDict() for invalidVote in invalidVotes];
    return make_response(jsonify(participants = results, invalidVotes=invalidVotesList), 200);

@application.route("/", methods =  ["GET"])
def index():
    return make_response("Hello Admin", 200);

if ( __name__ == "__main__" ):
    database.init_app ( application );
    application.run ( debug = True, host="0.0.0.0", port = 7000 );