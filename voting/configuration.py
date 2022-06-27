from datetime import timedelta;
import os;

if ("DATABASE_URL" in os.environ):
    databaseUrl = os.environ["DATABASE_URL"];
else:
    databaseUrl = "localhost";
if ("REDIS_HOST" in os.environ):
    redisHost = os.environ["REDIS_HOST"];
else:
    redisHost = "localhost";

class Configuration ( ):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{databaseUrl}/admin";
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta ( hours = 1 );
    JWT_REFRESH_TOKEN_EXPIRES = timedelta ( days = 30 );
    REDIS_HOST = redisHost;
    REDIS_VOTE_LIST = "VOTE_LIST";