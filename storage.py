import json
from typing import List, TypeVar, Generic, Type

T = TypeVar("T")


class StorageManager(Generic[T]):
    """
    Manages the storage of data in a JSON file.

    This class is generic and can be used to manage any type of data.
    Users must provide a data class (like Book or User) and a file path for storage.

    Attributes:
        file_path (str): The path to the JSON file used for storage.
    """

    def __init__(self, file_path: str):
        """
        Initialize the StorageManager with a path to a JSON file.

        Parameters:
            file_path (str): The path to the JSON file to be used for storage.
        """
        self.file_path = file_path

    def load_data(self, data_type: Type[T]) -> List[T]:
        """
        Load data from the JSON file and return a list of objects of the provided data type.

        If the file is not found, returns an empty list.
        If the file is not a valid JSON, raises a ValueError.

        Parameters:
            data_type (Type[T]): The class of the data to load (e.g., Book, User).

        Returns:
            List[T]: A list of objects of the provided data type, loaded from the JSON file.
        """
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                return [data_type(**item) for item in data]
        except FileNotFoundError:
            return []  # Return an empty list if the file does not exist
        except json.JSONDecodeError:
            raise ValueError("File is not a valid JSON.")

    def save_data(self, data: List[T]) -> None:
        """
        Save a list of objects to the JSON file.

        Parameters:
            data (List[T]): The list of objects to be saved.
        """
        with open(self.file_path, "w") as file:
            json.dump([item.__dict__ for item in data], file, indent=4)
