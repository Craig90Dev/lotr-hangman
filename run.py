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
    while True:
        
        view_instructions = input("Please enter either Y or N:\n")

        if validate_data_instructions(view_instructions):
            print("data valid")
            break
    
def validate_data_instructions(y_or_n):
    """
    Inside the try, ensures the players choice is either a Y or N.
    Raises a ValueError if the input is invalid or if there is more
    than one value.
    """
    try:
        if len(y_or_n) != 1:
            raise ValueError(
                f"Only 1 letter accepted, you entered {len(y_or_n)}"
            )
    except ValueError as e:
        print(f"Invalid answer: {e}.\n")
        return False
    
    if y_or_n.upper() == "Y":
        print("Guess each letter of the hidden word.")
        print("The word is the name of a character from J.R.R Tolkien's Lord Of The Rings series.")
        print("If you guess correctly the letters will be shown in their appropriate place.")
        print("If you guess incorrectly a body part will be added to the Hangman image.")
        print("If you guess the whole word you win!")
        print("If all body parts on the Hangman diagram are shown you lose.")
        print("You can try and guess the word at any time during the game.\n")
        print("Good Luck!\n")
        grab_word()
    elif y_or_n.upper() == "N":
        grab_word()
    else:
        print(f"You entered {y_or_n.upper()}\n")
        return False
    return True

def grab_word():
    print("WORD")
    
start_game()