import src.cryptography_utils as crypt
from pathlib import Path
import os
## Note Encryption Interface
## TODO : experiment using credential,credential as parameters (make a singular parameter key_derivation function at crypt)

## Backend Layer
def generate_key(with_credential : bool = False, credential : str = None): # type: ignore
    if with_credential:
        return crypt.derive_key_alternative(credential, credential)
    else:
        return crypt.derive_random_key()
def retrieve_key(credential, salt):
    try:
        key = crypt.get_key_alternative(credential, credential, salt)
        return key
    except Exception:
        return None

## Frontend Layer
def note_encryption():
    while (True):
        # Start Page
        print()
        print("Passcrypt Safe - Note Encryption")
        print("[GE]nerate | [RE]trieve | [EN]crypt | [DE]crypt | [E]xit")
        print()
        cmd = input("> ")

        if cmd.upper() == "GE":
            # Generate Key
            print("[W]ith Credential | [WI]thout Credential")
            decision = input("Generate Key> ")
            if (decision.upper() == "W"):
                credential = input("Input Credential> ")
                if credential == '' or credential == None:
                    print("No Credential Given")
                    continue
                key, salt = generate_key(credential) # type: ignore
                print(f"Generated Key: {key.decode()}") # type: ignore
                print(f"Generated Salt: {salt.decode()}") # type: ignore
                print("Remember Your Credential and Salt")
            else:
                key = generate_key()
                print(f"Generated Key: {key.decode()}") # type: ignore
                print("Remember Your Key")
            continue

        if cmd.upper() == "RE":
            # Retrieve Key
            credential = input("Input your Credential> ").encode()
            salt = input("Input your Salt> ").encode()
            key = retrieve_key(credential, salt)
            print(f"Key: {key.decode()}") # type: ignore
            continue

        if cmd.upper() == "EN":
            # Encrypt
            try:
                key = crypt.retrieve_key((input("Enter Key> ").encode()))
                filepath = input("Enter Full Filepath> ")
                new_path = input("Enter Full Filepath of Destination (Leave blank to replace file)> ")

                with open(filepath, 'r') as file:
                    content = file.read()
                    content = crypt.encrypt(key, content)
                if (new_path != ''):
                    filepath = new_path
                with open(filepath, 'w') as file:
                    file.write(content)
            except Exception:
                print("Decryption Failure")
                continue

            print("Filepath Encrypted")
            continue
        
        if cmd.upper() == "DE":
            try:
                # Decrypt
                key = crypt.retrieve_key((input("Enter Key> ").encode()))
                filepath = input("Enter (Full) Filepath> ")
                new_path = input("Enter Full Filepath of Destination (Leave blank to replace file)> ")

                with open(filepath, 'r') as file:
                    content = file.read()
                    content = crypt.decrypt(key, content)
                if (new_path != ''):
                    filepath = new_path
                with open(filepath, 'w') as file:
                    file.write(content)
            except Exception:
                print("Decryption Failure")
                continue

            print("Filepath Decrypted")
            continue

        else:
            print("Closing Program> ")
            break

def run():
    note_encryption()