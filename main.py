"""
This module contains code for creating and managing a music library database.
The module includes functions and classes for creating tables, inserting records, and performing authentication and authorization.
"""

import sqlite3                 # SQLite library for database operations
import hashlib                 # Hashlib library for hashing functions
import os                      # Os library for operating system functions such as random number generation (salt)
from datetime import datetime  # Datetime library for timestamping records

# Below connects to the SQLite database and creates a cursor object to execute SQL queries
conn = sqlite3.connect('music_library.db')
cursor = conn.cursor()

# The beginning of this script is the creation of the database and tables for storing data
# They will each be created with a primary key, and the timestamp will be automatically generated when a record is inserted
# Primay keys are unique identifiers for each record in the table and are used to uniquely identify each record in the table
# This is easier to manage and query the data in the database
# They will be explained in detail below

# Below creates a table for storing musical recordings of songs in the database
# The table will store the song title, recording (BLOB), checksum, and timestamp of the record
# Blob is a binary large object that can store large data such as images, audio, and video files
# The checksum is a hash value generated from the recording data to ensure data integrity
# This will be applied to all tables in the database to ensure data integrity
cursor.execute('''
CREATE TABLE IF NOT EXISTS musical_recordings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_title TEXT NOT NULL,
    recording BLOB NOT NULL,
    checksum TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Below creates a table for storing lyrics of songs in the database
# The table will store the song title, lyrics, and timestamp of the record
# The lyrics will be stored as text in the database
# The timestamp will be automatically generated when a record is inserted into the table
# The timestamp will be used to track the modification history of records in the database
cursor.execute('''
CREATE TABLE IF NOT EXISTS lyrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_title TEXT NOT NULL,
    lyrics TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Below creates a table for storing music scores of songs in the database
# The table will store the song title, score (BLOB), and timestamp of the record
# The score will be stored as a binary large object in the database
# Binary large object is a data type that can store large binary data such as images, audio, and video files
# The timestamp will be automatically generated when a record is inserted into the table
cursor.execute('''
CREATE TABLE IF NOT EXISTS music_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_title TEXT NOT NULL,
    score BLOB NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Below creates a table for storing modification history of records in the database
# The table will store modification history of records in the database including the table name, action, record ID, and timestamp
# The table name will store the name of the table where the record is modified
# The action will store the type of action performed on the record (INSERT, DELETE, UPDATE)
# This will be used by the admin user to track the modification history of records in the database
cursor.execute('''
CREATE TABLE IF NOT EXISTS modification_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    action TEXT NOT NULL,
    record_id INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Below creates a table for storing user accounts for authentication and authorization purposes in the database
# The table will store the account ID, first name, last name, date of birth, email, and timestamp of the record
# The account ID will be used as a foreign key in the users table to link the user account with the user details
# The email will be used as a unique identifier for the user account
# The timestamp will be automatically generated when a record is inserted into the table
# This will be used to store user details for authentication and authorization purposes in the database
cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    email TEXT NOT NULL UNIQUE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Below creates a table for storing user details and their roles in the database 
# The table will store the account ID, username, password hash, salt, role, and timestamp of the record
# The account ID will be used as a foreign key in the users table to link the user account with the user details
# The username will be used as a unique identifier for the user account
# The role will be used to determine the role of the user (user or admin)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user', 'admin')),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts (id)
)
''')

# Below commits the changes to the database
# The commit method is used to save the changes to the database 
conn.commit()

# Below is the class for creating an account in the database 
# The account class will store the user's first name, last name, date of birth, and email
# The save method will insert the account details into the accounts tables created above, and add the user to the database
# The save method will return the last row ID of the inserted record
class Account:
    def __init__(self, first_name, last_name, date_of_birth, email):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email = email

    def save(self):
        cursor.execute('INSERT INTO accounts (first_name, last_name, date_of_birth, email) VALUES (?, ?, ?, ?)',
                       (self.first_name, self.last_name, self.date_of_birth, self.email))
        conn.commit()
        return cursor.lastrowid

# Below is a login class for hashing the user's password and adding the user to the users table in the database
# Static method is applied to the class login to show the use of static methods in Python 
# Static method is a method that is bound to the class rather than the object of the class
# Static method is convenient because it doesnt require the creation of an instance of the class as its bound to the Login class itself
class Login:
    @staticmethod
    def hash_password(password, salt=None, iterations=100000):        # The hash_password method will hash the user's password
        if salt is None:                                              # The method will take the password and salt as input
            salt = os.urandom(16)                                     # The method will generate a random salt if no salt is provided
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)  
        return password_hash, salt                                    # The method will return the password hash and salt

    @staticmethod
    def add_user(account_id, username, password, role):
        password_hash, salt = Login.hash_password(password)
        cursor.execute('INSERT INTO users (account_id, username, password_hash, salt, role) VALUES (?, ?, ?, ?, ?)',
                       (account_id, username, password_hash, salt, role))
        conn.commit()

    @staticmethod
    def authenticate_user(username, password):
        cursor.execute('SELECT password_hash, salt, role FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            password_hash, salt, role = user
            test_hash, _ = Login.hash_password(password, salt)
            if test_hash == password_hash:
                return role  # This will return the role of the user if authentication is successful
        return None

# Below is a function to compute the checksum of a data record 
# The function will take the data as input and compute the SHA-256 hash of the data
# The function will return the checksum of the data as a hexadecimal string
# This is to ensure data integrity and prevent data tampering in the database
def compute_checksum(data):
    return hashlib.sha256(data).hexdigest()

# Below is a function to create a record to the database and log the modification to the database (admin privilege only)
# The function will take the username, password, table name, and data as input
# The function will authenticate the user based on the provided username and password
# The function will check if the user is an admin to add the record to the database
def add_record(username, password, table, data):
    role = Login.authenticate_user(username, password)
    if role != 'admin':
        print("Permission Denied: Only administrators can create records.")
        return

    placeholders = ', '.join(['?' for _ in data])     # This will create placeholders for the values to be inserted
    columns = ', '.join(data.keys())                  # This will create columns for the values to be inserted
    values = tuple(data.values())                     # This will create a tuple of values to be inserted

# Below checks if the table is 'musical_recordings' and computes the checksum of the recording data
# The checksum is added to the columns and values to be inserted into the database
# This is to ensure data integrity and prevent data tampering in the database
# The cursor will execute the insert query to add the record to the database
# The conn.commit() will commit the changes to the database
    if table == 'musical_recordings':
        checksum = compute_checksum(data['recording'])
        columns += ', checksum'
        placeholders += ', ?'
        values += (checksum,)

    cursor.execute(f'INSERT INTO {table} ({columns}) VALUES ({placeholders})', values)
    record_id = cursor.lastrowid
    cursor.execute('INSERT INTO modification_history (table_name, action, record_id) VALUES (?, ?, ?)',
                   (table, 'INSERT', record_id))
    conn.commit()
    print(f"Record added to {table}. Timestamp: {datetime.now()}")

# Below is a function to remove a record and log the modification to the database (admin privilege only)
# The function will take the username, password, table name, and record ID as input
# The function will authenticate the user based on the provided username and password
# The function will check if the user is an admin to delete the record from the database
# The cursor will execute the delete query to remove the record from the database
# The cursor will execute the insert query to log the modification history of the record in the database
# This will be used by the admin user to track the modification history of records in the database
# There will also be a datetime stamp to track the time of the modification
# The conn.commit() will commit the changes to the database
def remove_record(username, password, table, record_id):
    role = Login.authenticate_user(username, password)
    if role != 'admin':
        print("Permission Denied: Only administrators can delete records.")
        return

    cursor.execute(f'DELETE FROM {table} WHERE id = ?', (record_id,))
    cursor.execute('INSERT INTO modification_history (table_name, action, record_id) VALUES (?, ?, ?)',
                   (table, 'DELETE', record_id))
    conn.commit()
    print(f"Record deleted from {table}. Timestamp: {datetime.now()}")

# Below is a function to register a user account in the database
# The function will prompt the user to enter their first name, last name, date of birth, email, username, password, and role
# The function will check if the email and username already exist in the database
# If the email and username do not exist, the function will add the user to the database
# When the user has input the details, a prompt will ask the user to enter the role (user/admin)
# For the purpose of this script, this is to allow admin privileges and display the CRUD operations
def register_user():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
    email = input("Enter email: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (user/admin): ").lower()

    cursor.execute('SELECT id FROM accounts WHERE email = ?', (email,))
    if cursor.fetchone():
        print(f"Registration failed: An account with email {email} already exists.")
        return None, None

    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    if cursor.fetchone():
        print(f"Registration failed: A user with username {username} already exists.")
        return None, None

    account = Account(first_name, last_name, date_of_birth, email)
    account_id = account.save()
    Login.add_user(account_id, username, password, role)
    print(f"User {username} registered successfully.")
    return username, password

# Below is a function to clean up the database by deleting the admin and user accounts from the database
# This is to remove the test data from the database and prevent duplication of data
# The cursor will execute the delete query to remove the admin and user accounts from the database
def clean_up():
    cursor.execute('DELETE FROM users WHERE username IN ("admin", "user")')
    cursor.execute('DELETE FROM accounts WHERE email IN ("admin@example.com", "user@example.com")')
    conn.commit()

# Below is a function to add a list of sample songs to the database
# The function will add sample songs with lyrics, music scores, and musical recordings to the database
# This is to prevent the database from being empty and having to manually add data into the database
# Further data can be input into the database by the admin user in the records.py script
def add_sample_songs(username, password):
    songs = [
        ('Song 1', 'Lyrics of Song 1', b'PDF_BINARY_DATA_1', b'MP3_BINARY_DATA_1'),
        ('Song 2', 'Lyrics of Song 2', b'PDF_BINARY_DATA_2', b'MP3_BINARY_DATA_2'),
        ('Song 3', 'Lyrics of Song 3', b'PDF_BINARY_DATA_3', b'MP3_BINARY_DATA_3'),
        ('Song 4', 'Lyrics of Song 4', b'PDF_BINARY_DATA_4', b'MP3_BINARY_DATA_4'),
        ('Song 5', 'Lyrics of Song 5', b'PDF_BINARY_DATA_5', b'MP3_BINARY_DATA_5')
    ]

# Below will add the sample songs to the database by calling the add_record function
# The add_record function will add the sample songs to the lyrics, music_scores, and musical_recordings tables in the database
# The add_record function will also log the modification history of the records in the modification_history table in the database
    for song in songs:
        add_record(username, password, 'lyrics', {'song_title': song[0], 'lyrics': song[1]})
        add_record(username, password, 'music_scores', {'song_title': song[0], 'score': song[2]})
        add_record(username, password, 'musical_recordings', {'song_title': song[0], 'recording': song[3]})

# Below is a function to list songs with their modification history in the database
# The function will join the musical_recordings and modification_history tables 
# This will display the song title, timestamp, action, and modified timestamp of the records in the database
# This will be used by the admin user to track the modification history of records in the database
# The cursor will execute the select query to fetch the song title, timestamp, action, and modified timestamp of the records
def list_songs_with_history():
    cursor.execute('''
    SELECT m.song_title, m.timestamp, h.action, h.timestamp 
    FROM musical_recordings m 
    JOIN modification_history h ON m.id = h.record_id 
    WHERE h.table_name = 'musical_recordings'
    ''')
    songs = cursor.fetchall()
    for song in songs:
        print(f"Title: {song[0]}, Added on: {song[1]}, Action: {song[2]}, Modified on: {song[3]}")

# Below is the main function to execute the registration process 
# The main function will prompt the user to enter details to register an account
# The main function will authenticate the user based on the provided username and password
# If the user is admin, the sample list will be displayed along with the modification history 
# If the user is a regular user, the user will not be able to view the modification history 
def main():
    clean_up()
    print("Please enter details to register an account...")
    username, password = register_user()

    if username and password:
        role = Login.authenticate_user(username, password)
        if role == 'admin':
            add_sample_songs(username, password)
            list_songs_with_history()

# Below will execute the main function when the script is run
if __name__ == "__main__":
    main()

# Below will close the connection to the database
conn.close()

