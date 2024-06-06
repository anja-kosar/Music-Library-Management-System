"""
This module provides a simple login system for a Music Library Management System.
It allows users to authenticate with their username and password, and grants access based on their role.
Users with the 'user' role can view the library, while users with the 'admin' role can also create, modify, or delete items.
The module connects to an SQLite database to store user accounts and library data.
"""

import sqlite3       # Import the SQLite3 module to connect to the SQLite database
import hashlib       # Import the hashlib module to hash the password for security purposes

# Below will connect to the SQLite database and create a cursor object to execute SQL queries
conn = sqlite3.connect('music_library.db')
cursor = conn.cursor()

# Below will connect to the SQLite database and create a cursor object to execute SQL queries
conn = sqlite3.connect('music_library.db')
cursor = conn.cursor()

# For the purpose of executing this login.py script, output will prompt the user to enter username and password
# These accounts and their credentials were registered in the main.py script after running the script
# When the user enters the correct username and password, the user will be authenticated and granted access to the library
# The account details are stored in the users table in the database

# Below is a function to authenticate user based on the provided username and password
def authenticate_user(username, password):
    cursor.execute('SELECT password_hash, salt, role FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    if user:
        stored_hash, salt, role = user
        # Compare the stored hash with the hash of the provided password
        test_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        if test_hash == stored_hash:
            return role  # Return the role of the user if authentication succeeds
    return None


# Below is a view data function that will display the data in the library based on the user's role
# The cursor will execute SQL queries to select all data from the lyrics, music_scores, musical_recordings, and modification_history tables
# The select queries will fetch all the rows from the tables and display the data in the console
def view_data(role):
    if role:
        cursor.execute('SELECT * FROM lyrics')
        print("Lyrics:")
        for row in cursor.fetchall():
            print(row)

        cursor.execute('SELECT * FROM music_scores')
        print("Music Scores:")
        for row in cursor.fetchall():
            print(row)

        cursor.execute('SELECT * FROM musical_recordings')
        print("Musical Recordings:")
        for row in cursor.fetchall():
            print(row)

        cursor.execute('SELECT * FROM modification_history')
        print("Modification History:")
        for row in cursor.fetchall():
            print(row)
    else:
        print("Permission denied: Invalid username or password.")

# Below is the main function to execute the login process.
# The user will be prompted to enter their username and password.
# The authenticate_user function will be called to verify the user's credentials.
# If the user is authenticated, the user's role will be returned.
# The user will be welcomed with a 'Welcome to the Music Library Management System' message.

def main():
    print("Welcome to the Music Library Management System")
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = authenticate_user(username, password)
    
    if role is None:
        print("Login Failed: Invalid username or password.")
        return
    
# This elif statement will execute the function based on the role of the user.
# When the user is authenticated, a message will welcome the user based on their role and privileges.
# If the user is a regular user, they can only view the data.
# If the user is an admin, a prompt will display to view the data with a yes or no option.
# If the user selects yes, they will be able to view the data and will be asked if they would like to create, modify, or delete items.
# If the user selects yes, they will be prompted to navigate to the records section to perform CRUD operations.
# If the user selects no, they will be thanked for visiting the Music Library Management System.
# This simple login cript demonstrates the basic login process and the ability to view data based on the user's role.
    if role == 'user':
        print("Welcome, user! You can view the Music Library Management System library.")
        choice = input("Would you like to view the Music Library Management System library? (yes/no): ").lower()
        if choice == 'yes':
            view_data(role)
        else:
            print("Thank you for visiting the Music Library Management System. You can browse the library for more options.")
        
    elif role == 'admin':
        print("Welcome, administrator! You can create, read, update or delete the Music Library Management System library.")
        choice = input("Would you like to view the Music Library Management System library? (yes/no): ").lower()
        if choice == 'yes':
            view_data(role)
            choice_modify = input("Would you like to create, modify, or delete items? (yes/no): ").lower()
            if choice_modify == 'yes':
                print("Please navigate to the records section to perform CRUD operations.")
            else:
                print("Thank you for visiting the Music Library Management System. You can browse the library for more options .")
        
    else:
        print("Please register an account.")

if __name__ == "__main__":
    main()

# This will commit any changes to the database
conn.commit()
