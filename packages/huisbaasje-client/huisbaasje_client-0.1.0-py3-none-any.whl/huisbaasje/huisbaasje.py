import asyncio
import aiohttp
import async_timeout
from yarl import URL

from .const import API_HOST, AUTHENTICATION_PATH, DEFAULT_SOURCE_TYPES, SOURCES_PATH, AUTH_TOKEN_HEADER, ACTUALS_PATH
from .exceptions import HuisbaasjeConnectionException, HuisbaasjeException, HuisbaasjeUnauthenticatedException


class Huisbaasje:
    """Client to connect with Huisbaasje"""

    def __init__(self,
                 username: str,
                 password: str,
                 api_scheme: str = "https",
                 api_host: str = API_HOST,
                 api_port: int = 443,
                 request_timeout: int = 10,
                 source_types=DEFAULT_SOURCE_TYPES):
        self.api_scheme = api_scheme
        self.api_host = api_host
        self.api_port = api_port
        self.request_timeout = request_timeout
        self.source_types = source_types

        self._username = username
        self._password = password
        self._user_id = None
        self._auth_token = None
        self._sources = None

    async def authenticate(self) -> None:
        """Log in using username and password.

        If succesfull, the authentication is saved and is_authenticated() returns true
        """
        url = URL.build(scheme=self.api_scheme, host=self.api_host, port=self.api_port, path=AUTHENTICATION_PATH)
        data = {"loginName": self._username, "password": self._password}

        return await self.request("POST", url, data=data, callback=self._handle_authenticate_response)

    async def _handle_authenticate_response(self, response):
        json = await response.json()
        self._auth_token = response.headers.get(AUTH_TOKEN_HEADER)
        self._user_id = json["userId"]

    async def sources(self):
        """Request the sources."""
        if not self.is_authenticated():
            raise HuisbaasjeUnauthenticatedException("Authentication required")

        url = URL.build(scheme=self.api_scheme, host=self.api_host, port=self.api_port, path=(SOURCES_PATH % self._user_id))

        return await self.request("GET", url, callback=self._handle_sources_response)

    async def _handle_sources_response(self, response):
        json = await response.json()
        self._sources = dict()
        for source in json["sources"]:
            self._sources[source["type"]] = source["source"]

    async def actuals(self):
        """Request the actual values of the sources of the types configured in this instance (source_types)."""
        if not self.is_authenticated():
            raise HuisbaasjeUnauthenticatedException("Authentication required")

        source_ids = self.get_source_ids()

        query = {"sources": ",".join(source_ids)}
        url = URL.build(scheme=self.api_scheme, host=self.api_host, port=self.api_port, path=(ACTUALS_PATH % self._user_id), query=query)

        return await self.request("GET", url, callback=self._handle_actuals_response)

    async def _handle_actuals_response(self, response):
        json = await response.json()
        actuals = dict()
        for actual in json["actuals"]:
            actuals[actual["type"]] = actual

        return actuals

    async def current_measurements(self):
        """Wrapper method which returns the relevant actual values of sources.

        When required, this method attempts to authenticate."""
        try:
            if not self.is_authenticated():
                await self.authenticate()

            if self._sources is None:
                await self.sources()

            actuals = await self.actuals()
            current_measurements = dict()

            for source_type, actual in actuals.items():
                measurements = actual["measurements"]

                current_measurements[source_type] = {
                    "measurement": max(measurements, key=lambda item: item["time"]) if measurements else None,
                    "thisDay": actual["thisDay"],
                    "thisWeek": actual["thisWeek"],
                    "thisMonth": actual["thisMonth"],
                    "thisYear": actual["thisYear"]
                }

            return current_measurements
        except HuisbaasjeUnauthenticatedException as exception:
            self.invalidate_authentication()
            raise exception

    async def request(self, method: str, url: str, data: dict = None, callback=None):
        headers = {"Accept": "application/json"}

        # Insert authentication
        if self._auth_token is not None:
            headers[AUTH_TOKEN_HEADER] = self._auth_token

        try:
            with async_timeout.timeout(self.request_timeout):
                async with aiohttp.ClientSession() as session:
                    async with session.request(method, url, json=data, headers=headers, ssl=True) as response:
                        status = response.status
                        is_json = "application/json" in response.headers.get("Content-Type", "")

                        if status == 401:
                            raise HuisbaasjeUnauthenticatedException(await response.text())

                        if not is_json:
                            raise HuisbaasjeException("Response is not json", await response.text())

                        if not is_json or (status // 100) in [4, 5]:
                            raise HuisbaasjeException("Response is not success", response.status, await response.text())

                        if callback is not None:
                            return await callback(response)

        except asyncio.TimeoutError as exception:
            raise HuisbaasjeConnectionException("Timeout occurred while communicating with Huisbaasje") from exception
        except aiohttp.ClientError as exception:
            raise HuisbaasjeConnectionException("Error occurred while communicating with Huisbaasje") from exception

    def is_authenticated(self):
        """Returns whether this instance is authenticated

        Note: despite this method returning true, requests could still fail to an authentication error."""
        return self._user_id is not None and self._auth_token is not None

    def get_user_id(self):
        """Returns the unique id of the currently authenticated user"""
        return self._user_id

    def invalidate_authentication(self):
        """Invalidate the current authentication tokens."""
        self._user_id = None
        self._auth_token = None

    def get_source_ids(self):
        """Gets the ids of the sources which belong to self.source_types, if present."""
        return [source_id for source_id in map(self.get_source_id, self.source_types) if source_id is not None]

    def get_source_id(self, source_type):
        """Gets the id of the source which belongs to the given source type, if present."""
        return self._sources[source_type] if source_type in self._sources else None
