from Utils.dbconfig import Dbconfig  
import Utils.AES

from getpass import getpass
from Crypto.Protocol.KDF import scrypt
from rich import print as printc

def CryptoMasterKey(mp, salt, key_length=32, N=2**14, r=8, p=1):
    password = mp.encode() 
    salt = salt.encode() 
    key = scrypt(password, salt, key_length, N, r, p)
    return key


def checkEntry(sitename, siteurl, email, username):
	db = Dbconfig()
	cursor = db.cursor()
	query = f"SELECT * FROM password_manager.password_entries WHERE sitename = '{sitename}' AND siteurl = '{siteurl}' AND email = '{email}' AND username = '{username}'"
	cursor.execute(query)
	results = cursor.fetchall()

	if len(results)!=0:
		return True
	return False

def addEntry(mp, salt, sitename, siteurl, email, username):
	if checkEntry(sitename, siteurl, email, username):
		printc("[yellow][-][/yellow] Entry with these details already exists")
		return
	

	# print(mp)
	password = getpass("Password: ")
	mk = CryptoMasterKey(mp,salt)
	# print(mk)

	encrypted = Utils.AES.encrypt(key=mk, source=password, keyType="bytes")

	db = Dbconfig()
	cursor = db.cursor()
	query = "INSERT INTO password_manager.password_entries (sitename, siteurl, email, username, password) values (%s, %s, %s, %s, %s)"
	val = (sitename,siteurl,email,username,encrypted)
	cursor.execute(query, val)
	db.commit()

	printc("[green][+][/green] Added entry ")




# addEntry("Tushar","aaaaasssss","face","book.com","e@gamil.com","sd")












# # Example usage
# mp = "my_secure_taster_password"  # Master password
# salt = "unique_salt_value"  # Fixed salt value (must be stored securely)

# # Generate the AES key using scrypt
# aes_key = CryptoMasterKey(mp, salt)

# # The AES key will be a 256-bit key suitable for AES-256 encryption
# print("Generated AES key:")
# print(aes_key.hex())  # Output as hex to view the actual bytes
