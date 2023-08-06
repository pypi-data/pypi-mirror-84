
import requests

from py_behrtech.parsers import Parser
from py_behrtech.exceptions import JWTError, PermissionsError, QueryError


class Models:

    def __init__(self):
        self.username = None
        self.password = None
        self.server_address = None
        self.jwt_token = None
        self.req = None

    @property
    def check_status_code(self):
        if self.req.status_code == 400:
            raise QueryError(url=self.req.url, message="Endpoint is invalid or was built incorrectly")
        elif self.req.status_code == 401:
            raise JWTError(message="JWT Access token is missing or invalid")
        elif self.req.status_code == 403:
            raise PermissionsError(message="User doesn't have the correct permissions to access this data")
        elif self.req.status_code == 404:
            raise QueryError(url=self.req.url, message="Endpoint is invalid or was built incorrectly")

    def models_delete(self):
        pass

    def models_get(self, return_count: int = '', offset: int = ''):
        """
        Gets information on all registered node models from the gateway.

        :return: Requested data for all node models from the gateway
        """

        parameters = ''

        if return_count:
            parameters += f"?returnCount={return_count}"
        if offset:
            parameters += (f"&offset={offset}" if parameters else f"?offset={offset}")

        self.req = requests.get(url=self.server_address + f"/v2/sensormodels" + parameters,
                                headers={"Authorization": f"Bearer {self.jwt_token}"})

        if self.req.status_code == 200:
            return Parser(req=self.req)
        else:
            self.check_status_code()

    def models_post(self):
        pass

    def models_type_delete(self):
        pass

    def models_type_get(self, model_type: str):
        """
        Gets information on a requested registered node model from the gateway

        :param model_type: Unique identifier of the node model to be requested
        :return: Requested node model data from the gateway
        """

        self.req = requests.get(url=self.server_address + f"/v2/sensormodels/{model_type}",
                                headers={"Authorization": f"Bearer {self.jwt_token}"})

        if self.req.status_code == 200:
            return Parser(req=self.req)
        else:
            self.check_status_code()

    def models_type_post(self):
        pass
