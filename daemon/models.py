from flask_sqlalchemy import SQLAlchemy;
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session

from configuration import Configuration;

engine = create_engine(Configuration.SQLALCHEMY_DATABASE_URI, echo=True);
session = scoped_session(sessionmaker(bind=engine));
DBSession = session;
class _Base(object):
    query = DBSession.query_property()

Model = declarative_base(cls=_Base)



class ElectionParticipant( Model ):
    __tablename__ = "election_participant";

    id = Column(Integer, primary_key=True);
    pollNumber = Column(Integer, nullable = False);
    electionId = Column(Integer, ForeignKey("elections.id"), nullable=False);
    participantId = Column(Integer, ForeignKey("participants.id"), nullable=False);
    participant = relationship("Participant", back_populates="electionParticipant");

class Participant( Model ):
    __tablename__  = "participants";

    id = Column ( Integer, primary_key = True);
    name = Column( String(256), nullable = False);
    individual = Column( Boolean, nullable = False);
    elections = relationship("Election", secondary=ElectionParticipant.__table__,  back_populates="participants");
    electionParticipant = relationship("ElectionParticipant", back_populates="participant");
    def toDict(self):
        return {
            "id": self.id,
            "individual": self.individual,
            "name": self.name
        }

class Election( Model ):
    __tablename__ = "elections";

    id = Column(Integer, primary_key=True);
    individual = Column(Boolean, nullable=False);
    start = Column(DateTime(), nullable = False);
    end = Column(DateTime(), nullable = False);
    participants = relationship("Participant", secondary=ElectionParticipant.__table__, back_populates="elections");
    participantNumber = Column(Integer, nullable=False);

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
class ValidVote( Model ):
    __tablename__ = "valid_votes";
    id = Column(Integer, primary_key=True);
    ballotGuid = Column(String(60), nullable=False);
    electionOfficialJmbg = Column(String(13), nullable=False);
    pollNumber = Column(Integer, nullable=False);
    electionId = Column(Integer, ForeignKey("elections.id"), nullable=False);

class InvalidVote( Model ):
    __tablename__ = "invalid_votes";
    id = Column(Integer, primary_key = True);
    pollNumber = Column(Integer, nullable = False);
    ballotGuid = Column( String(60), nullable = False);
    electionOfficialJmbg = Column ( String(13), nullable  = False);
    electionId = Column(Integer, ForeignKey("elections.id"), nullable=False);
    reason = Column( String(256), nullable = False);

    def toDict(self):
        return {
            "electionOfficialJmbg": self.electionOfficialJmbg,
            "ballotGuid": self.ballotGuid,
            "pollNumber": self.pollNumber,
            "reason": self.reason
        }