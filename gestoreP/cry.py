from cryptography.fernet import Fernet
import os
from load_dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("KEY")

def encryptfile(file: str):
    filename = file.split(".")[0]
    
    fernet = Fernet(KEY)

    with open(file, "rb") as x:
        original = x.read()
    
    encrypted = fernet.encrypt(original)

    with open(file, "wb") as e:
        e.write(encrypted)

def decryptfile(file):
    filename = file.split(".")[0]
    
    fernet = Fernet(KEY)

    with open(file, "rb") as e:
        encrypted = e.read()
    
    decrypted = fernet.decrypt(encrypted)

    with open(file, "wb") as f:
        f.write(decrypted)

if __name__ == "__main__":
    decryptfile(file="filetoencrypt.txt")
