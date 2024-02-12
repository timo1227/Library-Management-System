from typing import Callable
from book import BookManager
from user import UserManager
from check import CheckoutManager


class LibrarySystemUI:
    """
    User Interface class for the Library Management System.
    Handles all interactions with the user and manages the display of information.

    """

    def __init__(self) -> None:
        """Initialize the Library System UI with a BookManager instance."""
        self.book_manager = BookManager()
        self.user_manager = UserManager()
        self.checkout_manager = CheckoutManager("checkouts.json", self.book_manager)

    def add_book_ui(self) -> Callable[[], Callable]:
        """Add a new book to the library. Prompt for title, author, and ISBN."""
        title = input("Enter title: ").strip()
        if not title:
            print("Title cannot be empty.")
            return self.book_menu

        author = input("Enter author: ").strip()
        if not author:
            print("Author cannot be empty.")
            return self.book_menu

        isbn = input("Enter ISBN: ").strip()
        if not isbn or not isbn.isdigit():
            print("Invalid ISBN. ISBN should be numeric.")
            return self.book_menu

        if self.book_manager.add_book(title, author, isbn):
            print("Book added successfully.")
        else:
            print("Failed to add book. ISBN already exists.")

        return self.book_menu

    def delete_book_ui(self) -> Callable[[], Callable]:
        """Delete a book from the library by ISBN."""
        isbn = input("Enter the ISBN of the book to delete: ").strip()
        if not isbn:
            print("ISBN cannot be empty.")
            return self.book_menu

        try:
            if self.book_manager.delete_book(isbn):
                print("Book deleted successfully.")
            else:
                print("Book not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        return self.book_menu

    def update_book_ui(self) -> Callable[[], Callable]:
        """Update the details of an existing book by ISBN."""
        isbn = input("Enter the ISBN of the book to update: ").strip()

        if not isbn or not isbn.isdigit():
            print("Invalid ISBN. ISBN should be numeric.")
            return self.book_menu

        new_title = input("Enter the new title (press enter to skip): ").strip()
        new_author = input("Enter the new author (press enter to skip): ").strip()
        new_isbn = input("Enter the new ISBN (press enter to skip): ").strip()

        if new_isbn and not new_isbn.isdigit():
            print("Invalid ISBN. ISBN should be numeric.")
            return self.book_menu

        if self.book_manager.update_book(isbn, new_title, new_author, new_isbn):
            print("Book updated successfully.")
        else:
            print("Book not found or update failed due to duplicate ISBN.")

        return self.book_menu

    def display_books(self) -> Callable[[], Callable]:
        """Display all the books currently in the library."""
        books = self.book_manager.all_books
        if books:
            print("\nBooks:")
            for book in books:
                print(book)
        else:
            print("\nNo books in the library.")

        return self.book_menu

    def find_book_ui(self) -> Callable[[], Callable]:
        """Find and display books based on a search term."""
        search_term = input(
            "Enter a search term to find books (title, author, or ISBN): "
        ).strip()

        if not search_term:
            print("Search term cannot be empty.")
            return self.book_menu

        found_books = self.book_manager.find_book(search_term)
        if found_books:
            print("\nFound Books:")
            for book in found_books:
                print(book)
        else:
            print("No books found matching the search term.")

        return self.book_menu

    def book_menu(self) -> Callable[[], None]:
        """Display the book management submenu."""
        menu_options = {
            "1": self.add_book_ui,
            "2": self.delete_book_ui,
            "3": self.update_book_ui,
            "4": self.display_books,
            "5": self.find_book_ui,
            "6": self.main_menu,
            "7": self.exit_program,
        }

        menu_text = """
        Book Management
        1. Add Book
        2. Delete Book
        3. Update Book
        4. List Books
        5. Find Book
        6. Back to Main Menu
        7. Exit
        """
        print(menu_text)
        choice = input("Enter choice: ")

        return menu_options.get(choice, self.invalid_choice)

    def add_user_ui(self) -> Callable[[], Callable]:
        """Add a new user to the system. Prompt for name and user ID."""
        name = input("Enter user name: ").strip()

        if not name:
            print("Name cannot be empty.")
            return self.user_menu

        user_id = input("Enter user ID: ").strip()

        if not user_id:
            print("User ID cannot be empty.")
            return self.user_menu

        if self.user_manager.add_user(name, user_id):
            print("User added successfully.")
        else:
            print("Failed to add user. User ID already exists.")

        return self.user_menu

    def delete_user_ui(self) -> Callable[[], Callable]:
        """Delete a user from the system by user ID."""
        user_id = input("Enter the user ID of the user to delete: ").strip()
        try:
            if self.user_manager.delete_user(user_id):
                print("User deleted successfully.")
            else:
                print("User not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        return self.user_menu

    def update_user_ui(self) -> Callable[[], Callable]:
        """Update the details of an existing user by user ID."""
        user_id = input("Enter the user ID of the user to update: ").strip()
        new_name = input("Enter the new name (press enter to skip): ").strip()
        new_user_id = input("Enter the new user ID (press enter to skip): ").strip()

        if not new_user_id and not new_name and not user_id:
            print("No changes provided.")
            return self.user_menu

        if self.user_manager.update_user(user_id, new_name, new_user_id):
            print("User updated successfully.")
        else:
            print("User not found or update failed due to duplicate user ID.")

        return self.user_menu

    def display_users(self) -> Callable[[], Callable]:
        """Display all the users currently in the system."""
        users = self.user_manager.all_users
        if users:
            print("\nUsers:")
            for user in users:
                print(user)
        else:
            print("\nNo users in the system.")

        return self.user_menu

    def find_user_ui(self) -> Callable[[], Callable]:
        """Find and display users based on a search term."""
        search_term = input(
            "Enter a search term to find users (name or user ID): "
        ).strip()
        found_users = self.user_manager.find_user(search_term)
        if found_users:
            print("\nFound Users:")
            for user in found_users:
                print(user)
        else:
            print("No users found matching the search term.")

        return self.user_menu

    def user_menu(self) -> Callable[[], None]:
        """Display the user management submenu."""
        menu_options = {
            "1": self.add_user_ui,
            "2": self.delete_user_ui,
            "3": self.update_user_ui,
            "4": self.display_users,
            "5": self.find_user_ui,
            "6": self.main_menu,
            "7": self.exit_program,
        }

        menu_text = """
        User Management
        1. Add User
        2. Delete User
        3. Update User
        4. List Users
        5. Find User
        6. Back to Main Menu
        7. Exit
        """
        print(menu_text)
        choice = input("Enter choice: ")

        return menu_options.get(choice, self.invalid_choice)

    def checkout_book_ui(self) -> Callable[[], Callable]:
        """Handle the checkout of a book."""
        user_id = input("Enter user ID: ")
        isbn = input("Enter ISBN of the book to checkout: ")

        if self.checkout_manager.checkout_book(user_id, isbn):
            print("Book checked out successfully.")
        else:
            print(
                "Failed to checkout book. It might be unavailable or user limit reached."
            )

        return self.checkout_menu

    def checkin_book_ui(self) -> Callable[[], Callable]:
        """Handle the checkin of a book."""
        isbn = input("Enter ISBN of the book to checkin: ")

        if self.checkout_manager.checkin_book(isbn):
            print("Book checked in successfully.")
        else:
            print("Failed to checkin book. It might not be checked out.")

        return self.checkout_menu

    def list_user_checkouts_ui(self) -> Callable[[], Callable]:
        """Display all books checked out by a specific user."""
        user_id = input("Enter user ID to list checkouts: ")
        checkouts = self.checkout_manager.list_user_checkouts(user_id)

        if checkouts:
            print("\nUser Checkouts:")
            for record in checkouts:
                print(f"ISBN: {record.isbn}")
        else:
            print("No books currently checked out by this user.")

        return self.checkout_menu

    def checkout_menu(self) -> Callable[[], None]:
        """Display the checkout management submenu."""
        menu_options = {
            "1": self.checkout_book_ui,
            "2": self.checkin_book_ui,
            "3": self.list_user_checkouts_ui,
            "4": self.main_menu,
            "5": self.exit_program,
        }

        menu_text = """
        Checkout Management
        1. Checkout Book
        2. Checkin Book
        3. List User Checkouts
        4. Back to Main Menu
        5. Exit
        """
        print(menu_text)
        choice = input("Enter choice: ")

        return menu_options.get(choice, self.invalid_choice)

    def main_menu(self) -> Callable[[], None]:
        """Display the main menu and return the function associated with the user's choice."""
        menu_options = {
            "1": self.book_menu,
            "2": self.user_menu,
            "3": self.checkout_menu,
            "4": self.exit_program,
        }

        menu_text = """
        Library Management System
        1. Book Management
        2. User Management
        3. Checkout Management
        4. Exit
        """
        print(menu_text)
        choice = input("Enter choice: ")

        return menu_options.get(choice, self.invalid_choice)

    def exit_program(self) -> None:
        """Exit the program."""
        print("Exiting.")
        exit()

    def invalid_choice(self) -> Callable[[], Callable]:
        print("Invalid choice, please try again.")
        return self.main_menu  # Go back to the main menu

    def run(self) -> None:
        """Run the main loop of the program, allowing user interaction until exit."""
        next_action = self.main_menu
        while True:
            next_action = next_action()


def main():
    library_system = LibrarySystemUI()
    library_system.run()


if __name__ == "__main__":
    main()
