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

start_game()

def start_game():
    """
    Asks player if they want to view instructions
    """
    print("Welcome to LOTR Hangman!")
    print("Do you want to view the instructions?\n")

    #Loops through validation function and repeats user input until data received returns True
    while True:
        
        view_instructions = input("Please enter either Y or N:\n")
        #Breaks from while loop 
        if validate_data_instructions(view_instructions):
            break
    
def validate_data_instructions(y_or_n):
    """
    Inside the try, ensures the players choice is either a Y or N.
    Raises a ValueError if the input is invalid or if there is more
    than one value.
    """
    #Checks if the player input is only 1 character long. If not, raises value error
    #and loops back to while statement.
    try:
        if len(y_or_n) != 1:
            raise ValueError(
                f"Only 1 letter accepted, you entered {len(y_or_n)}"
            )
    except ValueError as e:
        print(f"Invalid answer: {e}.\n")
        return False
    
    #Returns True if player answers Y or N. Shows instructions if player selects Y, 
    #starts grab_word function if selects N. Returns False and loops back to while
    #statement if player answers anything other than Y or N.
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
    """
    Grabs random word from Google worksheet
    """

def print_hangman(wrong):
    if (wrong == 0):
        print("\n ------|")
        print("     | ")
        print("     | ")
        print("     | ")
        print("   ===== ")

    elif (wrong == 1):
        print("\n ------|")
        print("     |   O")
        print("     | ")
        print("     | ")
        print("   ===== ")

    elif (wrong == 2):
        print("\n ------|")
        print("     |   O")
        print("     |   |")
        print("     | ")
        print("   ===== ")

    elif (wrong == 3):
        print("\n ------|")
        print("     |   O")
        print("     |  /|")
        print("     | ")
        print("   ===== ")


    elif (wrong == 4):
        print("\n ------|")
        print("     |   O")
        print("     |  /|\\")
        print("     | ")
        print("   ===== ")

    elif (wrong == 5):
        print("\n ------|")
        print("     |   O")
        print("     |  /|\\")
        print("     |  /")
        print("   ===== ")

    elif (wrong == 6):
        print("\n ------|")
        print("     |   O")
        print("     |  /|\\")
        print("     |  /\\")
        print("   ===== ")