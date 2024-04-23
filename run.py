import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('lotr_hangman')

def start_game():
    """
    Asks player if they want to view instructions
    """
    print("Welcome to LOTR Hangman!")
    print("Do you want to view the instructions?\n")

    decision = input("Please enter either Y or N:\n")
    print(f"You have selected {decision}")
    

start_game()