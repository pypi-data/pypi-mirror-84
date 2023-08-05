
import json
import requests
from requests import Response
from requests.exceptions import RequestException
from urllib3.exceptions import MaxRetryError, ConnectTimeoutError


class ApiCall:
    """
    Is a class for connecting to and accessing messages on BehrTech's industrial gateways
    """

    def __init__(self, username: str, password: str, server_address: str):
        self.username = username
        self.password = password
        self.server_address = server_address

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

        # Retrieves the JWT Token of the gateway computer
        if self.fetch_jwt_token:
            return True
        else:
            return False

    @property
    def fetch_jwt_token(self) -> str:
        """
        Gets the JWT token of the login endpoint.
        """
        try:
            res = requests.post(self.server_address + "/v2/login",
                                json={'user': self.username, 'password': self.password}, timeout=3)

            if res:
                results: dict = res.json()

                return results.get("JWT")

        except (TimeoutError, ConnectTimeoutError, MaxRetryError, RequestException):
            print("The wrong server IP address or login credentials were provided")

    def get_all_sensor_data(self, return_count: int, offset: int) -> Response:
        """
        Returns all messages for every sensor from the gateway.

        :param return_count: Is the amount of messages to be requested
        :param offset: Is the message count to start the message request from
        :return: the requested messages from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token

        message = self.server_address + f"/v2/messages?returnCount={return_count}&offset={offset}"

        return requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

    def get_sensor_data(self, return_count: int, offset: int, eui: str) -> Response:
        """
        Returns sensor messages from the gateway for a given sensor.

        :param return_count: Is the amount of messages to be requested for the given sensor
        :param offset: Is the message count to start the message request from
        :param eui: Is the identification EUI number of the sensor to be requested.
        :return: the requested message from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token

        message = self.server_address + f"/v2/messages?returnCount={return_count}&offset={offset}&epEui={eui}"

        return requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

    def get_node_models(self) -> Response:
        """
        Returns data on all setup node models from the gateway.

        :return: the requested data for all node models from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token

        message = self.server_address + "/v2/sensormodels"

        return requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

    def get_node_model(self, model_type: str) -> Response:
        """
        Returns data on a requested node model from the gateway.

        :param model_type: Is the unique identifier of the node model to be requested
        :return: the requested node model data from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token

        message = self.server_address + f"/v2/sensormodels/{model_type}"

        return requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

    def get_all_nodes(self, return_count: int, offset: int) -> Response:
        """
        Returns data on all connected nodes from the gateway.

        :param return_count: Is the amount of nodes to be requested
        :param offset: Is the node count to start the node data request from
        :return: the requested node data from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token

        message = self.server_address + f"/v2/nodes?returnCount={return_count}&offset={offset}"

        return requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

    def get_node(self, ep_eui: str) -> Response:
        """
        Returns data on a requested node from the gateway.

        :param ep_eui: Is the unique identifier of the node to be requested
        :return: the requested node data from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token

        message = self.server_address + f"/v2/nodes/{ep_eui}"

        return requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

    def get_MQTT_mappings(self, return_count: int, offset: int) -> Response:
        """
        Returns data on all setup MQTT Topics from the gateway.

        :param return_count: Is the amount of MQTT Topics to be requested
        :param offset: Is the MQTT Topic count to start the MQTT Topic data request from
        :return: the requested MQTT Topic data from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token

        message = self.server_address + f"/v2/mqttmapping?returnCount={return_count}&offset={offset}"

        return requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

    def get_all_MQTT_brokers(self, return_count: int, offset: int) -> Response:
        """
        Returns data on all setup MQTT Brokers from the gateway.

        :param return_count: Is the amount of MQTT Brokers to be requested
        :param offset: Is the MQTT Broker count to start the MQTT Broker data request from
        :return: the requested MQTT Broker data from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token

        message = self.server_address + f"/v2/broker?returnCount={return_count}&offset={offset}"

        return requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

    def get_MQTT_broker(self, broker_id: str) -> Response:
        """
        Returns data on a requested MQTT Broker from the gateway.

        :param broker_id: Is the unique identifier of the MQTT Broker to be requested
        :return: the requested MQTT Broker data from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token

        message = self.server_address + f"/v2/broker/{broker_id}"

        return requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

    def get_auth_ticker(self) -> Response:
        """
        Returns data on auth ticketers.

        :return: the requested MQTT Topic data from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token

        message = self.server_address + "/v2/auth/ticket"

        return requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

    def get_gateway_data(self) -> Response:
        """
        Returns data on the configured gateways.

        :return: the requested gateway data
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token

        message = self.server_address + "/v2/system"

        return requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

    def get_azure_mapping(self) -> Response:
        """
        Returns data for setup Azure connections on the gateway.

        :return: the requested Azure connection data
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token

        message = self.server_address + "/v2/azuremapping"

        return requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

    def get_components(self, ep_eui: str) -> list:
        """
        Returns a list of measured components for the specified sensor

        :param ep_eui:  The unique identifier of a node
        :return: List of measured components
        """

        sens_type = json.loads(self.get_node(ep_eui=ep_eui).text).get('type')
        components = json.loads(self.get_node_model(model_type=sens_type).text).get('components')

        return [x for x in components]

    def get_units(self, ep_eui: str) -> dict:
        """
        Returns a dict of units for measured components for the specified sensor

        :param ep_eui: The unique identifier of a node
        :return: Dict of units for measured components
        """

        sens_type = json.loads(self.get_node(ep_eui=ep_eui).text).get('type')
        components = json.loads(self.get_node_model(model_type=sens_type).text).get('components')

        return {x: components.get(x)['unit'] for x in components}
