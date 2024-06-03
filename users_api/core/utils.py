from .interfaces import SingletonMeta
from pathlib import Path
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import configparser
import os

file_path = Path('./env.cfg')


class EnvManager(metaclass=SingletonMeta):
    """ My custom environment manager """

    def __init__(self):
        self.env = None
        self.__get_dev_env()

    def get_env(self, key: str, default=None):
        """ Used to avoid install an external library for dev env files
        Parameters:
            key (str): The name of the environment variable to retrieve.
            default (any): The default value to return if the environment
                variable is not found. Default is None.
        Returns:
            The value of the environment variable if it is found, otherwise
            the default value.
        """
        if self.env:
            return self.env.get(key, default)
        return os.getenv(key, default)

    def __get_dev_env(self):
        """ If file exist then we are using dev environment
        otherwise we need to get variables from OS env variables
        over the [self.get_env] function """
        if file_path.exists():
            config = configparser.ConfigParser()
            config.read(file_path)
            self.env = config['Settings']


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        session_cookie = request.cookies.get("session_token")
        if session_cookie:
            # Set the Authorization header
            request.headers.__dict__["_list"].append(
                (b"authorization", f"Bearer {session_cookie}".encode())
            )
        response = await call_next(request)
        return response
