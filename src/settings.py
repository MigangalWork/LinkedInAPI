from os import environ
from dotenv import load_dotenv, find_dotenv

class Env:

    DATABASE_HOST: str
    DATABASE_PASSWORD: str

    @classmethod
    def main_set_env(cls):
        cls._get_env()
        cls._set_variables()

    @classmethod
    def _get_env(cls):
        load_dotenv(find_dotenv(".env"))

    @classmethod
    def _set_variables(cls):
        cls.DATABASE_HOST = environ.get("DATABASE_HOST")
        cls.DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD")
        cls.WEBHOOK_URL = environ.get("WEBHOOK_URL")
        cls.LINKEDIN_API_URL = environ.get("LINKEDIN_API_URL")
        cls.HOST = environ.get("HOST")
        cls.PORT = environ.get("PORT")
        cls.RELOAD = environ.get("RELOAD")
