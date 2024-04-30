from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

PORT = os.environ.get("POSTGRESQL_PORT")
DATABASE = os.environ.get("POSTGRESQL_DATABASE")
USER = os.environ.get("POSTGRESQL_USER")
HOST = os.environ.get("POSTGRESQL_HOST")
PASSWORD = os.environ.get("POSTGRESQL_PASSWORD")

URL_DATABASE = "postgresql://{}:{}@{}:{}/{}".format(
    USER, PASSWORD, HOST, PORT, DATABASE
)

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
