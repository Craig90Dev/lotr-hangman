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

    #Loops through validation function and repeats user input until data received returns True
    while True:
        view_instructions = input("Please enter either Y or N:\n")
        #Breaks from while loop 
        if validate_data_instructions(view_instructions):
            break

    main_game()

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

def hide_letters(word):
    """
    Replaces characters from word with underscores
    """
    hidden_word = ""
    for i in word:
        if i.isalpha():
            hidden_word += "_ "
        else:
            hidden_word += i
    return hidden_word    

def grab_word():
    """
    Grabs random word from Google worksheet
    """
    words = SHEET.worksheet("chars").get_all_values()

    import secrets
    random_word = (secrets.choice(words))

    chosen_word = str(random_word[0])

    return chosen_word
    
def main_game():
    """
    Runs a while loop to iterate through each of the players guesses, updating guessed_letters
    variable and updating the hidden word as necessary until the player either guesses the
    correct word or hits the limit of max_wrong_attempts. While loop breaks when either the player
    has guessed the word or if all attempts are used up. (Will be updated to play again option)
    """
    word = grab_word()
    hidden_word = hide_letters(word)
    max_wrong_attempts = 6
    wrong_attempts = 0
    guessed_letters = []

    while True:

        guessed_letters_shown = " ".join(guessed_letters)
        print_hangman(wrong_attempts)
        print(f"Guessed letters: {guessed_letters_shown}")
        print(hidden_word)

        guess = input("Guess a letter or the entire word: ").upper()
        #Player wins if guess matches entire word
        if guess == word:
            print("Congratulations! You've guessed the word correctly:", word)
            break
        #Checks if the players guessed letter is already in the guessed letters variable
        elif guess in guessed_letters:
            print("You've already guessed that letter.")
            continue
        #Checks to see if the players guess is a single letter and appends it to the guessed_letters variable
        elif len(guess) == 1 and guess.isalpha():
            guessed_letters.append(guess)
            #if guessed character is in the hidden word, updates the hidden word
            if guess in word:
                hidden_word = update_hidden_word(word, hidden_word, guess)
                #checks to see if the updated hidden word is equal to the word
                if hidden_word.replace(" ", "") == word:
                    print("Congratulations! You've guessed the word correctly:", word)
                    break
            #If none of the above conditions are met adds +1 to the wrong answers variable
            else:
                wrong_attempts += 1
                #If the wrong attempt is the last allowed attempt then prints final hangman diagram
                #and gives the final answer to the player
                if wrong_attempts >= max_wrong_attempts:
                    print("\n   ------|")
                    print("     |   O")
                    print("     |  /|\\")
                    print("     |  / \\")
                    print("   ===== ")
                    print("You've used up all your attempts. The word was:", word)
                    break
        #If the player guesses something that is not a single letter prints an "invalid" statement          
        else:
            print("Invalid input. Please enter a single letter or the entire word.")

def update_hidden_word(word, hidden_word, guess):
    """
    Updates the hidden word based on the players guessed letter
    """
    updated_hidden_word = ""
    for i in range(len(word)):
        if word[i] == guess:
            updated_hidden_word += guess + " "
        else:
            updated_hidden_word += hidden_word[2*i] + " "
    return updated_hidden_word

def print_hangman(wrong):
    """
    Prints the hangman diagram depending on how many wrong guesses the player has made
    """
    if (wrong == 0):
        print("\n   ------|")
        print("     | ")
        print("     | ")
        print("     | ")
        print("   ===== ")

    elif (wrong == 1):
        print("\n   ------|")
        print("     |   O")
        print("     | ")
        print("     | ")
        print("   ===== ")

    elif (wrong == 2):
        print("\n   ------|")
        print("     |   O")
        print("     |   |")
        print("     | ")
        print("   ===== ")

    elif (wrong == 3):
        print("\n   ------|")
        print("     |   O")
        print("     |  /|")
        print("     | ")
        print("   ===== ")


    elif (wrong == 4):
        print("\n   ------|")
        print("     |   O")
        print("     |  /|\\")
        print("     | ")
        print("   ===== ")

    elif (wrong == 5):
        print("\n   ------|")
        print("     |   O")
        print("     |  /|\\")
        print("     |  /")
        print("   ===== ")

start_game()