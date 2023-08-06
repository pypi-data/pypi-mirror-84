"""Main class for the Crownstone cloud cloud."""
import logging
import asyncio
import aiohttp
from typing import Optional
from crownstone_cloud.helpers.conversion import password_to_hash
from crownstone_cloud.cloud_models.crownstones import Crownstone
from crownstone_cloud.cloud_models.spheres import Spheres
from crownstone_cloud.helpers.requests import RequestHandler

_LOGGER = logging.getLogger(__name__)


class CrownstoneCloud:
    """Create a Crownstone cloud instance."""

    def __init__(self, email: str, password: str, clientsession: aiohttp.ClientSession = None) -> None:
        # Create request handler instance
        self.request_handler = RequestHandler(self, clientsession)
        # Instance data
        self.login_data = {'email': email, 'password': password_to_hash(password)}
        self.access_token: Optional[str] = None
        self.cloud_data: Optional[Spheres] = None

    async def async_initialize(self) -> None:
        """
        Login to Crownstone API & synchronize all cloud data.

        This method is a coroutine.
        """
        # Login
        login_response = await self.request_handler.request_login(self.login_data)

        # Save access token & create cloud data object
        self.access_token = login_response['id']
        self.cloud_data = Spheres(self, login_response['userId'])
        _LOGGER.debug("Login to Crownstone Cloud successful")

        # Synchronize data
        await self.async_synchronize()

    async def async_synchronize(self) -> None:
        """
        Sync all data from cloud.

        This method is a coroutine.
        """
        _LOGGER.debug("Initiating all cloud data")
        # get the sphere data for this user_id
        await self.cloud_data.async_update_sphere_data()

        # get the data from the sphere attributes
        for sphere in self.cloud_data:
            await asyncio.gather(
                sphere.async_update_sphere_presence(),
                sphere.crownstones.async_update_crownstone_data(),
                sphere.locations.async_update_location_data(),
                sphere.locations.async_update_location_presence(),
                sphere.users.async_update_user_data()
            )
        _LOGGER.debug("Cloud data successfully initialized")

    def get_crownstone(self, crownstone_name) -> Crownstone:
        """
        Get a crownstone by name without specifying a sphere.

        :param crownstone_name: Name of the Crownstone.
        :return: Crownstone object.
        """
        try:
            for sphere in self.cloud_data:
                for crownstone in sphere.crownstones:
                    if crownstone.name == crownstone_name:
                        return crownstone
        except KeyError:
            _LOGGER.exception("This login_id does not exist. Use 'async_login' to login.")
        except ValueError:
            _LOGGER.exception("No sphere data available for this login. Use 'async_synchronize' to load user data.")

    def get_crownstone_by_id(self, crownstone_id) -> Crownstone:
        """
        Get a crownstone by id without specifying a sphere.

        :param crownstone_id: The cloud id of the Crownstone.
        :return: Crownstone object.
        """
        try:
            for sphere in self.cloud_data:
                return sphere.crownstones[crownstone_id]
        except KeyError:
            _LOGGER.exception("This login_id does not exist. Use 'async_login' to login.")
        except ValueError:
            _LOGGER.exception("No sphere data available for this login. Use 'async_synchronize' to load user data.")

    async def async_close_session(self) -> None:
        """
        Close the aiohttp clientsession after all requests are done.

        The session should always be closed when the program ends.
        When there's an external clientsession in use, DON'T use this method.

        This method is a coroutine.
        """
        await self.request_handler.client_session.close()
