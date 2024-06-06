"""
This module contains functions to manage a music library database.
It provides functionality to authenticate users, view lyrics, music scores, and musical recordings,
as well as create, delete, and add various artifacts in the library.
"""

import hashlib                        # Hashlib library for hashing functions          
import sqlite3                        # SQLite library for database operations
from datetime import datetime         # Datetime library for timestamping records

# Below connects to the SQLite database and creates a cursor object to execute SQL queries
conn = sqlite3.connect('music_library.db')
cursor = conn.cursor()

# Below is a function to authenticate user based on the provided username and password
# The function will query the users table in the database to retrieve the stored hash, salt, and role for the provided username
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

# Below is a function to view lyrics from the lyrics table in the database
# The cursor will execute the SQL query to select all data from the lyrics table
# The select query will fetch all the rows from the table and display the data in the console
# The function will print the ID, Title, and Lyrics of each record in the lyrics table
def view_lyrics():
    conn = sqlite3.connect('music_library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lyrics')
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        print(f"ID: {row[0]}, Title: {row[1]}, Lyrics: {row[2]}")

# Below is a function to view music scores from the music_scores table in the database
# The cursor will execute the SQL query to select all data from the music_scores table
# The select query will fetch all the rows from the table and display the data in the console
# The function will print the ID, Title, and Score of each record in the music_scores table
def view_music_scores():
    conn = sqlite3.connect('music_library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM music_scores')
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        print(f"ID: {row[0]}, Title: {row[1]}, Score: {row[2]}")

# Below is a function to view musical recordings from the musical_recordings table in the database
# The cursor will execute the SQL query to select all data from the musical_recordings table
# The select query will fetch all the rows from the table and display the data in the console
# The function will print the ID, Title, Recording, and Checksum of each record in the musical_recordings table
def view_musical_recordings():
    conn = sqlite3.connect('music_library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM musical_recordings')
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        print(f"ID: {row[0]}, Title: {row[1]}, Recording: {row[2]}, Checksum: {row[3]}")

# Below is a function to create lyrics in the lyrics table of the database
# The function will insert the provided song title and lyrics into the lyrics table
# The cursor will execute the SQL query to insert the song title and lyrics into the lyrics table
# The function will commit the changes to the database and close the connection
def create_lyrics(song_title, lyrics):
    conn = sqlite3.connect('music_library.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO lyrics (song_title, lyrics, timestamp) VALUES (?, ?, ?)', (song_title, lyrics, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    print(f"Lyrics for '{song_title}' added successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.") 

# Below is a function to add music scores in the music_scores table of the database
# The function will insert the provided song title and score into the music_scores table
# The cursor will execute the SQL query to insert the song title and score into the music_scores table
# The function will commit the changes to the database and close the connection
def add_music_score(song_title, score):
    conn = sqlite3.connect('music_library.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO music_scores (song_title, score) VALUES (?, ?)', (song_title, score))
    conn.commit()
    conn.close()
    print(f"Music score for '{song_title}' added successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

# Below is a function to add musical recordings in the musical_recordings table of the database
# The function will insert the provided song title and recording into the musical_recordings table
# The cursor will execute the SQL query to insert the song title and recording into the musical_recordings table
# This function will also calculate the checksum of the recording using the hashlib library
# The function will also keep a date and time stamp of when the recording was added
def add_musical_recording(song_title, recording):
    checksum = hashlib.sha256(recording).hexdigest()
    conn = sqlite3.connect('music_library.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO musical_recordings (song_title, recording, checksum) VALUES (?, ?, ?)', (song_title, recording, checksum))
    conn.commit()
    conn.close()
    print(f"Musical recording for '{song_title}' added successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

# Below is a function to delete lyrics from the lyrics table in the database (admin only)
# The function will delete the lyrics for the provided song title from the lyrics table
# The cursor will execute the SQL query to delete the lyrics based on the song title
# The function will also keep a date and time stamp of when the lyrics were deleted
def delete_lyrics(song_title):
    conn = sqlite3.connect('music_library.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM lyrics WHERE song_title = ?', (song_title,))
    conn.commit()
    conn.close()
    print(f"Lyrics for '{song_title}' deleted successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

# Below is a function to delete music scores from the music_scores table in the database (admin only)
# The function will delete the music score for the provided song title from the music_scores table
# The cursor will execute the SQL query to delete the music score based on the song title
# The function will also keep a date and time stamp of when the music score was deleted
def delete_music_score(song_title):
    conn = sqlite3.connect('music_library.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM music_scores WHERE song_title = ?', (song_title,))
    conn.commit()
    conn.close()
    print(f"Music score for '{song_title}' deleted successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")


# # Below is a function to delete musical recordings from the musical_recordings table in the database (admin only)
# The function will delete the musical recording for the provided song title from the musical_recordings table
# The cursor will execute the SQL query to delete the musical recording based on the song title
# The function will also keep a date and time stamp of when the musical recording was deleted
def delete_musical_recording(song_title):
    conn = sqlite3.connect('music_library.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM musical_recordings WHERE song_title = ?', (song_title,))
    conn.commit()
    conn.close()
    print(f"Musical recording for '{song_title}' deleted successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

# Below is the main function to execute the login process.
# The user will be prompted to enter their username and password.
# The authenticate_user function will be called to verify the user's credentials.
# These credentials are stored in the users table in the database which were created in the main.py script
# If the user is authenticated, the user's role will be returned.
# The user will be welcomed with a 'Welcome, user!' or 'Welcome, administrator!' message based on their role.
def main():
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = authenticate_user(username, password)

    if role is None:
        print("Login Failed: Invalid username or password.")
        return

# Below is a elif conditional statement to check the role of the user and display the appropriate message
# If the role is 'user', the user will be able to view the Music Library
# The view_lyrics, view_music_scores, and view_musical_recordings functions will be called to display the data
# If the role is 'admin', the administrator will be able to perform the CRUD operations on the library artifacts
# The strip() and lower() methods are used to remove any leading/trailing whitespaces and convert the input to lowercase
# This is done to ensure that the input is case-insensitive and to handle any extra spaces in the input
    if role == 'user':
        print("Welcome, user!")
        print("You can now view the Music Management System Library.")
        print("\nLyrics:")
        view_lyrics()
        print("\nMusic Scores:")
        view_music_scores()
        print("\nMusical Recordings:")
        view_musical_recordings()
    elif role == 'admin':
        print("Welcome, administrator!")
        print("You can create or delete library artifacts.")
        action = input("Do you want to create or delete artifacts? (create/delete): ").strip().lower()

# Below is an if-elif conditional statement to check the action the admin wants to perform
# If the action is 'create', the admin will be prompted to enter the type of artifact they want to add (lyrics/score/recording)
# The admin will then be prompted to enter the song title and the corresponding data for the artifact   
# The create_lyrics, add_music_score, and add_musical_recording functions will be called based on the artifact type
# The function will add the artifact based on the song title and keep a date and time stamp of when the artifact was created  
# The strip() and lower() methods are used to remove any leading/trailing whitespaces and convert the input to lowercase
# This is done to ensure that the input is case-insensitive and to handle any extra spaces in the input
        if action == 'create':
            artifact_type = input("What type of artifact do you want to create? (lyrics/score/recording): ").strip().lower()
            song_title = input("Enter song title: ")

# Below are conditional statements to check the artifact type and call the appropriate function to add the artifact
# The create_lyrics, add_music_score, and add_musical_recording functions will be called based on the artifact type          
            if artifact_type == 'lyrics':
                lyrics = input("Enter lyrics: ")
                create_lyrics(song_title, lyrics)
                print(f"Lyrics for '{song_title}' added at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
            elif artifact_type == 'score':
                score = input("Enter music score data (as text): ")
                add_music_score(song_title, score)
                print(f"Music score for '{song_title}' added at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
            elif artifact_type == 'recording':
                recording = input("Enter musical recording data (as text): ").encode()
                add_musical_recording(song_title, recording)
                print(f"Musical recording for '{song_title}' added at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
            else:
                print("Invalid artifact type.")
 
# Below is an elif conditional statement to check if the action is 'delete'
# The admin will be prompted to enter the type of artifact they want to delete (lyrics/score/recording)
# The admin will then be prompted to enter the song title for the artifact they want to delete
# The delete_lyrics, delete_music_score, and delete_musical_recording functions will be called based on the artifact type
# The function will delete the artifact based on the song title and keep a date and time stamp of when the artifact was deleted
# The strip() and lower() methods are used to remove any leading/trailing whitespaces and convert the input to lowercase
# This is done to ensure that the input is case-insensitive and to handle any extra spaces in the input       
        elif action == 'delete':
            artifact_type = input("What type of artifact do you want to delete? (lyrics/score/recording): ").strip().lower()
            song_title = input("Enter song title: ")

# Below are conditional statements to check the artifact type and call the appropriate function to delete the artifact
# The delete_lyrics, delete_music_score, and delete_musical_recording functions will be called based on the artifact type          
            if artifact_type == 'lyrics':
                delete_lyrics(song_title)
                print(f"Lyrics for '{song_title}' deleted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
            elif artifact_type == 'score':
                delete_music_score(song_title)
                print(f"Music score for '{song_title}' deleted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
            elif artifact_type == 'recording':
                delete_musical_recording(song_title)
                print(f"Musical recording for '{song_title}' deleted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
            else:
                print("Invalid artifact type.")
        
        else:
            print("Invalid action.")
    else:
        print("Unknown role.")

if __name__ == "__main__":
    
     main()