"""
This module provides a simple login system called the Music Library Management System.
It allows users to authenticate with their username and password, granting access to the platform based on their role.
The 'user' role can view the library, while the 'admin' role can perform CRUD operations on the library.
The module connects to an SQLite database to store user accounts and library data, which is encrypted for security.
"""

import sqlite3       # Import the SQLite3 module to connect to the SQLite database
import hashlib       # Import the hashlib module to hash the password for security purposes

# Below will connect to the SQLite database and create a cursor object to execute SQL queries
conn = sqlite3.connect('music_library.db')
cursor = conn.cursor()

# For the purpose of executing this login.py script, output will prompt the user to enter username and password
# These accounts and their credentials were registered in the main.py script after running the script
# When the user enters the correct username and password, the user will be authenticated and granted access to the library
# The account details are stored in the users table in the database

# Below will get the user credentials from the database
def get_user_credentials(username):
    cursor.execute('SELECT password_hash, salt, role FROM users WHERE username = ?', (username,))
    return cursor.fetchone()

# Below will hash the password for security purposes
def hash_password(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

# Below will authenticate the user based on the username and password entered
def authenticate_user(username, password):
    user = get_user_credentials(username)

# If the user is in the database, the password will be hashed  
# The hashed password will be compared with the stored hash in the database
    if user:
        stored_hash, salt, role = user
        test_hash = hash_password(password, salt) 

# If the hashed password matches the stored hash, the user will be authenticated and granted access to the library                                                     
        if test_hash == stored_hash:
            return role                           
    
    return None

# Below will view the data based on the user's role 
# Based on the role, the data will be pulled from the lyrics, music_scores, musical_recordings, and modification_history tables
# The cursor will execute the SQL query to select all the data from the tables
def view_data(role):
    if role:
        tables = ['lyrics', 'music_scores', 'musical_recordings', 'modification_history']
        for table in tables:
            cursor.execute(f'SELECT * FROM {table}')
            print(f"{table.replace('_', ' ').title()}:")
            for row in cursor.fetchall():
                print(row)
    else:
        print("Permission denied: Invalid username or password.")

# Below will perform the main function of the login system
# The user will be prompted to enter their username and password which was created in the main.py script
# The user will be authenticated based on the entered credentials
# If the user is authenticated, the user will be granted access to the library based on their role
def main():
    
    print("Welcome to the Music Library Management System")
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = authenticate_user(username, password)
    
    if role is None:
        print("Login Failed: Invalid username or password.")
        return

# If the role is 'user', the user will be granted access to view the library
# The user will be prompted to view the library by entering 'yes' or 'no'
    if role == 'user':
        print("Welcome, user! You can view the Music Library Management System library.")
        choice = input("Would you like to view the Music Library Management System library? (yes/no): ").strip().lower()
        if choice == 'yes':
            view_data(role)
        else:
            print("Thank you for visiting the Music Library Management System. You can browse the library for more options.")

# If the role is 'admin', the administrator will be granted access to view the library
# The administrator will be prompted to view the library by entering 'yes' or 'no'
# The administrator will also be prompted to create, modify, or delete items by entering 'yes' or 'no' 
# If the administrator chooses to modify items, the administrator will be directed to the records section to perform CRUD operations
# This script is a simple login system by yes or no prompts        
    elif role == 'admin':
        print("Welcome, administrator! You can create, read, update, or delete the Music Library Management System library.")
        choice = input("Would you like to view the Music Library Management System library? (yes/no): ").strip().lower()
        if choice == 'yes':
            view_data(role)
            choice_modify = input("Would you like to create, modify, or delete items? (yes/no): ").strip().lower()
            if choice_modify == 'yes':
                print("Please navigate to the records section to perform CRUD operations.")
            else:
                print("Thank you for visiting the Music Library Management System. You can browse the library for more options.")
        else:
            print("Thank you for visiting the Music Library Management System. You can browse the library for more options.")
    else:
        print("Please register an account.")

if __name__ == "__main__":
    main()

# This will commit any changes to the database
conn.commit()
