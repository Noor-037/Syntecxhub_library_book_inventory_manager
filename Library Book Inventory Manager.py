import json
import os
from turtle import title

class Book:
    def __init__(self, title, author, quantity, issued=0):
        self.title = title
        self.author = author
        self.quantity = quantity
        self.issued = issued

    def to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'quantity': self.quantity,
            'issued': self.issued
        }
    @staticmethod
    def from_dict(data):
        return Book(
            title=data['title'],
            author=data['author'],
            quantity=data['quantity'],
            issued=data['issued']
        )

class Library:
    def __init__(self, inventory_file='library_inventory.json'):
        self.inventory_file = inventory_file
        self.books = {}

    def load_data(self):
        if os.path.exists(self.inventory_file):
            with open(self.inventory_file, 'r') as f:
                data = json.load(f)
                for book_data in data:
                    book = Book.from_dict(book_data)
                    self.books[book.title.lower()] = book
                
    def save_data(self):
        with open(self.inventory_file, 'w') as f:
            data = [book.to_dict() for book in self.books.values()]
            json.dump(data, f, indent=4)

    def add_book(self, title, author, quantity):
        title_lower = title.lower()
        if title_lower in self.books:
            self.books[title_lower].quantity += quantity
            print("Updated quantity of existing book.")
        else:
            book = Book(title, author, quantity)
            self.books[title_lower] = book
            print("Book added to inventory.")

        self.save_data()
    
    def search_title(self, title):
        title=input("Enter the title of the book to search: ")
        title_lower = title.lower()
        if title_lower in self.books:
            book = self.books[title_lower]
            print("\n Book Found:")
            print(f"Title: {book.title}, Author: {book.author}, Quantity: {book.quantity}, Issued: {book.issued}")
        else:
            print("Book not found in inventory.")

    def search_author(self, author):
        author = input("Enter the author of the book to search: ").lower()
        found = False
        for book in self.books.values():
            if book.author.lower() == author:
                print(f"Title: {book.title}, Author: {book.author}, Quantity: {book.quantity}, Issued: {book.issued}")
                found = True
        if not found:
            print("No books found by this author.")
            
    def issued_book(self):
        title=input("Enter the title of the book to issue: ")
        title_lower = title.lower()
        if title_lower in self.books:
            book = self.books[title_lower]
            if book.quantity > 0:
                book.quantity -= 1
                book.issued += 1
                print(f"Book '{book.title}' issued successfully.")
            else:
                print("No copies available for issuing.")
            self.save_data()
        else:
            print("Book not found in inventory.")

    def return_book(self):
        title = input("Enter the title of the book to return: ")
        title_lower = title.lower()
        if title_lower in self.books:
            book = self.books[title_lower]
            book.quantity += 1
            if book.issued > 0:
                book.issued -= 1
            print(f"Book '{book.title}' returned successfully.")
            self.save_data()
        else:
            print("Book not found in inventory.")

    def report(self):
        total_books = sum(book.quantity + book.issued for book in self.books.values())
        total_issued = sum(book.issued for book in self.books.values())

        print("\n -------Library Report-------")
        print("Total Titles:",len(self.books))
        print("Total Books in Inventory:", total_books)
        print("Total Books Issued:", total_issued)
        print("-----------------------------")

    @staticmethod
    def main():
        library = Library()
        library.load_data()

        while True:
            print("\n ===== Library Book Inventory Manager =====")
            print("1. Add Book")
            print("2. Search Book by Title")
            print("3. Search Book by Author")
            print("4. Issue Book")
            print("5. Return Book")
            print("6. Report")
            print("7. Exit")

            choice = input("Enter your choice (1-7): ")

            if choice == '1':
                title = input("Enter the title of the book: ")
                author = input("Enter the author of the book: ")
                quantity = int(input("Enter the quantity of the book: "))
                library.add_book(title,author,quantity)

            elif choice == '2':
                library.search_title(title)

            elif choice == '3':
                library.search_author(author)

            elif choice == '4':
                library.issued_book()

            elif choice == '5':
                library.return_book()

            elif choice == '6':
                library.report()
            
            elif choice == '7':
                print("Thank you for using the Library Book Inventory Manager.")
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    Library.main()