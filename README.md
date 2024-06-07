Hello and welcome to the Music Library Management System. This application is designed in three (3) main Python scripts named:

#### Main.py

#### Login.py

#### Records.py

GitHub Repository: https://github.com/anja-kosar/Music-Library-Management-System 

They will each be described in more detail below.
The idea behind this project is to build a command-line application with a database in which musical recordings, lyrics and music scores can be stored. These artefacts can be viewed by regular users and administrator users, with administrators having CRUD function privileges. 
The project was written in Python3 using Visual Studio Code. The design was created by following the UML Class Diagram submitted in week 3 design report. In the Python scripts, the database module SQLite3 was imported using the import function. SQLite3 is a self-contained, file-based SQL database which comes bundled with Python and can be used in any Python application without having to install any additional software. It operates by creating a file on the user’s computer, in which data can be accessed (Muller, D. 2020). The database contains various tables for storing artefacts, user accounts and modification history, as well as functions for generating a checksum to confirm the integrity of the artefacts, the ability to encrypt the artefact and date/time stamp function which will hold a record of creation, modification and removal of artefacts.

## Main.py Script
This script is the foundation of the application in which individual database tables have been created. The database consists of the following tables:

* Musical Recordings

* Lyrics

* Music Scores 

* Modification History 

* Accounts

* Users 

All db tables have a primary key which is a unique identifier for each record in the table, a date/time stamp to track modification history and basic info depending on table, for example ‘lyrics’, ‘recording’ or ‘score’. The musical recording table is a BLOB (binary large object), which can store binary data. Before inserting a recording into the table, the recording would be hashed, using the hashlib module, which was also imported into the scripts and used throughout the application for encryption purposes. After hashing the recording, the value would be stored in the checksum column. When retrieving the recording from the database, its integrity would be verified by comparing the hash of the retrieved recording with the stored hash in the checksum column (Python org. N.D). The users table holds a similar concept where the username and passwords are stored, using a hash and random salt value for security purposes. 
Once the database tables were established, a class was created for user accounts where the user would have to input their first name, last name, date of birth, email address to register the details into the table. This was followed by a login class where a static method was used to hash password, add user and authenticate the user. A static method in Python is a method that belongs to a class, not its instances. It does not require an instance of the class to be called, nor does it have access to an instance (Hostman, N.D). This was convenient as hashing, adding and authentication were bound to the login class. 
This was followed by two functions where only admin could create and remove a record, with a sample list of songs, lyrics and scores pre-input, for the purpose of demonstrating the CRUD functions by admin user and save time on manually having to enter each data set.

## Login.py Script

This script showcases the basic login functions using the username and password previously created when registering an account in the main.py section. The application will prompt a user to enter username and password, which will recognize whether the user is a regular user or admin, based on the db. Depending on what the user selects, the application will display a message giving further instructions.

## Records.py Script

This script showcases the CRUD functions using the username and password previously created when registering an account in the main.py section. Based on the role of the user, the database library cam either be viewed, created or deleted. 

# Application Instructions
1.	For the application to run as designed, please navigate to the main.py script and run the script in terminal. The application will prompt to enter user details to register. After entering the desired username and password, the application will ask whether you would like to be user or admin. For this exercise, create an account for each role (1 user and 1 admin). After doing so, the application will create a music_library.db file in which the necessary tables will be created, storing artefacts.
2.	Once this is complete, navigate to the login.py script and run the script in terminal. The application will prompt to enter the username and password previously created. Depending on which user is entered, the appropriate message will display. 
3.	Once this is complete, navigate to the records.py script and run the script in terminal. Depending on which user is entered, the appropriate instructions will follow. If the ‘user’ role is logged in, the library will be in view only mode. If the ‘admin’ user is logged in, the admin may perform CRUD functionalities, as per the system prompt. 

## Testing
For testing the above scripts, Flake8 and Bandit were applied, using pip install functions in terminal. These are the reports below:

### Flake8 Testing

![alt text](<Images/Flake8 Main Test.png>)
Figure 1.1 Flake8 test on main.py script

##





![alt text](<Images/Flake8 Login Test.png>)
Figure 1.2 Flake8 test on login.py

##




![alt text](<Images/Flake8 Records Test.png>)
Figure 1.3 Flake8 test on records.py

As displayed in the figures 1.1 – 1.3. each test indicates that there are existing issues with comment lines being too long (E501). There was also trailing whitespace (W291), blank lines containing whitespace (W293) and expecting two blank lines Line lengths are recommended to be no greater than 79 characters. The reasoning for this comes from PEP8 itself by limiting the required editor window width makes it possible to have several files open side-by-side and works well when using code review tools that present the two versions in adjacent columns. It is common for developers, especially those in closed-source projects, to change the maximum line length to 100 or 120 characters. (Flake8 Rules, N.D)


### Bandit Testing

![alt text](<Images/Bandit Main Test.png>)
Figure 2.1 Bandit test on main.py

##


![alt text](<Images/Bandit Login Test.png>)
Figure 2.2. Bandit Test on login.py

##


![alt text](<Images/Bandit Records Test.png>)

Figure 2.3 Bandit test on records.py

#

Without sufficient removal or quoting of SQL syntax in user-controllable inputs, the generated SQL query can cause those inputs to be interpreted as SQL instead of ordinary user data. This can be used to alter query logic to bypass security checks, or to insert additional statements that modify the back-end database, possibly including execution of system commands.
SQL injection has become a common issue with database-driven web sites. The flaw is easily detected, and easily exploited, and as such, any site or product package with even a minimal user base is likely to be subject to an attempted attack of this kind. This flaw depends on the fact that SQL makes no real distinction between the control and data planes. (Mitre, 2018).

The above description from the Mitre website explains the Bandit testing results and further give instructions on how this can be avoided. 




#### References:

Chan, S. (2021). SQLite in VSCode (open db, run que
ry, view results) demo. YouTube. Available from: https://www.youtube.com/watch?v=VKg1Dnz7GN0 [Accessed 28 May 2024].

Muller, D. (2020). How To Use the sqlite3 Module in Python 3. [online] DigitalOcean. Available from: https://www.digitalocean.com/community/tutorials/how-to-use-the-sqlite3-module-in-python-3. [Accessed 28 May 2024]. 

PYnative. (2019). Python SQLite tutorial [Complete Guide]. [online] Available from: https://pynative.com/python-sqlite/. [Accessed 28 May 2024].

docs.python.org. (n.d.). hashlib — Secure hashes and message digests — Python 3.8.4rc1 documentation. [online] Available from: https://docs.python.org/3/library/hashlib.html. [Accessed 28 May 2024].

Hostman. (n.d.). Python static method: A Step-by-Step Guide. [online] Available from: https://hostman.com/tutorials/python-static-method/. [Accessed 28 May 2024].

www.flake8rules.com. (n.d.). Line too long (82 > 79 characters) (E501). [online] Available from: https://www.flake8rules.com/rules/E501.html. [Accessed 28 May 2024].

mitre (2013). CWE - CWE-89: Improper Neutralization of Special Elements used in an SQL Command (‘SQL Injection’) (3.4.1). [online] Mitre.org. Available from: https://cwe.mitre.org/data/definitions/89.html. [Accessed 28 May 2024].

bandit.readthedocs.io. (n.d.). Welcome to Bandit’s developer documentation! — Bandit documentation. [online] Available from: https://bandit.readthedocs.io/en/latest/. [Accessed 28 May 2024].


