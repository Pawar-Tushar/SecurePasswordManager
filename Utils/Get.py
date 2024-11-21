from Utils.dbconfig import Dbconfig
import Utils.AES
import pyperclip
from Crypto.Protocol.KDF import scrypt

from rich import print as printc
from rich.console import Console
from rich.table import Table


def CryptoMasterKey(mp, salt, key_length=32, N=2**14, r=8, p=1):
    password = mp.encode() 
    salt = salt.encode()  
    key = scrypt(password, salt, key_length, N, r, p)
    return key


def GetEntries(mp, salt, search, decryptPassword = False):
	db = Dbconfig()
	cursor = db.cursor()

	query = ""
	if len(search)==0:
		query = "SELECT * FROM password_manager.password_entries"
	else:
		query = "SELECT * FROM password_manager.password_entries WHERE "
		for i in search:
			query+=f"{i} = '{search[i]}' AND "
		query = query[:-5]

	cursor.execute(query)
	results = cursor.fetchall()

	if len(results) == 0:
		printc("[yellow][-][/yellow] No results for the search")
		return

	if (decryptPassword and len(results)>1) or (not decryptPassword):
		if decryptPassword:
			printc("[yellow][-][/yellow] More than one result found for the search, therefore not extracting the password. Be more specific.")
		table = Table(title="Results")
		table.add_column("Site Name")
		table.add_column("URL",)
		table.add_column("Email")
		table.add_column("Username")
		table.add_column("Password")

		for i in results:
			table.add_row(i[0], i[1], i[2], i[3], "{hidden}")
		console = Console()
		console.print(table)
		return 

	if decryptPassword and len(results)==1:
		mk = CryptoMasterKey(mp,salt)

		decrypted = Utils.AES.decrypt(key=mk,source=results[0][4],keyType="bytes")

		printc("[green][+][/green] Password copied to clipboard")
		pyperclip.copy(decrypted.decode())

	db.close()


