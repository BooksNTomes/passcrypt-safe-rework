from src.interface import run
from plugins.note_encryption import run as ncrypt_run

## Debug Variables
RESET_DB = False
DEBUG = 0

if __name__ == "__main__":
    ## Main Program
    if DEBUG == 0:
        ## Run interface layer
        run(RESET_DB)
    ## Note Encryption / Decryption
    if DEBUG == 1:
        ncrypt_run()