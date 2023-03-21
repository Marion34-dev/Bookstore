# Define colour codes
PINK = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[0m'
GREEN = '\033[92m'
BOLD = '\033[1m'

# Import SQLite
import sqlite3
from sqlite3 import OperationalError, IntegrityError

# Creating database called 'ebookstore' and cursor
db = sqlite3.connect('ebookstore')
cursor = db.cursor()

# Creating table called 'books'
cursor.execute('''CREATE TABLE if not exists books(
ID int PRIMARY KEY not null,
Title varchar not null,
Author varchar not null,
Qty int)
;''')
db.commit()

# Inserting books in the ebookstore
book1 = (3001, "A tale of Two Cities", "Charles Dickens", 30)
book2 = (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40)
book3 = (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25)
book4 = (3004, "The Lord of the Rings", "J.R.R. Tolkien", 37)
book5 = (3005, "Alice in Wonderland", "Lewis Carroll", 12)
books = [book1, book2, book3, book4, book5]
cursor.executemany("INSERT INTO books (ID, Title, Author, Qty) "
                   "VALUES(?,?,?,?)", books)

# ========== Menu =============
while True:
    menu = f"\n{CYAN}{BOLD}<========== Main Menu =============>\n"
    menu += f"{GREEN}1 - {PINK}To enter a book\n"
    menu += f"{GREEN}2 - {PINK}To update a book\n"
    menu += f"{GREEN}3 - {PINK}To delete a book\n"
    menu += f"{GREEN}4 - {PINK}To search for books\n"
    menu += f"{GREEN}0 - {PINK}Exit the menu\n"
    print(menu)

    try:
        user = int(input(f"{WHITE}Welcome! What would you like to do? "))

        # If user selects option 1, add a book to the database
        if user == 1:
            while True:
                try:
                    ID, title, author, qty = int(input("Insert book ID: ")), input("Insert book title: "), \
                        input("Insert the name of the author: "), \
                        int(input("Insert the number of copies in stock: "))
                    new_book = (ID, title, author, qty)
                    cursor.execute("INSERT INTO books (ID, Title, Author, Qty)"
                                   "VALUES(?,?,?,?)", new_book)
                    print("The book has been successfully added!")
                    break
                except ValueError:
                    print("Invalid input, please try again.")
                except IntegrityError:
                    print("Please use a different ID number, this one already exists!")
                continue
            continue

        # If user selects option 2, ask user what they want to update
        elif user == 2:
            while True:
                choice = "\n===== Options =====\n"
                choice += "1 - To update the Title\n"
                choice += "2 - To update the Author\n"
                choice += "3 - To update the Quantity in Stock\n"
                print(choice)
                user_input = int(input("What would you like to do? "))

                # If user wants to update the title
                if user_input == 1:
                    try:
                        book = input("Please insert the ID of the book you would like to update: ")
                        new_title = input("Insert the new title: ")
                        cursor.execute(f"UPDATE books SET Title = '{new_title}' WHERE ID = {book}")
                        print("Thank you, the title has been successfully modified!")
                        break
                    except OperationalError:
                        print("Input not valid, please try again")
                        continue

                # If user wants to update the author
                if user_input == 2:
                    try:
                        book = input("Please insert the ID of the book you would like to update: ")
                        new_author = input("Insert the name of the new author: ")
                        cursor.execute(f'''UPDATE books SET Author = '{new_author}' WHERE ID = {book}''')
                        print("Thank you, the author has been successfully modified!")
                        break
                    except OperationalError:
                        print("Input not valid, please try again")
                        continue
                # If user wants to update the quantity
                if user_input == 3:
                    try:
                        book = input("Please insert the ID of the book you would like to update: ")
                        new_qty = input("Insert the new quantity: ")
                        cursor.execute(f'''UPDATE books SET Qty = {new_qty} WHERE ID = {book}''')
                        print("Thank you, the quantity has been successfully updated!")
                        break
                    except OperationalError:
                        print("Input not valid, please try again")
                        continue

                else:
                    print("Invalid input, please try again")

        # If user selects option 3, delete the row of the book chosen by the user
        elif user == 3:
            try:
                choice = input("Please insert the ID of the book you would like to remove from the ebookstore: ")
                cursor.execute(f'''DELETE FROM books WHERE ID = {choice}''')
                print("The book has been successfully deleted!")
                continue
            except OperationalError:
                print("Invalid input, please try again")

        # If user selects option 4, print out the book the user has selected
        elif user == 4:
            while True:
                choice = "\n===== Options =====\n"
                choice += "1 - To look it up by the book ID\n"
                choice += "2 - To look it up by Author\n"
                choice += "3 - To look it up by the Title\n"
                print(choice)
                user_input = int(input("What would you like to do? "))

                if user_input == 1:
                    try:
                        choice = input("Please insert the ID of the book you would like to view: ")
                        book = cursor.execute(f'''SELECT * FROM books WHERE ID = {choice}''')
                        print(book.fetchone())
                        break

                    except OperationalError:
                        print("Invalid input, please try again")

                elif user_input == 2:
                    choice = input("Please insert the Author of the book you would like to view: ")
                    book = cursor.execute(f'''SELECT * FROM books WHERE Author = '{choice}' ''')
                    print("Below, you can view all the books we have from this author:")
                    for item in book.fetchall():
                        print(item)
                    break

                elif user_input == 3:
                    choice = input("Please insert the Title of the book you would like to view: ")
                    book = cursor.execute(f'''SELECT * FROM books WHERE Title = '{choice}' ''')
                    print("Below, you can view all the books we have with this title:")
                    for item in book.fetchall():
                        print(item)
                    break

                else:
                    print("Incorrect input, please try again")

        # If user selects the exit option
        elif user == 0:
            print("Bye!")
            break

        else:
            print("Invalid input, please try again")

    except ValueError:
        print("Invalid entry, please try again")

# db.commit()
db.close()
