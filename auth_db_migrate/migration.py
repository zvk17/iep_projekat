import time
from flask import Flask;
from flask_migrate import Migrate, init, migrate, upgrade;
from sqlalchemy_utils import database_exists, create_database;

from models import database, User;
from UserType import UserType;
from configuration import Configuration;

application = Flask ( __name__ );
application.config.from_object ( Configuration );

migrateObject = Migrate ( application, database );

done = False;
counter = 0;
while not done:
    try:
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
        done = True;
    except:
        counter += 1;
        if (counter > 60):
            break;
        time.sleep(2);