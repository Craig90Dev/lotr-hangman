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

    view_instructions = input("Please enter either Y or N:\n")
    validate_data_instructions(view_instructions)

    # print(f"You have selected {view_instructions}")
    
def validate_data_instructions(y_or_n):
    """
    Inside the try, ensures the players choice is either a Y or N.
    Raises a ValueError if the input is invalid or if there is more
    than one value.
    """
    try:
        if len(y_or_n) != 1:
            raise ValueError(
                f"Only 1 letter accepted, you provided {len(y_or_n)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please enter Y or N.\n")


start_game()