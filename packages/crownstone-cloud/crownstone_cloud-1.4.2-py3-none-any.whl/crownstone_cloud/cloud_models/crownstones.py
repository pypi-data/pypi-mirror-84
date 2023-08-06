"""Crownstone handler for Crownstone cloud data"""
from crownstone_cloud.const import DIMMING_ABILITY
from crownstone_cloud.exceptions import (
    CrownstoneAbilityError,
    AbilityError
)
from typing import Dict, Any
import logging

_LOGGER = logging.Logger(__name__)


class Crownstones:
    """Handler for the crownstones of a sphere."""

    def __init__(self, cloud, sphere_id: str) -> None:
        """Initialization."""
        self.cloud = cloud
        self.crownstones: Dict[str, Crownstone] = {}
        self.sphere_id: str = sphere_id

    def __iter__(self):
        """Iterate over crownstones."""
        return iter(self.crownstones.values())

    async def async_update_crownstone_data(self) -> None:
        """Get the crownstones data from the cloud."""
        # include abilities and current switch state in the request
        data_filter = {"include": ["currentSwitchState", {"abilities": "properties"}]}
        # request data
        crownstone_data = await self.cloud.request_handler.get(
            'Spheres', 'ownedStones', filter=data_filter, model_id=self.sphere_id
        )
        # process items
        removed_items = []
        new_items = []
        for crownstone in crownstone_data:
            crownstone_id = crownstone['id']
            exists = self.crownstones.get(crownstone_id)
            # check if the crownstone already exists
            # it is important that we don't throw away existing objects, as they need to remain functional
            if exists:
                # update data and update abilities
                self.crownstones[crownstone_id].data = crownstone
            else:
                # add new Crownstone
                self.crownstones[crownstone_id] = Crownstone(self.cloud, crownstone)

            # update the abilities of the Crownstone from the data
            self.crownstones[crownstone_id].update_abilities()

            # generate list with new id's to check with the existing id's
            new_items.append(crownstone_id)

        # check for removed items
        for crownstone_id in self.crownstones:
            if crownstone_id not in new_items:
                removed_items.append(crownstone_id)

        # remove items from dict
        for crownstone_id in removed_items:
            del self.crownstones[crownstone_id]

    def find(self, crownstone_name: str) -> object or None:
        """Search for a crownstone by name and return crownstone object if found."""
        for crownstone in self.crownstones.values():
            if crownstone_name == crownstone.name:
                return crownstone

    def find_by_id(self, crownstone_id) -> object or None:
        """Search for a crownstone by id and return crownstone object if found."""
        return self.crownstones[crownstone_id]

    def find_by_uid(self, crownstone_uid) -> object or None:
        """Search for a crownstone by uid and return crownstone object if found."""
        for crownstone in self.crownstones.values():
            if crownstone_uid == crownstone.unique_id:
                return crownstone


class CrownstoneAbility:
    """Represents a Crownstone Ability"""

    def __init__(self, data: dict) -> None:
        """Initialization"""
        self.data: Dict[str, Any] = data
        self.is_enabled: bool = self.data['enabled']
        self.properties: dict = self.data['properties']

    @property
    def type(self) -> str:
        """Return the ability type."""
        return self.data['type']

    @property
    def ability_id(self) -> str:
        """Return the ability id."""
        return self.data['id']

    @property
    def crownstone_id(self) -> str:
        """Return the Crownstone id."""
        return self.data['stoneId']


class Crownstone:
    """Represents a Crownstone"""

    def __init__(self, cloud, data: Dict[str, Any]) -> None:
        """Initialization."""
        self.cloud = cloud
        self.data: Dict[str, Any] = data
        self.abilities: Dict[str, CrownstoneAbility] = {}
        # power usage (W)
        self.power_usage = None

    @property
    def name(self) -> str:
        """Return the name of this Crownstone."""
        return self.data['name']

    @property
    def unique_id(self) -> int:
        """Return the unique_id of this Crownstone."""
        return self.data['uid']

    @property
    def cloud_id(self) -> str:
        """Return the cloud id of this Crownstone."""
        return self.data['id']

    @property
    def type(self) -> str:
        """Return the Crownstone type."""
        return self.data['type']

    @property
    def sw_version(self) -> str:
        """Return the firmware version of this Crownstone."""
        return self.data['firmwareVersion']

    @property
    def icon(self) -> str:
        """Return the icon of this Crownstone."""
        return self.data['icon']

    @property
    def state(self) -> int:
        """Return the last reported switch state (0 - 100) of this Crownstone."""
        return self.data['currentSwitchState']['switchState']

    @state.setter
    def state(self, value: int) -> None:
        """
        Set a new switch state (0 - 100) of this Crownstone.

        Only updates state in cloud, does not send a switch command to the actual Crownstone.
        """
        self.data['currentSwitchState']['switchState'] = value

    def update_abilities(self) -> None:
        """Add/update the abilities for this Crownstone."""
        for ability in self.data['abilities']:
            self.abilities[ability['type']] = CrownstoneAbility(ability)

    async def async_turn_on(self) -> None:
        """
        Turn this crownstone on.

        This method is a coroutine.
        """
        # send a command to the cloud to turn the Crownstone on.
        await self.cloud.request_handler.post(
            'Stones', 'switch', model_id=self.cloud_id, json={"type": "TURN_ON"}
        )

    async def async_turn_off(self) -> None:
        """
        Turn this crownstone off.

        This method is a coroutine.
        """
        # send a command to the cloud to turn the Crownstone off.
        await self.cloud.request_handler.post(
            'Stones', 'switch', model_id=self.cloud_id, json={"type": "TURN_OFF"}
        )

    async def async_set_brightness(self, brightness: int) -> None:
        """
        Set the brightness of this crownstone, if dimming enabled.

        :param brightness: brightness value between (0 - 100)

        This method is a coroutine.
        """
        # check dimming availability & value, and send a command to the cloud to dim the Crownstone.
        if self.abilities[DIMMING_ABILITY].is_enabled:
            if brightness < 0 or brightness > 100:
                raise ValueError("Enter a value between 0 and 100")
            else:
                await self.cloud.request_handler.post(
                    'Stones', 'switch', model_id=self.cloud_id, json={"type": "PERCENTAGE", "percentage": brightness}
                )
        else:
            raise CrownstoneAbilityError(AbilityError["NOT_ENABLED"])
