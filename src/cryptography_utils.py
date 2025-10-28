import cryptography
from cryptography.fernet import Fernet
import bcrypt
import hashlib
import base64

# INSECURE : Change When Personalizing System
NOT_SALT = b'$2b$12$bbFRQG5/7p7N/VZVcd.RhO'

## HASH ##
def hash(password : str, include_salt : bool = True):
    # encode
    bytes = password.encode('utf-8')
    # salt
    salt = bcrypt.gensalt()
    # hash
    hashed = bcrypt.hashpw(bytes, salt)
    if not include_salt:
        return hashed.decode()
    return hashed.decode(), salt
## HASH END ##
## VERIFY HASH ##
def verify_hash(password : str, salt : str):
    # encode
    bytes = password.encode('utf-8')
    # hash
    hashed = bcrypt.hashpw(bytes, salt) # type: ignore
    return hashed.decode()
## VERIFY HASH END ##

## SALTLESS HASH ##
def no_salt_hash(text):
    # encode
    bytes = text.encode('utf-8')
    # hash
    hashed = bcrypt.hashpw(bytes, NOT_SALT)
    return hashed.decode()
## SALTLESS HASH END ##

## KEY GENERATION ##
def derive_key(name : str, password : str):
    hashed_key1 : str = no_salt_hash(password)
    hashed_key2 : str = no_salt_hash(name + password)
    salt = bcrypt.gensalt()
    
    key = hashed_key1 + hashed_key2
    key = bcrypt.hashpw(key.encode(), salt)
    key = hashlib.sha256(key).digest()
    key = base64.urlsafe_b64encode(key)

    return Fernet(key), salt
## KEY GENERATION END ##

## RETRIEVE USER KEY ##
def get_key(name, password, salt):
    hashed_key1 : str = no_salt_hash(password)
    hashed_key2 : str = no_salt_hash(name + password)
    
    key = hashed_key1 + hashed_key2
    key = bcrypt.hashpw(key.encode(), salt)
    key = hashlib.sha256(key).digest()
    key = base64.urlsafe_b64encode(key)

    return Fernet(key)
## RETRIEVE USER KEY END ##

## ENCRYPT ##
def encrypt(key : Fernet, text: str):
    # convert argument
    ciphertext = key.encrypt(text.encode())
    # return argument
    return ciphertext.decode()
## ENCRYPT END ##

## DECRYPT ##
def decrypt(key : Fernet, ciphertext : str):
    # convert argument
    text = key.decrypt(ciphertext.encode())
    # return argument
    return text.decode()
## DECRYPT END ##

## ALTERNATIVE / EXPERIMENTAL ##
## KEY GENERATION ALTERNATIVE ##
def derive_key_alternative(name : str, password : str):
    hashed_key1 : str = no_salt_hash(password)
    hashed_key2 : str = no_salt_hash(name + password)
    salt = bcrypt.gensalt()
    
    key = hashed_key1 + hashed_key2
    key = bcrypt.hashpw(key.encode(), salt)
    key = hashlib.sha256(key).digest()
    key = base64.urlsafe_b64encode(key)

    return key, salt
## KEY GENERATION ALTERNATIVE END ##

## RETRIEVE KEY ALTERNATIVE ##
def get_key_alternative(name, password, salt):
    hashed_key1 : str = no_salt_hash(password)
    hashed_key2 : str = no_salt_hash(name + password)
    
    key = hashed_key1 + hashed_key2
    key = bcrypt.hashpw(key.encode(), salt)
    key = hashlib.sha256(key).digest()
    key = base64.urlsafe_b64encode(key)

    return key
## RETRIEVE KEY ALTERNATIVE END ##

## RANDOM KEY ##
def derive_random_key():
    return Fernet.generate_key()
## RANDOM KEY END ##

## RETRIEVE KEY ##
def retrieve_key(key : bytes):
    return Fernet(key)
## RETRIEVE KEY END ##

# Tests
DEBUG = False
if __name__ == "__main__":
    if DEBUG == True:
        pass