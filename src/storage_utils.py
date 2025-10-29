import sqlite3
from dotenv import dotenv_values

# Environment Variables
STORAGE_FILE = f"{dotenv_values(".env")["STORAGE_FILE"]}" 

# Storage Format
## - SQLite Database, where entities are returned as lists
## - For interface, the lists can be fed to class constructors for creating views

## REGULAR OPERATIONS ##
## OPEN ## SQLite Connection
def open():
    connection = sqlite3.connect(STORAGE_FILE)
    cursor = connection.cursor()
    return connection, cursor

## SAVE ##
def save(connection):
    connection.commit()

## CLOSE ##
def close(connection, cursor):
    cursor.close()
    connection.close()

def save_and_close(connection, cursor):
    save(connection)
    close(connection, cursor)
## REGULAR OPERATIONS END ##

## CREATE ##
def create_user(name, hash, salt):
    connection, cursor = open()
    cursor.execute("INSERT INTO User (name, password, salt) VALUES (?, ?, ?)", (name, hash, salt))
    save_and_close(connection, cursor)

def create_account(user_id, name, email, description, encrypted_password):
    connection, cursor = open()
    cursor.execute("INSERT INTO Account (user_id, name, email, description, password) VALUES (?, ?, ?, ?, ?)", (user_id, name, email, description, encrypted_password))
    save_and_close(connection, cursor)
## CREATE END ##

## READ ##
def get_users():
    connection, cursor = open()
    cursor.execute("SELECT * FROM User")
    users = cursor.fetchall()
    save_and_close(connection, cursor)
    return users

def get_user(user_id):
    connection, cursor = open()
    cursor.execute("SELECT * FROM User WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    save_and_close(connection, cursor)
    return user

def get_user_by_name(name):
    connection, cursor = open()
    cursor.execute("SELECT * FROM User WHERE name = ?", (name,))
    user = cursor.fetchone()
    save_and_close(connection, cursor)
    return user

def get_all_accounts():
    connection, cursor = open()
    cursor.execute("SELECT * FROM Account")
    accounts = cursor.fetchall()
    save_and_close(connection, cursor)
    return accounts

def get_accounts(user_id):
    connection, cursor = open()
    cursor.execute("SELECT * FROM Account WHERE user_id = ?", (user_id,))
    accounts = cursor.fetchall()
    save_and_close(connection, cursor)
    return accounts

def get_account(account_id, user_id):
    connection, cursor = open()
    cursor.execute("SELECT * FROM Account WHERE account_id = ? AND user_id = ?", (account_id, user_id))
    account = cursor.fetchone()
    save_and_close(connection, cursor)
    return account
## READ END ##

## UPDATE ##
# User
def update_user_name(name, user_id):
    connection, cursor = open()
    cursor.execute("UPDATE User SET name = ? WHERE user_id = ?", (name, user_id))
    save_and_close(connection, cursor)
def update_user_password(password, user_id):
    connection, cursor = open()
    cursor.execute("UPDATE User SET password = ? WHERE user_id = ?", (password, user_id))
    save_and_close(connection, cursor)
def update_user_salt(salt, user_id):
    connection, cursor = open()
    cursor.execute("UPDATE User SET salt = ? WHERE user_id = ?", (salt, user_id))
    save_and_close(connection, cursor)

def update_user(field : str, entry, user_id):
    if field == "name":
        update_user_name(entry, user_id)
    elif field == "password":
        update_user_password(entry, user_id)
    elif field == "salt":
        update_user_salt(entry, user_id)

# Account
def update_account_name(name, account_id, user_id):
    connection, cursor = open()
    cursor.execute("UPDATE Account SET name = ? WHERE account_id = ? AND user_id = ?", (name, account_id, user_id))
    save_and_close(connection, cursor)
def update_account_email(email, account_id, user_id):
    connection, cursor = open()
    cursor.execute("UPDATE Account SET email = ? WHERE account_id = ? AND user_id = ?", (email, account_id, user_id))
    save_and_close(connection, cursor)
def update_account_description(description, account_id, user_id):
    connection, cursor = open()
    cursor.execute("UPDATE Account SET description = ? WHERE account_id = ? AND user_id = ?", (description, account_id, user_id))
    save_and_close(connection, cursor)
def update_account_password(password, account_id, user_id):
    connection, cursor = open()
    cursor.execute("UPDATE Account SET password = ? WHERE account_id = ? AND user_id = ?", (password, account_id, user_id))
    save_and_close(connection, cursor)

def update_account(field : str, entry, account_id, user_id):
    if field == "name":
        update_account_name(entry, account_id, user_id)
    elif field == "email":
        update_account_email(entry, account_id, user_id)
    elif field == "description":
        update_account_description(entry, account_id, user_id)
    elif field == "password":
        update_account_password(entry, account_id, user_id)
## UPDATE END ##

## DELETE ##
# User
def delete_user(user_id):
    connection, cursor = open()
    cursor.execute("DELETE FROM User WHERE user_id = ?", (user_id,))
    save_and_close(connection, cursor)
# Account
def delete_account(account_id):
    connection, cursor = open()
    cursor.execute("DELETE FROM Account WHERE account_id = ?", (account_id,))
    save_and_close(connection, cursor)
## DELETE END ##

# Tests
DEBUG = False
if __name__ == "__main__":
    if DEBUG == True:
        pass
    pass