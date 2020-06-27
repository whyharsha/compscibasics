# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()

def check_if_letter_exists(char, list_of_letters):
    for var in list_of_letters:
        if (char == var):
            return True
    
    return False

def is_word_guessed(secret_word, letters_guessed):
    if (len(secret_word) <= 0 or len(letters_guessed) <= 0):
        raise ValueError
    
    guessed_word = ""
    
    #case insensitive check
    lower_case_secret = secret_word.lower()
    lower_case_input = letters_guessed.lower()
    
    for char in lower_case_secret:
        if(check_if_letter_exists(char, lower_case_input)):
            guessed_word = guessed_word + char
        else:
            guessed_word = guessed_word + "_ "
    
    if(secret_word == guessed_word):
        return True
        
    return False

def get_guessed_word(secret_word, letters_guessed):
    if (len(secret_word) <= 0):
        raise ValueError
    
    guessed_word = ""
    
    #case insensitive check
    lower_case_secret = secret_word.lower()
    lower_case_letters_guessed = letters_guessed.lower()
    
    for char in lower_case_secret:
        if(check_if_letter_exists(char, lower_case_letters_guessed)):
            guessed_word = guessed_word + char
        else:
            guessed_word = guessed_word + "_ "
    
    return guessed_word

def get_available_letters(letters_guessed):
    if (len(letters_guessed) <= 0):
        return string.ascii_lowercase
    
    alphabet = string.ascii_lowercase
    
    for char in letters_guessed:
        
        index = 0
        for var in alphabet:
            if (char == var):
                alphabet = alphabet[0:index] + alphabet[(index + 1): len(alphabet)]
                break
            index = index + 1
        
    return alphabet

def hangman(secret_word):
    print("Welcome to Hangman!")
    
    number_of_guesses = 6
    letters_guessed = ""
    available_letters = get_available_letters("")
    count_invalid_input = 0
    count_already_entered = 0
    str_vowels = "aeiou"
    
    #Repeat until no guesses left
    while (number_of_guesses > 0):
        #reset lostaGuess and invalidInput for every new round of guessing
        lost_a_guess = False
        invalid_input = True
        
        #Check if the input is valid, if not ask for it again
        while (invalid_input):
            print("You've guessed " + get_guessed_word(secret_word, letters_guessed) + " so far.")
            print("You have " + str(number_of_guesses) + " guesses remaining.")
            print("Pick one of these: " + available_letters)
            user_input = input("Take a guess: ")
            #case insensitive validation of alphabets
            lower_case_input = user_input.lower()
            
            if(len(lower_case_input) == 1 and check_if_letter_exists(lower_case_input, string.ascii_lowercase)):
                invalid_input = False
                break       
            
            #checks if the user has made 3 invalid inputs in the game, and lose a guess every time after
            count_invalid_input = count_invalid_input + 1
                
            if(count_invalid_input <= 3):
                print("You can only have three total invalid inputs in the game.")
                print("You have " + str(3 - count_invalid_input) + " chance(s) remaining.")
                print("Please select only letters from the English alphabet.")
            else:
                number_of_guesses = number_of_guesses - 1
                lost_a_guess = True
                print("Invalid input! You lose a guess for incorrect inputs now on.")
                print("Please select only letters from the English alphabet.")
                break
        
        #check if the letter was already guessed and lose a guess after 3 warnings
        if(check_if_letter_exists(lower_case_input, letters_guessed)):
            count_already_entered = count_already_entered + 1
            if(count_already_entered <= 3):
                print("You already entered this letter. You can only do that thrice.")
                print("You lose guesses after that.")
                print("You have " + str(3 - count_already_entered) + " chance(s) remaining.")
            else:
                number_of_guesses = number_of_guesses - 1
                lost_a_guess = True
                print("You tried this letter before! You lose a guess for this now on.")
        
        if not(lost_a_guess):
            #If input is valid, update the list of guessed letters
            letters_guessed = letters_guessed + lower_case_input

            #If the word has been guessed, display and exit.
            if(is_word_guessed(secret_word, letters_guessed)):
                score = len(secret_word) * number_of_guesses
                print("You, winner, you! You guessed " + get_guessed_word(secret_word, letters_guessed) + " correctly!")
                print("Your score is " + str(score) + "!")
                print("Play again!")
                break
            else:
                #If the input is valid and in the secret word, do not reduce the number of guesses.
                if(check_if_letter_exists(lower_case_input, secret_word)):
                    print("Making progress.")
                else:
                    #check for vowels and handle the loss of guesses correctly
                    if(check_if_letter_exists(lower_case_input, str_vowels)):
                        number_of_guesses = number_of_guesses - 2
                        print("You guessed an incorrect vowel. You lose 2 guesses.")
                    else:
                        number_of_guesses = number_of_guesses - 1
                        print("You guessed wrong. You lose a guess.")

                availableLetters = get_available_letters(letters_guessed)
    
    #User loses, if the number of guesses is 0 and the word has not been guessed.
    if(number_of_guesses == 0 and not is_word_guessed(secret_word, letters_guessed)):
        print("Gah! You're out of guesses and luck! The word was " + secret_word + "!")
        print("Try your luck again. Start over.")

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------

def match_with_gaps(my_word, other_word):
    if (len(my_word) < 0 or len(other_word) <= 0):
        raise ValueError
    
    lower_case_my_word = my_word.lower()
    lower_case_other_word = other_word.lower()

    mod_my_word = ""

    #eliminate spaces
    for letter in lower_case_my_word:
        if not (letter == " "):
          mod_my_word = mod_my_word + letter
    
    #check length
    if not (len(mod_my_word) == len(lower_case_other_word)):
        return False
    
    #since length is equal, match characters by index, unless my word has an underscore
    for index in range(len(lower_case_other_word)):
        if not (mod_my_word[index] == "_"):
            if not (mod_my_word[index] == lower_case_other_word[index]):
                return False

    return True        

def show_possible_matches(my_word):
    if(len(wordlist) == 0):
      print("No words in the list")

    for word in wordlist:
      if(match_with_gaps(my_word, word)):
        print(str(word))


def hangman_with_hints(secret_word):
    print("Welcome to Hangman (type * (a single asterisk) to get hints)!")
    
    number_of_guesses = 6
    letters_guessed = ""
    count_invalid_input = 0
    count_already_entered = 0
    str_vowels = "aeiou"
    
    #Repeat until no guesses left
    while (number_of_guesses > 0):
        #reset lostaGuess and invalidInput for every new round of guessing
        lost_a_guess = False
        invalid_input = True
        asked_for_hint = False
        print("The secret word has " + str(len(secret_word)) + " letters.")
        
        #Check if the input is valid, if not ask for it again
        while (invalid_input):
            print("You've guessed " + get_guessed_word(secret_word, letters_guessed) + " so far.")
            print("You have " + str(number_of_guesses) + " guesses remaining.")
            print("Pick one of these: " + get_available_letters(letters_guessed))
            user_input = input("Take a guess: ")
            #case insensitive validation of alphabets
            lower_case_input = user_input.lower()

            print("Lower case input is " + lower_case_input)
            
            if(len(lower_case_input) == 1 and check_if_letter_exists(lower_case_input, string.ascii_lowercase)):
                invalid_input = False
                break       
            
            #here's where we give hints
            if(len(lower_case_input) == 1 and lower_case_input == "*"):
              print("-------------------------------------------------------------")
              print("Possible matched words are:")
              temp_guessed_word = get_guessed_word(secret_word, letters_guessed)
              show_possible_matches(temp_guessed_word)
              print("-------------------------------------------------------------")
              asked_for_hint = True
              break

            #checks if the user has made 3 invalid inputs in the game, and lose a guess every time after
            count_invalid_input = count_invalid_input + 1
                
            if(count_invalid_input <= 3):
                print("You can only have three total invalid inputs in the game.")
                print("You have " + str(3 - count_invalid_input) + " chance(s) remaining.")
                print("Please select only letters from the English alphabet.")
            else:
                number_of_guesses = number_of_guesses - 1
                lost_a_guess = True
                print("Invalid input! You lose a guess for incorrect inputs now on.")
                print("Please select only letters from the English alphabet.")
                break
        
        #check if the letter was already guessed and lose a guess after 3 warnings
        if(check_if_letter_exists(lower_case_input, letters_guessed)):
            count_already_entered = count_already_entered + 1
            if(count_already_entered <= 3):
                print("You already entered this letter. You can only do that thrice.")
                print("You lose guesses after that.")
                print("You have " + str(3 - count_already_entered) + " chance(s) remaining.")
            else:
                number_of_guesses = number_of_guesses - 1
                lost_a_guess = True
                print("You tried this letter before! You lose a guess for this now on.")
        
        if not(lost_a_guess or asked_for_hint):
            #If input is valid, update the list of guessed letters
            letters_guessed = letters_guessed + lower_case_input

            #If the word has been guessed, display and exit.
            if(is_word_guessed(secret_word, letters_guessed)):
                score = len(secret_word) * number_of_guesses
                print("You, winner, you! You guessed " + get_guessed_word(secret_word, letters_guessed) + " correctly!")
                print("Your score is " + str(score) + "!")
                print("Play again!")
                break
            else:
                #If the input is valid and in the secret word, do not reduce the number of guesses.
                if(check_if_letter_exists(lower_case_input, secret_word)):
                    print("Making progress.")
                else:
                    #check for vowels and handle the loss of guesses correctly
                    if(check_if_letter_exists(lower_case_input, str_vowels)):
                        number_of_guesses = number_of_guesses - 2
                        print("You guessed an incorrect vowel. You lose 2 guesses.")
                    else:
                        number_of_guesses = number_of_guesses - 1
                        print("You guessed wrong. You lose a guess.")
    
    #User loses, if the number of guesses is 0 and the word has not been guessed.
    if(number_of_guesses == 0 and not is_word_guessed(secret_word, letters_guessed)):
        print("Gah! You're out of guesses and luck! The word was " + secret_word + "!")
        print("Try your luck again. Start over.")



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
