import mysql.connector
from rich import print as printc
from rich.console import Console
console = Console()
// configure your databse here
def Dbconfig():
  try:
    db = mysql.connector.connect(
      host ="localhost",
      user ="yourusername",
      passwd ="yourpassword"
    )
  except Exception as e:
    print("[red][!] An error occurred while trying to connect to the database[/red]")
    console.print_exception(show_locals=True)

  return db
