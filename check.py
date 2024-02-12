from typing import List
from book import BookManager
from storage import StorageManager


class CheckoutRecord:
    """
    Represents a record of a book being checked out by a user.

    Attributes:
        user_id (str): The ID of the user who checked out the book.
        isbn (str): The ISBN of the book that is checked out.
    """

    def __init__(self, user_id: str, isbn: str) -> None:
        self.user_id = user_id
        self.isbn = isbn


class CheckoutManager:
    """
    Manages the process of checking books in and out of the library.
    """

    def __init__(self, checkout_file: str, book_manager: BookManager) -> None:
        """
        Initializes the CheckoutManager with a file path for checkout records and a BookManager instance.
        """
        self.storage_manager = StorageManager[CheckoutRecord](checkout_file)
        self.checkouts = self.storage_manager.load_data(CheckoutRecord)
        self.book_manager = book_manager

    def checkout_book(self, user_id: str, isbn: str) -> bool:
        """
        Checks out a book using its ISBN and the user's ID.

        Parameters:
            user_id (str): The ID of the user checking out the book.
            isbn (str): The ISBN of the book to check out.

        Returns:
            bool: True if the checkout was successful, False otherwise.
        """
        # Check if book is already checked out
        if any(checkout.isbn == isbn for checkout in self.checkouts):
            return False

        # Check if user has less than 3 books checked out
        if sum(checkout.user_id == user_id for checkout in self.checkouts) >= 3:
            return False

        # Check if the book exists and is available
        book = self.book_manager.find_book_by_isbn(isbn)
        if book and book.available:
            book.available = False
            self.book_manager.save_books()
            self.checkouts.append(CheckoutRecord(user_id, isbn))
            self.storage_manager.save_data(self.checkouts)
            return True

        return False

    def checkin_book(self, isbn: str) -> bool:
        """
        Checks in a book using its ISBN. If the book is found in the checkouts, it is removed and marked as available.

        Parameters:
            isbn (str): The ISBN of the book to check in.

        Returns:
            bool: True if the check-in was successful, False otherwise.
        """
        for checkout in self.checkouts:
            if checkout.isbn == isbn:
                self.checkouts.remove(checkout)
                book = self.book_manager.find_book_by_isbn(isbn)
                if book:
                    book.available = True
                    self.book_manager.save_books()
                self.storage_manager.save_data(self.checkouts)
                return True
        return False

    def list_user_checkouts(self, user_id: str) -> List[CheckoutRecord]:
        """
        Lists all the books checked out by a specific user.

        Parameters:
            user_id (str): The ID of the user whose checkouts are to be listed.

        Returns:
            List[CheckoutRecord]: A list of CheckoutRecord for the specified user.
        """
        return [checkout for checkout in self.checkouts if checkout.user_id == user_id]
