import src.cryptography_utils as crypt
import src.storage_utils as store
import src.initialize_database as initdb
from src.classes import User, Account
from typing import List

from maskpass import askpass

## INTERFACE ##
# Consists of the outer frontend layer and the backend layer beneath it
# TODO : Frontend in TUI is difficult to separate from the backend due to logic, but separation would be beneficial

DEBUG = 0

## Backend Layer
def register_user(name : str, password : str, reentered_password : str) -> bool:
    if name != None and password != None and reentered_password == password:
        try:
            # Create New User : storage_utils
            hash, salt = crypt.hash(password)
            store.create_user(name, hash, salt)
        except Exception: # SQL EXCEPTION
            return False
        return True
    return False

def authenticate_user(name : str, password : str) -> bool:
    try:
        # Load User
        salt = store.get_user_by_name(name)[-1]
        if (DEBUG):
            print(salt)

        hash = crypt.verify_hash(password, salt)
        if (DEBUG):
            print(hash)
        stored = store.get_user_by_name(name)[2]
        if (DEBUG):
            print(stored)

        if hash == stored:
            return True
        return False
    except Exception:
        print("Error")
    return False
    
def load_user(name : str, password : str):
    # name is used to get user as a class
    user = User(store.get_user_by_name(name))
    # set key
    key = crypt.get_key(user.name, password, user.salt)
    # accounts are loaded as class list
    loaded_accounts = store.get_accounts(user.user_id)
    accounts : List[Account] = []
    for account in loaded_accounts:
       account_class = Account(account)
       # key is used to decrypt
       account_class.password = crypt.decrypt(key, account[4])
       accounts.append(account_class)
    return user, accounts, key

## Frontend Layer
def frontend():
    while (True):
        # Start Page
        print()
        print("Passcrypt Safe - Password Storage")
        print("[L]ogin | [R]egister | [E]xit")
        print()
        cmd = input("> ")

        if cmd.upper() == "L":
            # Login
            print()
            name = input("Login> Enter Username> ")
            password = askpass("Login> Enter Password> ")
            print()
            # Authenticate
            if authenticate_user(name, password):
                # Dashboard
                while (True):
                    # Load User
                    user, accounts, key = load_user(name, password)
                    
                    # Print All Accounts
                    for account in accounts:
                        print()
                        print(f"account_id : {account.account_id}")
                        print(f"name : {account.name}")
                        print(f"email : {account.email}")
                        print(f"description : {account.description}")
                        print(f"password : {account.password}")
                        print()

                    # Prompt User
                    print()
                    print("ad -> add account")
                    print("md [account_id] -> modify account")
                    print("rm [account_id] -> remove account")
                    print("ed -> edit password")
                    print("lg -> logout")
                    print()
                    cmd = input("> ")

                    # Command Split : prm parameter and cmd command
                    if (len(cmd.split(' ')) > 1):
                        prm = cmd.split(' ')[1]
                        cmd = cmd.split(' ')[0]

                        # Add Account
                        if (cmd.lower() == 'ad'):
                            # Get New Parameters
                            account_name = input(f"Enter Name> ")
                            print(account_name)
                            account_email = input(f"Enter Email> ")
                            print(account_email)
                            account_description = input(f"Enter Description> ")
                            print(account_description)
                            account_password = input(f"Enter Password> ")
                            print(account_password)
                            
                            # Create Credentials
                            account_password = crypt.encrypt(key, password)
                            store.create_account(user.user_id, account_name, account_email, account_description, account_password)
                            print("Created New Account")
                    try:
                        # Modify Account
                        if (cmd.lower() == 'md'):
                            # Get Account
                            account = Account(store.get_account(prm, user.user_id))

                            # Get New Parameters
                            print("Leave blank if no modification")
                            account_name = input(f"Editing Account {account.account_id}> Enter New Name> ")
                            print(account_name)
                            account_email = input(f"Editing Account {account.account_id}> Enter New Email> ")
                            print(account_email)
                            account_description = input(f"Editing Account {account.account_id}> Enter New Description> ")
                            print(account_description)
                            account_password = input(f"Editing Account {account.account_id}> Enter New Password> ")
                            print(account_password)
                            
                            # Update Credentials
                            if account_name != "":
                                store.update_account("name", account_name, account.account_id, user.user_id)
                            if account_email != "":
                                store.update_account("email", account_email, account.account_id, user.user_id)
                            if account_description != "":
                                store.update_account("description", account_description, account.account_id, user.user_id)
                            if account_password != "":
                                account_password = crypt.encrypt(key, account_password)
                                store.update_account("password", account_password, account.account_id, user.user_id)
                            else:
                                pass
                            print("Updated Credentials")

                        # Remove Account
                        if (cmd.lower() == "rm"):
                            # Get Account
                            account = Account(store.get_account(prm, user.user_id))
                            # Deletion Decision
                            decision = input(f"Deleting Account {account.name}> Are You Sure? [y]es / [n]o> ")
                            if (decision.lower() == "y"):
                                store.delete_account(prm)
                            else:
                                print("Aborting Deletion.")
                                continue
                    except Exception:
                        print("No Account ID Provided")
                        continue

                    # Edit
                    if (cmd.lower() == 'ed'):
                        # Authenticate
                        print()
                        old_password = askpass("Authenticate> Enter Password> ")
                        print()
                        if authenticate_user(user.name, old_password):
                            # Edit Proper
                            print()
                            print("Leave blank if no modification")
                            new_password = askpass("Edit Password> Enter New Password> ")
                            print(new_password)

                            # Update Credentials
                            credentials_changed = False
                            if new_password != "":
                                store.update_user("password", new_password, user.user_id)
                                credentials_changed = True
                            else:
                                credentials_changed = False
                                
                            # Reencrypt -> Return to login
                            if (credentials_changed):
                                # New Key and its Salt
                                stored_password = new_password
                                new_password, new_salt = crypt.hash(new_password)
                                new_key = crypt.get_key(name, stored_password, new_salt)

                                # Reencrypt Passwords of All Accounts
                                for account in accounts:
                                    # decrypted = crypt.decrypt(key, account.password)
                                    encrypted = crypt.encrypt(new_key, account.password)
                                    store.update_account("password", encrypted, account.account_id, user.user_id)
                                    print("Reencrypted Credentials")
                                
                                # Update User Credentials
                                store.update_user("password", new_password, user.user_id)
                                store.update_user("salt", new_salt, user.user_id)
                                # Logging Out Message
                                print("User Credentials Changed, Logging Out> ")
                                break
                            else:
                                print("Credentials Unchanged")
                        else:
                            print("Incorrect Password")
                            continue

                    # Logout
                    if (cmd.lower() == 'lg'):
                        break

                    # Error Handling : Incorrect Input
                    else:
                        print("Incorrect Input")
                        continue
                continue
            else:
                print("Incorrect Credentials")
                continue

        if cmd.upper() == "R":
            # Register
            print()
            name = input("Register> Enter Username> ")
            password = askpass("Register> Enter Password> ")
            reentered_password = askpass("Register> Reenter Password> ")
            print()
            # Create User
            if register_user(name, password, reentered_password):
                print("Registration Successful")
            else:
                print("Registration Failure")
            continue

        else:
            print("Closing Program> ")
            break
    
## Main
def run(reset : bool = False):
    initdb.initialize_tables(reset=False)
    frontend()

if __name__ == '__main__':
    pass