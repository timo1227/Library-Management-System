from typing import List, Optional
from storage import StorageManager


class User:
    """
    Represents a library user with a name and user ID.

    Attributes:
        name (str): The name of the user.
        user_id (str): The unique identifier for the user.
    """

    def __init__(self, name: str, user_id: str) -> None:
        """
        Initializes a User with a name and user ID.
        """
        self.name = name
        self.user_id = user_id

    def __str__(self) -> str:
        """
        String representation of the User.
        """
        return f"User: {self.name}, ID: {self.user_id}"


class UserManager:
    """
    Manages a collection of users.

    Attributes:
        users (List[User]): List of users managed by the UserManager.
    """

    def __init__(self, file_path: str = "users.json") -> None:
        """
        Initializes the UserManager with an empty list of users.
        """
        self.storage_manager = StorageManager[User](file_path)
        self.users = self.storage_manager.load_data(User)

    @property
    def all_users(self) -> List[User]:
        """
        Returns a list of all users.
        """
        return self.users

    def add_user(self, name: str, user_id: str) -> bool:
        """
        Adds a new user to the collection.

        Ensures that the user ID is unique.
        """
        if any(user.user_id == user_id for user in self.users):
            return False  # User ID already exists

        self.users.append(User(name, user_id))
        self.storage_manager.save_data(self.users)  # Save after adding
        return True

    def delete_user(self, user_id: str) -> bool:
        """
        Deletes a user identified by user ID.
        """
        user_to_delete = next(
            (user for user in self.users if user.user_id == user_id), None
        )
        if user_to_delete:
            self.users.remove(user_to_delete)
            self.storage_manager.save_data(self.users)  # Save after deleting
            return True
        return False

    def update_user(
        self,
        user_id: str,
        new_name: Optional[str] = None,
        new_user_id: Optional[str] = None,
    ) -> bool:
        """
        Updates the attributes of a user identified by user ID.
        """
        user_to_update = next(
            (user for user in self.users if user.user_id == user_id), None
        )
        if user_to_update:
            if new_name:
                user_to_update.name = new_name
            if new_user_id:
                if any(
                    user.user_id == new_user_id
                    for user in self.users
                    if user != user_to_update
                ):
                    return False
                user_to_update.user_id = new_user_id

            self.storage_manager.save_data(self.users)  # Save after updating
            return True
        return False

    def list_users(self) -> List[User]:
        """
        Returns a list of all users.
        """
        return self.users

    def find_user(self, search_term: str) -> List[User]:
        """
        Finds users that match the search term in name or user ID.
        """
        found_users = []
        search_term_lower = search_term.lower()
        for user in self.users:
            if search_term_lower in user.name.lower() or search_term in user.user_id:
                found_users.append(user)
        return found_users
