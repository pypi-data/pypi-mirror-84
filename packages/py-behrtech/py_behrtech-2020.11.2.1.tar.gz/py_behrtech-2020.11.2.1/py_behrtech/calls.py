
import requests
from requests.exceptions import RequestException
from urllib3.exceptions import MaxRetryError, ConnectTimeoutError
from .parsers import Parser
from .exceptions import JWTError, PermissionsError, QueryError


class Calls:
    """
    Is a class for connecting to and accessing messages on BehrTech's industrial gateways
    """

    def __init__(self, username: str, password: str, server_address: str):

        def fetch_jwt_token() -> str:
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

        self.username = username
        self.password = password
        self.server_address = server_address
        self.jwt_token = fetch_jwt_token()

    def __repr__(self):
        return f"Connection to {self.server_address} for user {self.username}"

    def set_username(self, username: str):
        """
        Sets the login username for the given gateway

        :param username: username credential
        """

        self.username = username

    def get_username(self) -> str:
        """
        Returns the username credential for the given gateway

        :return: The username credential for the given gateway
        """

        return self.username

    def set_password(self, password: str):
        """
        Sets the login password for the given gateway

        :param password: password credential
        """

        self.password = password

    def get_password(self) -> str:
        """
        Returns the password credential for the given gateway

        :return: The password credential for the given gateway
        """

        return self.password

    def set_server_address(self, server_address):
        """
        Sets the IP address for the given gateway

        :param server_address: The IP address of the given gateway
        """

        self.server_address = server_address

    def get_server_address(self) -> str:
        """
        Returns the set IP address of the gateway

        :return: The set IP address of the gateway
        """

        return self.server_address

    def test_connection(self) -> bool:
        if self.jwt_token:
            return True
        else:
            return False

    def get_messages(self, return_count: int = '', offset: int = '', epEui: str = '', epName: str = '', bsEui: str = '',
                     sensorType: str = '') -> Parser:
        """
        Returns all messages for every sensor from the gateway.

        :param return_count: The amount of messages to be requested. (-1 for all)
        :param offset: Message number to start the request from
        :param epEui: The epEui number of the sensor to be requested
        :param epName: Endpoint of which messages to be requested. Name is not unique
        :param bsEui: The bsEui number of the messages to be requested
        :param sensorType: The node type of a sensor to be requested
        :return: the requested messages from the gateway
        """

        parameter = ''

        if return_count:
            parameter += f"?returnCount={return_count}"
        if offset:
            parameter += (f"&offset={offset}" if parameter else f"?offset={offset}")
        if epEui:
            parameter += f"&epEui={epEui}" if parameter else f"?epEui={epEui}"
        if epName:
            parameter += f"&epName={epName}" if parameter else f"?epName={epName}"
        if bsEui:
            parameter += f"&bsEui={bsEui}" if parameter else f"?bsEui={bsEui}"
        if sensorType:
            parameter += f"&sensorType={sensorType}" if parameter else f"?sensorType={sensorType}"

        req = requests.get(self.server_address + f"/v2/messages" + parameter,
                           headers={"Authorization": f"Bearer {self.jwt_token}"})

        if req.status_code == 200:
            return Parser(req=req)
        elif req.status_code == 400:
            raise QueryError(url=req.url, message="Endpoint is invalid or was built incorrectly")
        elif req.status_code == 401:
            raise JWTError(message="JWT Access token is missing or invalid")
        elif req.status_code == 403:
            raise PermissionsError(message="User doesn't have the correct permissions to access this data")
        elif req.status_code == 404:
            raise QueryError(url=req.url, message="Endpoint is invalid or was built incorrectly")

    def get_node_models(self) -> Parser:
        """
        Returns data on all setup node models from the gateway.

        :return: the requested data for all node models from the gateway
        """

        message = self.server_address + "/v2/sensormodels"

        return Parser(requests.get(message, headers={"Authorization": f"Bearer {self.jwt_token}"}))

    def get_node_model(self, model_type: str) -> Parser:
        """
        Returns data on a requested node model from the gateway.

        :param model_type: Is the unique identifier of the node model to be requested
        :return: the requested node model data from the gateway
        """

        message = self.server_address + f"/v2/sensormodels/{model_type}"

        return Parser(requests.get(message, headers={"Authorization": f"Bearer {self.jwt_token}"}))

    def get_all_nodes(self, return_count: int, offset: int) -> Parser:
        """
        Returns data on all connected nodes from the gateway.

        :param return_count: Is the amount of nodes to be requested
        :param offset: Is the node count to start the node data request from
        :return: the requested node data from the gateway
        """

        message = self.server_address + f"/v2/nodes?returnCount={return_count}&offset={offset}"

        return Parser(requests.get(message, headers={"Authorization": f"Bearer {self.jwt_token}"}))

    def get_node(self, ep_eui: str) -> Parser:
        """
        Returns data on a requested node from the gateway.

        :param ep_eui: Is the unique identifier of the node to be requested
        :return: the requested node data from the gateway
        """

        message = self.server_address + f"/v2/nodes/{ep_eui}"

        return Parser(requests.get(message, headers={"Authorization": f"Bearer {self.jwt_token}"}))

    def get_MQTT_mappings(self, return_count: int, offset: int) -> Parser:
        """
        Returns data on all setup MQTT Topics from the gateway.

        :param return_count: Is the amount of MQTT Topics to be requested
        :param offset: Is the MQTT Topic count to start the MQTT Topic data request from
        :return: the requested MQTT Topic data from the gateway
        """

        message = self.server_address + f"/v2/mqttmapping?returnCount={return_count}&offset={offset}"

        return Parser(requests.get(message, headers={"Authorization": f"Bearer {self.jwt_token}"}))

    def get_all_MQTT_brokers(self, return_count: int, offset: int) -> Parser:
        """
        Returns data on all setup MQTT Brokers from the gateway.

        :param return_count: Is the amount of MQTT Brokers to be requested
        :param offset: Is the MQTT Broker count to start the MQTT Broker data request from
        :return: the requested MQTT Broker data from the gateway
        """

        message = self.server_address + f"/v2/broker?returnCount={return_count}&offset={offset}"

        return Parser(requests.get(message, headers={"Authorization": f"Bearer {self.jwt_token}"}))

    def get_MQTT_broker(self, broker_id: str) -> Parser:
        """
        Returns data on a requested MQTT Broker from the gateway.

        :param broker_id: Is the unique identifier of the MQTT Broker to be requested
        :return: the requested MQTT Broker data from the gateway
        """

        message = self.server_address + f"/v2/broker/{broker_id}"

        return Parser(requests.get(message, headers={"Authorization": f"Bearer {self.jwt_token}"}))

    def get_auth_ticker(self) -> Parser:
        """
        Returns data on auth ticketers.

        :return: the requested MQTT Topic data from the gateway
        """

        message = self.server_address + "/v2/auth/ticket"

        return Parser(requests.get(message, headers={"Authorization": f"Bearer {self.jwt_token}"}))

    def get_gateway_data(self) -> Parser:
        """
        Returns data on the configured gateways.

        :return: the requested gateway data
        """

        message = self.server_address + "/v2/system"

        return Parser(requests.get(message, headers={"Authorization": f"Bearer {self.jwt_token}"}))

    def get_azure_mapping(self) -> Parser:
        """
        Returns data for setup Azure connections on the gateway.

        :return: the requested Azure connection data
        """

        message = self.server_address + "/v2/azuremapping"

        return Parser(requests.get(message, headers={"Authorization": f"Bearer {self.jwt_token}"}))
