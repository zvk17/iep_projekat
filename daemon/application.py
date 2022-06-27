import json;
import validation;
from sqlalchemy import and_;
import time;

from redis import Redis;
from models import ValidVote, Election, InvalidVote;
from models import session;
from configuration import Configuration;


#application = Flask ( __name__ );
#application.config.from_object ( Configuration );
#if ( __name__ == "__main__" ):
#    database.init_app ( application );
#    application.run ( debug = True, port = 5005 );
#

while True:
    try:
        with Redis(host=Configuration.REDIS_HOST) as redis:
            while True:
                votesNumber = redis.llen(Configuration.REDIS_VOTE_LIST);
                print(f"Votes number: {votesNumber}");
                if (votesNumber == 0):
                    time.sleep(1);
                else:
                    while True:
                        vote = redis.lpop(Configuration.REDIS_VOTE_LIST);
                        if (vote is None):
                            break;
                        if (isinstance(vote, bytes)):
                            vote = vote.decode("utf-8");
                        vote = json.loads(vote);

                        guid = vote["guid"];
                        datetime = validation.parseIsoDateTime(vote["datetime"]);
                        pollNumber = vote["pollNumber"];
                        jmbg = vote["jmbg"];
                        election = Election.query.filter(
                            and_(Election.start <= datetime, Election.end >= datetime)).first();

                        if (election is None):
                            continue;
                        electionId = election.id;
                        if (election.participantNumber < pollNumber):
                            newInvalidVote = InvalidVote(

                                ballotGuid=guid,
                                electionOfficialJmbg=jmbg,
                                electionId=electionId,
                                pollNumber=pollNumber,
                                reason="Invalid poll number."
                            );

                            session.add(newInvalidVote);
                            session.commit();
                            continue;

                        duplicate = ValidVote.query.filter(
                            and_(ValidVote.ballotGuid == guid, ValidVote.electionId == electionId)
                        ).first();
                        if (not (duplicate is None)):
                            newInvalidVote = InvalidVote(

                                ballotGuid=guid,
                                electionOfficialJmbg=jmbg,
                                electionId=electionId,
                                pollNumber=pollNumber,
                                reason="Duplicate ballot."
                            );
                            session.add(newInvalidVote);
                            session.commit();
                            continue;

                        newValidVote = ValidVote(
                            ballotGuid=guid,
                            electionOfficialJmbg=jmbg,
                            electionId=electionId,
                            pollNumber=pollNumber
                        )
                        session.add(newValidVote);
                        session.commit();
                        # time.sleep(10)
          # probaj ponovo da se konektujes na redis server
    except:
        time.sleep(2)
        print("no connection")