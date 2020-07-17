# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    if len(sequence) == 0:
        return []
    elif len(sequence) == 1:
        return [sequence]
    else:
        list_of_perms = []

        for index in range(len(sequence)):
             for element in get_permutations((sequence[:index] + sequence[index + 1:])):
                 list_of_perms.append(sequence[index] + element)

    return list_of_perms

def get_permutations_v2(sequence, level, result):
    if level == len(sequence):
        print(result)
        return ""

    freq_dict = create_freq_dict(sequence)
    
    for letter in freq_dict:
        mod_seq = build_modified_sequence(sequence, letter)
        result += letter
        result += get_permutations_v2(mod_seq, (level + 1), result)

    return result

def create_freq_dict(sequence):
    freq_dict = {}

    if sequence is not None:
        for letter in sequence:
            if letter in freq_dict:
                freq_dict[letter] += 1
            else:
                freq_dict[letter] = 1
    
    return freq_dict

def build_modified_sequence(sequence, letter):

    mod_sequence = ""
    count_letter = 0

    for char in sequence: #abcd #a
        if char == letter:
            if count_letter < 1:
                continue
            else:
                mod_sequence += char
            count_letter += 1
        else:
            mod_sequence += char
    
    return mod_sequence

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    pass #delete this line and replace with your code here

