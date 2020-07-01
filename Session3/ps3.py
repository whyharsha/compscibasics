# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    if(n < 0):
        raise ValueError

    lower_case_word = word.lower()

    score_letter_points = 0

    for letter in lower_case_word:
        score_letter_points = score_letter_points + SCRABBLE_LETTER_VALUES[letter]
    
    score_word_len = max((len(lower_case_word) * 7) - (3 * (n - len(lower_case_word))), 0)

    return max(score_letter_points, score_word_len)

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    if(len(word) == 0 or len(hand) == 0):
        return hand
    
    letter_freq = get_frequency_dict(word)
    updated_hand = {}

    for letter in letter_freq:
        count_letter_remaining = hand.get(letter, 0) - letter_freq[letter]
        if(count_letter_remaining > 0):
            updated_hand[letter] = count_letter_remaining
    
    return updated_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    lower_case_word = word.lower()

    #Take each word in the list
    for var in word_list:
        is_word_in_list = False
        is_not_same_word = False #could probably use one less bool here, will revisit
        are_letters_in_hand = True

        #check the length of our word and the word from the list is equal
        if (len(lower_case_word) == len(var)):
            #match each character
            for index in range(len(var)):
                #if a character does not match, break the match loop
                if not (var[index] == word[index]):
                    is_not_same_word = True
                    break
            
            if not (is_not_same_word):
                is_word_in_list = True
        
        #in parallel, for each word, check if the hand has the required letters
        letter_freq = get_frequency_dict(var)

        for letter in letter_freq:
            count_letter_remaining = hand.get(letter, 0) - letter_freq[letter]
            #if the available count for any letter is less than zero, the word is invalid
            if(count_letter_remaining < 0):
                are_letters_in_hand = False
        
        if(is_word_in_list and are_letters_in_hand):
            return True

    return False

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    hand_len = 0

    for key in hand:
        hand_len = hand_len + hand[key]
    
    return hand_len

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    hand_score = 0
    handlen = calculate_handlen(hand)

    while handlen > 0:
        print("---------------------------------------------------------------------")
        print("Your hand is as below:")
        display_hand(hand)
        print("---------------------------------------------------------------------")

        user_input = input("Enter a word using the letters in the hand: ")

        if not (user_input == "!!"):
            lower_case_user_input = user_input.lower()

            if(is_valid_word(lower_case_user_input)):
                score = get_word_score(lower_case_user_input, handlen)
                print("Well played! You scored " + str(score) + " points")
                hand_score = hand_score + score
                print("Your total score is now: " + str(hand_score))
            else:
                print("Sorry! That was an invalid word.")
                
            update_hand(hand, lower_case_user_input)
        else:
            print("Thank you for playing. Your total score is:" + str(hand_score))
    else:
        print("You ran out of letters! Thank you for playing. Your total score is:" + str(hand_score))
        
    return hand_score



#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    #if letter to be replaced is not in the hand, return the hand
    if letter not in hand:
        return hand
    
    #create a substitute hand since we don't want to mutate hand
    substitute_hand = {}
    substitute_letter = random.choice(string.ascii_lowercase)

    #ensure substitute letter is not the same as the chosen letter
    while substitute_letter == letter:
        substitute_letter = random.choice(string.ascii_lowercase)
    
    for character in hand:
        #ensure the replacement character has the same count as the letter replaced
        if letter == character:
            substitute_hand[substitute_letter] = hand[character]
        else:
            substitute_hand[character] = hand[character]

    return substitute_hand
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    
    is_invalid_input = True
    number_of_hands = 0

    while is_invalid_input:

        user_input = input("How many hands due to wish to play?")

        if user_input.isdigit() and int(user_input) > 0 and int(user_input) < 16:
            number_of_hands = int(user_input)
            is_invalid_input = False
        else:
            print("Invalid input. Please enter only numbers over 0 upto 15.")
    
    total_score = 0
    played_a_sub = False
    replayed_hand = False

    while number_of_hands > 0:

        print("Let's play!")

        is_invalid_input = True
        lower_case_input = ""

        hand = deal_hand(15)
        display_hand(hand)

        #Substitution section
        if not played_a_sub:
            while is_invalid_input:
                user_input = input("Would you like to substitute a letter in your hand? Enter yes or no.")

                lower_case_input = user_input.lower()

                if lower_case_input == 'yes':
                    is_valid_sub_input = False

                    while not is_valid_sub_input:
                        sub_input = input("Pick a letter in your hand to substitute: ")

                        lower_case_sub = sub_input.lower()

                        if lower_case_sub in string.ascii_lowercase and len(lower_case_sub) == 1:
                            substitute_hand(hand, lower_case_sub)
                            is_valid_sub_input = True
                        else:
                            print("Invalid input. Please enter a single character from the English alphabet only.")
                    
                    is_invalid_input = False
                    played_a_sub = True
                elif lower_case_input == 'no':
                    is_invalid_input = False
                else:
                    print("Invalid input. Please enter only yes or no.")
        
        temp_total_score = play_hand(hand)

        #Replay section
        if not replayed_hand:
            is_invalid_replay_input = True

            while is_invalid_replay_input:
                replay_input = input("Would you like to replay the hand? Enter yes or no.")

                lower_case_replay = replay_input.lower()

                if not lower_case_replay == "no" or lower_case_replay == "yes":
                    print("Invalid input. Please enter only yes or no.")

                elif lower_case_replay == "yes":
                    replay_score = play_hand(hand)
                    total_score += max(temp_total_score, replay_score)
                    replayed_hand = True
                    is_invalid_replay_input = False
                
                elif lower_case_replay == "no":
                    total_score += temp_total_score
                    is_invalid_replay_input = False

        print("Your total score now stands at: " + str(total_score))
        
        #end of a hand
        number_of_hands -= 1

    print("Thank you for playing! Your final score is: " + str(total_score))
    


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
