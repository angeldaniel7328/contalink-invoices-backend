import os
from datetime import timedelta

from dotenv import load_dotenv

from sqlalchemy.engine import URL

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername= "postgresql+psycopg2",
        username= os.getenv("DB_USER"),
        password= os.getenv("DB_PASSWORD"),
        host= os.getenv("DB_HOST"),
        port= os.getenv("DB_PORT", 5432),
        database= os.getenv("DB_NAME"),
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    MAIL_TO = os.getenv("MAIL_RECIPIENT")


class ConfigTest:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_SESSION_OPTIONS = {"expire_on_commit": False}
    JWT_SECRET_KEY = "test-secret-key"