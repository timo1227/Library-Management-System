from typing import List, Optional
from storage import StorageManager


class Book:
    """
    Represents a book with a title, author, and ISBN.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        isbn (str): The ISBN of the book.
        available (bool): Whether the book is available for checkout.
    """

    def __init__(
        self, title: str, author: str, isbn: str, available: bool = True
    ) -> None:
        """
        Constructs all the necessary attributes for the Book object.

        Parameters:
            title (str): Title of the book.
            author (str): Author of the book.
            isbn (str): ISBN of the book.
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available

    def __str__(self) -> str:
        """
        String representation of the Book object.

        Returns:
            str: String describing the book.
        """
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Status: {'Available' if self.available else 'Checked Out'}"


class BookManager:
    """
    Manages a collection of books.

    Attributes:
        storage_manager (StorageManager): Instance of StorageManager to handle book data storage.
        books (List[Book]): List of books managed by the BookManager.
    """

    def __init__(self, file_path: str = "books.json") -> None:
        """
        Initializes the BookManager with a StorageManager instance and loads existing books.

        Parameters:
            file_path (str): The path to the JSON file containing book data.
                             Defaults to 'books.json'.
        """
        self.storage_manager = StorageManager[Book](file_path)
        self.books = self.storage_manager.load_data(Book)

    @property
    def all_books(self) -> List[Book]:
        """
        Retrieves the list of all books.

        Returns:
            List[Book]: List of all books in the manager.
        """
        return self.books

    def add_book(self, title: str, author: str, isbn: str) -> bool:
        """
        Adds a new book to the collection. Ensures that the ISBN is unique.

        Parameters:
            title (str): Title of the new book.
            author (str): Author of the new book.
            isbn (str): ISBN of the new book.

        Returns:
            bool: True if book was successfully added, False if ISBN already exists.
        """
        if any(book.isbn == isbn for book in self.books):
            return False  # ISBN already exists

        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        self.storage_manager.save_data(self.books)
        return True

    def delete_book(self, isbn: str) -> bool:
        """
        Deletes a book identified by its ISBN.

        Parameters:
            isbn (str): ISBN of the book to delete.

        Returns:
            bool: True if book was successfully deleted, False otherwise.
        """
        book_to_delete = next((book for book in self.books if book.isbn == isbn), None)
        if book_to_delete:
            self.books.remove(book_to_delete)
            self.storage_manager.save_data(self.books)
            return True
        return False

    def update_book(
        self,
        isbn: str,
        new_title: Optional[str] = None,
        new_author: Optional[str] = None,
        new_isbn: Optional[str] = None,
    ) -> bool:
        """
        Updates the attributes of a book identified by its ISBN. Ensures that the new ISBN is unique.

        Parameters:
            isbn (str): ISBN of the book to update.
            new_title (Optional[str]): New title for the book.
            new_author (Optional[str]): New author for the book.
            new_isbn (Optional[str]): New ISBN for the book.

        Returns:
            bool: True if the book was successfully updated, False otherwise.
        """
        book_to_update = next((book for book in self.books if book.isbn == isbn), None)
        if book_to_update:
            # Check if new ISBN already exists in other books
            if new_isbn and any(
                book.isbn == new_isbn for book in self.books if book != book_to_update
            ):
                return False  # New ISBN already exists

            if new_title:
                book_to_update.title = new_title
            if new_author:
                book_to_update.author = new_author
            if new_isbn:
                book_to_update.isbn = new_isbn

            self.storage_manager.save_data(self.books)
            return True
        return False

    def save_books(self) -> None:
        """
        Saves the current list of books to the storage file.
        """
        self.storage_manager.save_data(self.books)

    def find_book_by_isbn(self, isbn: str):
        """
        Finds a book by its ISBN.

        Parameters:
            isbn (str): The ISBN of the book to find.

        Returns:
            Book: The book with the given ISBN, or None if not found.
        """
        return next((book for book in self.books if book.isbn == isbn), None)

    def find_book(
        self,
        search_term: str,
    ) -> List[Book]:
        """
        Finds books that match the search term in title, author, or ISBN.

        Parameters:
            search_term (str): The term to search for in the book's title, author, or ISBN.

        Returns:
            List[Book]: List of books that match the search term.
        """
        found_books = []
        search_term_lower = search_term.lower()
        for book in self.books:
            if (
                search_term_lower in book.title.lower()
                or search_term_lower in book.author.lower()
                or search_term in book.isbn
            ):
                found_books.append(book)
        return found_books
