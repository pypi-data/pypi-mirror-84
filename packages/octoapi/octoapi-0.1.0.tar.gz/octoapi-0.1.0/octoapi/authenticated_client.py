import requests
from .exceptions import ApiException
from .types import JSONType


class AuthenticatedClient:
    """Base class for making authenticated requests to the remote API"""

    API_BASE_URL = "https://api.octopus.energy/v1"

    def __init__(self, api_key: str) -> None:
        self.session = requests.Session()
        self.session.auth = (api_key, "")

    def request_json(self, path: str, params: dict = None) -> JSONType:
        """Make a request against the Octopus API"""
        request_url = "/".join([self.API_BASE_URL, path.lstrip("/")])
        if not params:
            params = {}
        try:
            response = self.session.request(
                method="GET", url=request_url, params=params
            )
            response.raise_for_status()
        except requests.RequestException as exception:
            raise ApiException("Unexpected response exception") from exception

        return response.json()
