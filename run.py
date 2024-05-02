import gspread
import secrets
import os
import sys
import time
from google.oauth2.service_account import Credentials
from colorama import Fore

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('lotr_hangman')

def main():
    """
    Main program function
    """
    while True:

        global type_delay, welcome_sentences, instruction_sentences, used_words

        type_delay = 0.01
        used_words = []

        welcome_sentences = [
            "Welcome to LOTR Hangman!\n",
            "Do you want to view the instructions?\n"
        ]

        instruction_sentences = [
            "Guess each letter of the hidden word.\n",
            "The words are names of characters from Tolkien's Lord Of The Rings series.\n",
            "If you guess correctly the letters will be shown in their appropriate place.\n",
            "If you guess incorrectly a body part will be added to the Hangman image.\n",
            "If you guess the whole word you win!\n",
            "If all body parts on the Hangman diagram are shown you lose.\n",
            "You can try and guess the word at any time during the game.\n",
            "Good Luck!\n"
        ]
        start_game()

def start_game():
    """
    Starts the game if the player chooses not to view instructions or has already viewed them.
    """
    instructions_viewed = False
    while not instructions_viewed:
        typewriter_effect_welcome(welcome_sentences, type_delay)
        
        # Loops through validation function and repeats user input until data received returns True
        while True:
            view_instructions = input("Please enter either Y or N: \n")
            clear_screen()
            instructions_viewed = validate_data_instructions(view_instructions)
            if instructions_viewed:
                break

    while True:
        if main_game():
            continue
        else:
            return False

def validate_data_instructions(y_or_n):
    """
    Inside the try, ensures the player's choice is either Y or N.
    Raises a ValueError if the input is invalid or if there is more
    than one value.
    """
    # Checks if the player input is only 1 character long. If not, raises value error
    # and loops back to while statement.
    try:
        if len(y_or_n) != 1:
            raise ValueError(
                f"Only 1 letter accepted, you entered {len(y_or_n)}"
            )
    except ValueError as e:
        print(f"Invalid answer: {e}.\n")
        return False
    # Returns True if player answers Y or N. Shows instructions if player selects Y, 
    # starts grab_word function if selects N. Returns False and loops back to while
    # statement if player answers anything other than Y or N.
    if y_or_n.upper() == "Y":
        typewriter_effect_instructions(instruction_sentences, type_delay)
        return True
    elif y_or_n.upper() == "N":
        return True 
    else:
        print(f"You entered {y_or_n.upper()}\n")
        return False
    
def typewriter_effect_instructions(instruction_sentences, type_delay):
    """
    Add typewriter effect to print instuctions
    """
    for sentence in instruction_sentences:
        for char in sentence:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(type_delay)
    
    time.sleep(1)

def typewriter_effect_welcome(welcome_sentances, type_delay):
    """
    Add typewriter effect to print welcome message
    """
    for sentence in welcome_sentances:
        for char in sentence:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(type_delay)
    
    time.sleep(1)

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
    Grabs random word from Google worksheet, converts to string and returns as chosen word
    """
    words = SHEET.worksheet("chars").get_all_values()
    #If the length of the variables used_words and words are the same, word returns as None, ending
    #from main_game function if word is None returning false and this message will print to player
    if len(used_words) == len(words):
        print("All words have been used.")
        return None

    while True:
        random_word = (secrets.choice(words))
        chosen_word = str(random_word[0])
        if chosen_word not in used_words:
            used_words.append(chosen_word)
            return chosen_word
    
def main_game():
    """
    Runs a while loop to iterate through each of the player's guesses, updating guessed_letters
    variable and updating the hidden word as necessary until the player either guesses the
    correct word or hits the limit of max_wrong_attempts. While loop calls play_again function when either the player
    has guessed the word or if all attempts are used up.
    """
    while True:
        word = grab_word()
        #If all words in spreadsheet have been used, return false to end game
        if word is None:
            return False
        hidden_word = hide_letters(word)
        max_wrong_attempts = 6
        wrong_attempts = 0
        guessed_letters = []

        while True:
            guessed_letters_shown = " ".join(guessed_letters)
            print_hangman(wrong_attempts)
            print(f"{Fore.BLUE}Guessed letters: {guessed_letters_shown}{Fore.WHITE}")
            print(hidden_word)
            guess = input("Guess a letter or the entire word: \n").upper()

            # Player wins if guess matches entire word
            if len(guess) == len(word) and guess != word:
                clear_screen()
                print(f"{Fore.RED}Sorry, that is not the correct word. {Fore.WHITE}")
                wrong_attempts += 1
            elif guess == word:
                clear_screen()
                print(f"{Fore.GREEN}Congratulations! You've guessed the word correctly: {Fore.WHITE}", word)
                return play_again()
            # Checks if the players guessed letter is already in the guessed letters variable
            elif guess in guessed_letters:
                clear_screen()
                print("You've already guessed that letter.")
                continue
            # Checks to see if the players guess is a single letter and appends it to the guessed_letters variable
            elif len(guess) == 1 and guess.isalpha():
                clear_screen()
                guessed_letters.append(guess)
                # if guessed character is in the hidden word, updates the hidden word
                if guess in word:
                    clear_screen()
                    print(f"{Fore.GREEN}Good job! You found a letter! {Fore.WHITE}")
                    hidden_word = update_hidden_word(word, hidden_word, guess)
                    # checks to see if the updated hidden word is equal to the word
                    if hidden_word.replace(" ", "") == word:
                        clear_screen()
                        print(f"{Fore.GREEN}Congratulations! You've guessed the word correctly: {Fore.WHITE}", word)
                        return play_again()
                # If none of the above conditions are met adds +1 to the wrong answers variable
                else:
                    clear_screen()
                    print(f"{Fore.RED}Sorry, that letter is not in the word! {Fore.WHITE}")
                    wrong_attempts += 1
                    # If the wrong attempt is the last allowed attempt then prints final hangman diagram
                    # and gives the final answer to the player
                    if wrong_attempts >= max_wrong_attempts:
                        clear_screen()
                    
                        print("\n   ------|")
                        print("     |   O")
                        print("     |  /|\\")
                        print("     |  / \\")
                        print("   ===== ")
                        print(f"{Fore.RED}Sorry, you've used up all your attempts. The word was: {Fore.WHITE}", word)

                        return play_again()
            # If the player guesses something that is not a single letter prints an "invalid" statement
            else:
                clear_screen()
                print("Invalid input. Please enter a single letter or the entire word.")

def update_hidden_word(word, hidden_word, guess):
    """
    Updates the hidden word based on the players guessed letter and adds a space to separate
    """
    updated_hidden_word = ""
    for i in range(len(word)):
        #if guessed letter matches a character in the hidden word, reveals the character
        if word[i] == guess:
            updated_hidden_word += guess + " "
        #If guessed letter does not match, keeps hidden letter in position
        else:
            updated_hidden_word += hidden_word[2*i] + " "
    return updated_hidden_word

def play_again():
    """
    Asks the player if they want to play again and returns True if they do, False otherwise.
    """
    while True:
        print("Do you want to play again?")
        play_again_input = input("Please enter either Y or N: \n").upper()
        if play_again_input == 'Y':
            clear_screen()
            return True
        elif play_again_input == 'N':
            clear_screen()
            return False
        else:
            clear_screen()
            print("Invalid input. Please enter either Y or N.")


def clear_screen():
    """
    Function clears the terminal (screen).
    """
    os.system('clear')
    return None

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

if __name__ == '__main__':
    main()