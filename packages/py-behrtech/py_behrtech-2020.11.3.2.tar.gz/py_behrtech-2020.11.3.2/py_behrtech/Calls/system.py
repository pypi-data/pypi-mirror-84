
import requests
from requests.exceptions import RequestException
from urllib3.exceptions import MaxRetryError, ConnectTimeoutError

from py_behrtech.exceptions import JWTError


class System:

    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = None
        self.jwt_token = None

    def login(self) -> str:
        """
        Gets the JWT token of the login endpoint.
        """
        try:
            res = requests.post(
                self.server_address + "/v2/login",
                json={'user': self.username, 'password': self.password},
                timeout=3
            )

            if res.status_code == 200:
                # Successfully logged in
                return res.json().get("JWT")
            elif res.status_code == 401:
                # Credentials provided are incorrect
                raise JWTError(message="The wrong server IP address or login credentials were provided")

        except (TimeoutError, ConnectTimeoutError, MaxRetryError, RequestException):
            raise JWTError(message="The wrong server IP address or login credentials were provided")
