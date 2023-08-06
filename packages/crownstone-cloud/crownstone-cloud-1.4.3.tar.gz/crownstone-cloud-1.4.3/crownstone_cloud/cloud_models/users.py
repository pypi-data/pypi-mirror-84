"""User handler for Crownstone cloud data."""
from typing import Dict, Any


class Users:
    """Handler for the users in a sphere."""

    def __init__(self, cloud, sphere_id: str) -> None:
        """Initialization."""
        self.cloud = cloud
        self.users: Dict[str, User] = {}
        self.sphere_id: str = sphere_id

    def __iter__(self):
        """Iterate over users."""
        return iter(self.users.values())

    async def async_update_user_data(self) -> None:
        """
        Get the users for the sphere from the cloud.

        This method is a coroutine.
        """
        user_data = await self.cloud.request_handler.get(
            'Spheres', 'users', model_id=self.sphere_id
        )
        # process items
        removed_items = []
        new_items = []
        for role, users in user_data.items():
            for user in users:
                user_id = user['id']
                exists = self.users.get(user_id)
                # check if the User already exists
                # it is important that we don't throw away existing objects, as they need to remain functional
                if exists:
                    # update data
                    self.users[user_id].data = user
                else:
                    # add new User + their role
                    self.users[user_id] = User(user, role)

                # generate list with new id's to check with the existing id's
                new_items.append(user_id)

        # check for removed items
        for user_id in self.users:
            if user_id not in new_items:
                removed_items.append(user_id)

        # remove items from dict
        for user_id in removed_items:
            del self.users[user_id]

    def find_by_first_name(self, first_name: str) -> list:
        """Search for a user by first name and return a list with the users found."""
        found_users = []
        for user in self.users.values():
            if first_name == user.first_name:
                found_users.append(user)

        return found_users

    def find_by_last_name(self, last_name: str) -> list:
        """Search for a user by last name and return a list with the users found."""
        found_users = []
        for user in self.users.values():
            if last_name == user.last_name:
                found_users.append(user)

        return found_users

    def find_by_id(self, user_id: str) -> object or None:
        """Search for a user by id and return crownstone object if found."""
        return self.users[user_id]


class User:
    """Represents a user in a sphere."""

    def __init__(self, data: Dict[str, Any], role: str) -> None:
        """Initialization."""
        self.data: Dict[str, Any] = data
        self.role: str = role

    @property
    def first_name(self) -> str:
        """Return the first name of this User."""
        return self.data['firstName']

    @property
    def last_name(self) -> str:
        """Return the last name of this User."""
        return self.data['lastName']

    @property
    def email(self) -> str:
        """Return the email of this User."""
        return self.data['email']

    @property
    def cloud_id(self) -> str:
        """Return the cloud id of this User."""
        return self.data['id']

    @property
    def email_verified(self) -> bool:
        """Return whether the user has verified email."""
        return self.data['emailVerified']
