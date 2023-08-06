
import requests

from py_behrtech.parsers import Parser
from py_behrtech.exceptions import JWTError, PermissionsError, QueryError


class Messages:

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

    def messages_delete(self, deleteAll: bool = False):
        """
        Deletes all messages from the gateways

        :param deleteAll: Verifies deletion was on purpose
        :return:
        """

        self.req = requests.delete(url=self.server_address + f"/v2/messages", params={'deleteAll': deleteAll},
                                   headers={"Authorization": f"Bearer {self.jwt_token}"})

        if self.req.status_code == 200:
            return Parser(req=self.req)
        else:
            self.check_status_code()

    def messages_get(self, return_count: int = '', offset: int = '', epEui: str = '', epName: str = '', bsEui: str = '',
                     sensorType: str = '') -> Parser:
        """
        Returns messages from the gateway.

        :param return_count: The amount of messages to be requested. (-1 for all)
        :param offset: Message number to start the request from
        :param epEui: The epEui number of the sensor to be requested
        :param epName: Endpoint of which messages to be requested. Name is not unique
        :param bsEui: The bsEui number of the messages to be requested
        :param sensorType: The node type of a sensor to be requested
        :return: Parser object
        """

        parameters = ''

        if return_count:
            parameters += f"?returnCount={return_count}"
        if offset:
            parameters += (f"&offset={offset}" if parameters else f"?offset={offset}")
        if epEui:
            parameters += f"&epEui={epEui}" if parameters else f"?epEui={epEui}"
        if epName:
            parameters += f"&epName={epName}" if parameters else f"?epName={epName}"
        if bsEui:
            parameters += f"&bsEui={bsEui}" if parameters else f"?bsEui={bsEui}"
        if sensorType:
            parameters += f"&sensorType={sensorType}" if parameters else f"?sensorType={sensorType}"

        self.req = requests.get(url=self.server_address + f"/v2/messages" + parameters,
                                headers={"Authorization": f"Bearer {self.jwt_token}"})

        if self.req.status_code == 200:
            return Parser(req=self.req)
        else:
            self.check_status_code()

    def messages_post(self):
        # TODO: build this function
        pass
