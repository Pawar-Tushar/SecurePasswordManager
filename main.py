from getpass import getpass
from rich import print as printc
import Utils.Add
import Utils.Get
import Utils.Generate
import Utils.Password_strength
from Utils.dbconfig import Dbconfig
from argon2 import PasswordHasher
import pyperclip

def inputAndValidateMasterPassword():
    mp = getpass("MASTER PASSWORD: ")

    db = Dbconfig()
    cursor = db.cursor()
    query = "SELECT * FROM password_manager.app_secrets"
    cursor.execute(query)
    result = cursor.fetchall()[0]
    ph = PasswordHasher()
    try:
        ph.verify(result[0], mp)  
    except Exception as e:
        printc("[red][!] Incorrect master password. Please try again.[/red]")
        return None
    
    printc("[green][+] Master password validated successfully![/green]")
    return [mp, result[1]]


def main():
    printc("[blue][+] Welcome to the Password Manager Application![/blue]")
    
    res = inputAndValidateMasterPassword()
    if not res:
        return 

    # Main menu
    while True:
        printc("[yellow][+] Please choose an option from the menu:[/yellow]")
        printc("1. Add a new entry")
        printc("2. Retrieve an entry")
        printc("3. Generate a new password")
        printc("4. Check Password Strength ")
        printc("5. Exit")
        
        choice = input("Enter your choice (1/2/3/4/5): ").strip()
        
        if choice == "1":
            add_entry(res)
        elif choice == "2":
            get_entry(res)
        elif choice == "3":
            generate_password()
        elif choice == '4':
            print("Password Strength Checker")
            password = input("Enter a password to check its strength: ")
    
            strength, feedback = Utils.Password_strength.check_password_strength(password)
    
            printc(f"[red][!] \nPassword Strength: {strength}[/red]")
            print(feedback)
        elif choice == "5":
            printc("[green][+] Exiting the application. Goodbye![/green]")
            break
        else:
            printc("[red][!] Invalid choice. Please try again.[/red]")

def add_entry(res):
    printc("[blue][+] Adding a new entry[/blue]")

    sitename = input("Enter the site name: ").strip()
    siteurl = input("Enter the site URL: ").strip()
    email = input("Enter the email (leave blank if not applicable): ").strip()
    username = input("Enter the username: ").strip()

    Utils.Add.addEntry(res[0], res[1], sitename, siteurl, email, username)
    printc("[green][+] Entry added successfully![/green]")

def get_entry(res):
    printc("[blue][+] Retrieving an entry[/blue]")
    
    sitename = input("Enter the site name (leave blank to search all): ").strip()
    siteurl = input("Enter the site URL (leave blank to search all): ").strip()
    email = input("Enter the email (leave blank to search all): ").strip()
    username = input("Enter the username (leave blank to search all): ").strip()

    search = {}
    if sitename:
        search["sitename"] = sitename
    if siteurl:
        search["siteurl"] = siteurl
    if email:
        search["email"] = email
    if username:
        search["username"] = username

    Utils.Get.GetEntries(res[0], res[1], search, decryptPassword=True)
    
def generate_password():
    length = input("Enter the desired length for the new password: ").strip()
    
    if not length.isdigit() or int(length) < 8:
        printc("[red][!] Please enter a valid length (at least 8 characters).[/red]")
        return
    
    password = Utils.Generate.generatePassword(int(length))
    pyperclip.copy(password) 
    
    printc(f"[green][+] Generated password: {password}[/green]")
    printc("[green][+] Password copied to clipboard![/green]")


if __name__ == "__main__":
    main()
