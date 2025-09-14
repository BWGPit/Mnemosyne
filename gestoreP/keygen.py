from cryptography.fernet import Fernet
import os
from load_dotenv import load_dotenv
load_dotenv()

def generate_key():
	if os.getenv("KEY") == None or os.getenv("KEY") == "ENTER A VALID ENCRYPTION KEY":
		with open(".env", "a+") as env:
			env.write(f'\nKEY="{str(Fernet.generate_key())}"')
		print("An encryption key was succesfully generated")
	else:
		print("This program already has an encryption key")

if __name__ == "__main__":
	generate_key()