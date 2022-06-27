from flask import Flask;

from UserType import UserType;
from configuration import Configuration;
from flask_migrate import Migrate, init, migrate, upgrade;
from authentication.models import database, User;
from sqlalchemy_utils import database_exists, create_database;

application = Flask ( __name__ );
application.config.from_object ( Configuration );

migrateObject = Migrate ( application, database );

if ( not database_exists ( application.config["SQLALCHEMY_DATABASE_URI"] ) ):
    create_database ( application.config["SQLALCHEMY_DATABASE_URI"] );

database.init_app ( application );

with application.app_context ( ) as context:
    init ( );
    migrate ( message = "Production migration" );
    upgrade ( );

    admin = User (
            jmbg = "0000000000000",
            email = "admin@admin.com",
            password = "1",
            forename = "admin",
            surname = "admin",
            userType=UserType.ADMIN
    );

    database.session.add ( admin );
    database.session.commit ( );

