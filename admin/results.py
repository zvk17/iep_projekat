def calculatePresidentialResults(election, participants, validVotes):
    voteNumber = len(validVotes);
    votes = [0 for i in range(0, len(participants) + 1)];

    for v in validVotes:
        votes[v.pollNumber] += 1;

    if (voteNumber > 0):
        for i in range(1, len(participants) + 1):
            votes[i] /= voteNumber * 1.0;
    results = [];
    for p in participants:
        dict = p.toDict();
        pollNumber = p.electionParticipant[0].pollNumber;
        results.append({
            "name": dict["name"],
            "result": round(votes[pollNumber], 2),
            "pollNumber": pollNumber
        });


    return results;


def calculateParlamentaryResults(election, participants, validVotes):
    results = [];
    voteNumber = len(validVotes);
    votes = [0 for i in range(0, len(participants) + 1)];
    seats = [0 for i in range(0, len(participants) + 1)];


    for v in validVotes:
        votes[v.pollNumber] += 1;
    #votesCopy = [v for v in votes];
    # cenzus 5%
    for i in range(1, len(participants) + 1):
        q = votes[i] * 1.0 / voteNumber;
        if (q < 0.05):
            votes[i] = 0;

    for i in range(1,251):
        maxId = -1;
        maxQ = -1;
        for i in range(1, len(participants) + 1):
            q = votes[i] * 1.0 / (seats[i] + 1);
            if maxId == -1 or maxQ < q:
                maxQ = q;
                maxId = i;
        seats[maxId] += 1;

    for p in participants:
        dict = p.toDict();
        pollNumber = p.electionParticipant[0].pollNumber;
        results.append({
            "name": dict["name"],
            "result": seats[pollNumber],
            #"votes": votesCopy[pollNumber],
            "pollNumber": pollNumber
        });
    return results;


def calculateResults(election, participants, validVotes):
    validVotesList = [v for v in validVotes];
    participantsList = [e for e in participants];
    if (election.individual):
        return calculatePresidentialResults(election, participantsList, validVotesList);
    else:
        return calculateParlamentaryResults(election, participantsList, validVotesList);
