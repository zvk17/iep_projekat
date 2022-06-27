from flask_sqlalchemy import SQLAlchemy;


database = SQLAlchemy ( );

class ElectionParticipant( database.Model ):
    __tablename__ = "election_participant";

    id = database.Column(database.Integer, primary_key=True);
    pollNumber = database.Column(database.Integer, nullable = False);
    electionId = database.Column(database.Integer, database.ForeignKey("elections.id"), nullable=False);
    participantId = database.Column(database.Integer, database.ForeignKey("participants.id"), nullable=False);
    participant = database.relationship("Participant", back_populates="electionParticipant");

class Participant( database.Model ):
    __tablename__  = "participants";

    id = database.Column ( database.Integer, primary_key = True);
    name = database.Column( database.String(256), nullable = False);
    individual = database.Column( database.Boolean, nullable = False);
    elections = database.relationship("Election", secondary=ElectionParticipant.__table__,  back_populates="participants");
    electionParticipant = database.relationship("ElectionParticipant", back_populates="participant");
    def toDict(self):
        return {
            "id": self.id,
            "individual": self.individual,
            "name": self.name
        }

class Election( database.Model ):
    __tablename__ = "elections";

    id = database.Column(database.Integer, primary_key=True);
    individual = database.Column(database.Boolean, nullable=False);
    start = database.Column(database.DateTime(), nullable = False);
    end = database.Column(database.DateTime(), nullable = False);
    participants = database.relationship("Participant", secondary=ElectionParticipant.__table__, back_populates="elections");
    participantNumber = database.Column(database.Integer, nullable=False);

    def toDict(self):
        participantsList = [];
        for p in self.participants:
            pDict = p.toDict();
            del pDict["individual"];
            participantsList.append(pDict);
        return {
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "id": self.id,
            "individual": self.individual,
            "participants": participantsList
        }
class ValidVote( database.Model ):
    __tablename__ = "valid_votes";
    id = database.Column(database.Integer, primary_key=True);
    ballotGuid = database.Column(database.String(60), nullable=False);
    electionOfficialJmbg = database.Column(database.String(13), nullable=False);
    pollNumber = database.Column(database.Integer, nullable=False);
    electionId = database.Column(database.Integer, database.ForeignKey("elections.id"), nullable=False);

class InvalidVote( database.Model ):
    __tablename__ = "invalid_votes";
    id = database.Column(database.Integer, primary_key = True);
    pollNumber = database.Column(database.Integer, nullable = False);
    ballotGuid = database.Column( database.String(60), nullable = False);
    electionOfficialJmbg = database.Column ( database.String(13), nullable  = False);
    electionId = database.Column(database.Integer, database.ForeignKey("elections.id"), nullable=False);
    reason = database.Column( database.String(256), nullable = False);

    def toDict(self):
        return {
            "electionOfficialJmbg": self.electionOfficialJmbg,
            "ballotGuid": self.ballotGuid,
            "pollNumber": self.pollNumber,
            "reason": self.reason
        }