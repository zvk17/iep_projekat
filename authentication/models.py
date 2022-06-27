from flask_sqlalchemy import SQLAlchemy;
from UserType import UserType;
database = SQLAlchemy ( );



class User( database.Model ):
    __tablename__  = "users";

    id = database.Column ( database.Integer, primary_key = True);
    jmbg = database.Column ( database.String(13), nullable  = False);
    forename = database.Column(database.String(256), nullable=False);
    surname = database.Column(database.String(256), nullable=False);
    email = database.Column(database.String(256), nullable=False, unique = True);
    password = database.Column(database.String(256), nullable=False);
    userType = database.Column(database.Enum(UserType), nullable = False);

    def __repr__(self):
        return self.forename + " " + self.surname + " " + self.jmbg + " " + self.email + " " + self.password + " " + self.type;
