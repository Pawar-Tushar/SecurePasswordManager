import os 
import sys 
import string , random , hashlib

from getpass import getpass
from rich import print as printc
from rich.console import Console
from argon2 import PasswordHasher

from Utils.dbconfig import Dbconfig


console = Console()

def CheckConfig():
    db = Dbconfig()
    cursor  = db.cursor()
    query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA  WHERE SCHEMA_NAME = 'password_manager'"
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    if len(results) != 0:
        return True
    return False

def makingSalt(length=35):
	return ''.join(random.choices(string.ascii_uppercase + string.digits +  string.ascii_lowercase + string.punctuation, k = length))

def Create():
	if CheckConfig():
		printc("[red][!] Already Configured! [/red]")
		return

	printc("[green][+] Creating new config [/green]")

	# Create database
	db = Dbconfig()
	cursor = db.cursor()
	try:
		cursor.execute("CREATE DATABASE password_manager")
	except Exception as e:
		printc("[red][!] An error occurred while trying to create db. Check if database with name 'pm' already exists - if it does, delete it and try again.")
		console.print_exception(show_locals=True)
		sys.exit(0)

	printc("[green][+][/green] Database 'password_manager' created")

	# Create tables
	query = "CREATE TABLE password_manager.app_secrets (masterkey_hash TEXT NOT NULL, Salt TEXT NOT NULL)"
	res = cursor.execute(query)
	printc("[green][+][/green] Table 'app_secrets' created ")

	query = "CREATE TABLE Password_manager.password_entries (sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
	res = cursor.execute(query)
	printc("[green][+][/green] Table 'entries' created ")


	mp = ""
	printc("[green][+] A [bold]MASTER PASSWORD[/bold] is the only password you will need to remember in-order to access all your other passwords. Choosing a strong [bold]MASTER PASSWORD[/bold] is essential because all your other passwords will be [bold]encrypted[/bold] with a key that is derived from your [bold]MASTER PASSWORD[/bold]. Therefore, please choose a strong one that has upper and lower case characters, numbers and also special characters. Remember your [bold]MASTER PASSWORD[/bold] because it won't be stored anywhere by this program, and you also cannot change it once chosen. [/green]\n")

	while 1:
		mp = getpass("Choose a MASTER PASSWORD: ")
		if mp == getpass("Re-type: ") and mp!="":
			break
		printc("[yellow][-] Please try again.[/yellow]")

	# Hash the MASTER PASSWORD
	ph = PasswordHasher()
	hashed_mp = ph.hash(mp)
	printc("[green][+][/green] Generated hash of MASTER PASSWORD")


	# Generate a device secret
	salt = makingSalt()
	printc("[green][+][/green] Device Secret generated")

	# Add them to db  ds==salt
	query = "INSERT INTO Password_manager.app_secrets (masterkey_hash, Salt) values (%s, %s)"
	val = (hashed_mp, salt)
	cursor.execute(query, val)
	db.commit()

	printc("[green][+][/green] Added to the database")

	printc("[green][+] Configuration done![/green]")

	db.close()

def Remove():
	printc("[red][-] Deleting a config clears the device secret and all your entries from the database. This means you will loose access to all your passwords that you have added into the password manager until now. Only do this if you truly want to 'destroy' all your entries. This action cannot be undone. [/red]")

	while 1:
		op = input("So are you sure you want to continue? (y/N): ")
		if op.upper() == "Y":
			break
		if op.upper() == "N" or op.upper == "":
			sys.exit(0)
		else:
			continue

	printc("[green][-][/green] Deleting config")


	if not CheckConfig():
		printc("[yellow][-][/yellow] No configuration exists to delete!")
		return

	db = Dbconfig()
	cursor = db.cursor()
	query = "DROP DATABASE password_manager"
	cursor.execute(query)
	db.commit()
	db.close()
	printc("[green][+] Config deleted![/green]")

def Recreate():
	print("Recreating the Configuration Again...")
	Remove()
	Create()
	
# if __name__ == "__main__":

# 	if len(sys.argv)!=2:
# 		print("Usage: python db.py <make/delete/remake>")
# 		sys.exit(0)

# 	if sys.argv[1] == "make":
# 		Create()
# 	elif sys.argv[1] == "delete":
# 		Remove()
# 	elif sys.argv[1] == "remake":
# 		Recreate()
# 	else:
# 		print("Usage: python db.py <make/delete/remake>")




# import argon2
# from argon2.exceptions import VerifyMismatchError

# # Function to hash a password (simulating storing it in a database)
# def hash_password(password):
#     # Create an Argon2 PasswordHasher instance
#     argon2_hasher = argon2.PasswordHasher()
#     # Hash the password
#     hashed_password = argon2_hasher.hash(password)
#     return hashed_password

# # Function to verify entered password against the stored hashed password
# def verify_password(stored_hashed_password, entered_password):
#     # Create an Argon2 PasswordHasher instance again for verification
#     argon2_hasher = argon2.PasswordHasher()
#     try:
#         # Verify the entered password against the stored hashed password
#         argon2_hasher.verify(stored_hashed_password, entered_password)
#         return True  # Passwords match
#     except VerifyMismatchError:
#         return False  # Passwords do not match

# # Simulate storing and verifying passwords
# def main():
#     # Step 1: Hash the password (Simulating the password storage process)
#     password = "user_password"  # Password from the user during registration or first-time setup
#     stored_hashed_password ="$argon2id$v=19$m=65536,t=3,p=4$5mUlxRkyIrZQpTznU98g1w$7ooUjhFLzK7UkZzxZjtsa8cF1H0eZIvwI5pY0NSuSKI"  # Store this hash in the database
    
#     print("Stored Hashed Password:", stored_hashed_password)

#     # Step 2: Verify the password when the user tries to log in
#     entered_password = "use r_password"  # Password entered by the user during login
    
#     # Verify the entered password against the stored hashed password
#     if verify_password(stored_hashed_password, entered_password):
#         print("Correct password, proceed with login.")
#     else:
#         print("Incorrect password, access denied.")

# # Run the script
# if __name__ == "__main__":
#     main()
