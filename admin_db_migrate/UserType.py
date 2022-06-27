from enum import Enum;

class UserType(str, Enum):
    ADMIN = "ADMIN";
    ELECTION_OFFICIAL = "ELECTION_OFFICIAL";
