# Jonathan Grant
# main.py
# Lexical Analyzer
# 10 November 2017
#
# This program reads lines from an input file (input.txt)
# and uses an FSA with a transition table (config.py) to accept or reject
# each line of input.  If the line is accepted, the program
# will also print additional information about the string.
#
# This program also imports a regular language from regularlanguage.py
# and creates an instance of the class described in that file.

import regularlanguage
my_regular_expression = regularlanguage.Initialize_Class()

def Get_Config_Info():
    """ Gets info about the language rules from config.txt.

        config.txt has a particular format:
        
            The first section of lines that lead up to a blank line
            describe possible inputs, with each row corresponding to
            a different 'type' of input, or column in the transition table.

            The second section desrcibes the transition table, it says which
            state to go to next based off of which state it is currently in,
            and which symbol the program just read in.

            The third section desrcibes accepting states. Once the final
            character of a string has been read, then if the transition table
            is pointing to an accepting state, the string is accepted.

            The fourth and final section describes rejection states, which
            immediately allow us to stop looking at the string because we know
            it is already not a valid string.
    """
    # transition_table     - contains state transition
    # possible_inputs      - each row of this 2D array describes a column in the
    #                        state transition table.
    # accepting_states     - array of states that accept the string as valid.
    # rejecting_states     - array of states that reject the string as invalid.
    #                        (There is currently only one rejecting state)
    # config_file          - the file that contains information for the transition table
    # place_in_config_file - describes which section we are reading from.
    #                        i.e. the 4 sections described above.

    transition_table = []
    possible_inputs = []

    config_file = open("<filename>", "r")

    # Each line in our config file contains a row from the
    # transition table, and each row represents a state
    # in the transition table.  This table is implemented as
    # a 2D array.
    # Note that the 2nd to last line contains accepting states,
    # and the last line is the rejecting state.

    place_in_config_file = 0
    for line in config_file:

        if line == '\n':

            # Newline character separates the sections of the
            # config file.
            place_in_config_file += 1

        elif place_in_config_file == 0:

            possible_inputs.append(line.rstrip().split(' '))

        elif place_in_config_file == 1:

            transition_table.append(line.rstrip().split(' '))

        elif place_in_config_file == 2:

            accepting_states = line.rstrip().split(' ')

        else:

            rejecting_states = line.rstrip().split(' ')

    config_file.close()

    return (possible_inputs, transition_table, accepting_states, rejecting_states)


def Characterize_Input_Symbol(a, list_of_possible_inputs):
    """ Determines the type of character a (digit, letter, etc.)

        a - The character of the string being looked at
        list_of_possible_inputs - Describes where the variable 'a'
                                  might be found. 
    """
    # counter - Describes which column of the transition table we are
    #           looking into to see if the input symbol being read belongs
    #           to that column.

    counter = 0
    found = False
    while (not found) and (counter < len(list_of_possible_inputs)):

        if a in list_of_possible_inputs[counter]:

            found = True

        else:

            counter += 1

    # Note that if we never found the input symbol to belong in
    # any certain row, then it is not an acceptable symbol.
    return counter


def Apply_Transition_Table(transition_table, current_state, type_of_character):
    """ Decides which state to go to based off of the current state and input symbol. """

    next_state = transition_table[int(current_state)][type_of_character]

    return next_state

def Print_Validity(valid):
    """ Prints if a string is a valid sentence in the language.
        input_string - The string that is being looked at, either valid or invalid
        valid - boolean describing if the input_string is a sentence in the language
    """

    if valid:
    
        print(" is Valid")
        my_regular_expression.Print_Attributes()

    else:

        print(" is Invalid")

    print("\n")

def Main():

    # type_of_character - Describes which column of the state transition
    #                     matrix we are currently looking at.
    # transition_table  - contains state transition
    # inputs            - each row of this 2D array describes a column in the
    #                     state transition table.
    # accepting_states  - array of states that accept the string as valid.
    # rejecting_states  - array of states that reject the string as invalid.
    #                     (There is currently only one rejecting state)
    # input_file        - Name of file to retrieve test input strings
    # state             - Current state in transition table / FSA
    # valid             - Boolean value describing if an individual string is accepted
    # type_of_character - Describes which column of the transition table the
    #                     current input symbol belongs to.

    inputs, transition_table, accepting_states, rejecting_states = Get_Config_Info()

    input_file = open("<filename>", "r")
    
    for line in input_file:

        print()

        # Reset the state and validity of each new string
        state = '0'
        valid = True

        # We strip the new line character from each line because it is not
        # considered to be part of the input string.
        for a in (line.lstrip().rstrip('\n')):

            print(a, end='', sep='')

            # As long as we have not encountered a rejecting state,
            # we keep analyzing the next character.
            # Note that if we do reach a rejecting state, we just
            # read through until we reach the next string.
            if not (state in rejecting_states) and (valid):

                type_of_character = Characterize_Input_Symbol(a, inputs)

                # type_of_character could describe a character not in the given
                # alphabet, so if it is part of the alphabet, we analyze it.
                if type_of_character < len(inputs):

                    my_regular_expression.Mealy(a, state)
                    state = Apply_Transition_Table(transition_table, state, type_of_character)
                    my_regular_expression.Moore(a, state)

                else:

                    # In this conditional, we are saying that if a character is outside of
                    # the given possible inputs, we know the string is invalid.
                    valid = False

            else:

                # Here, we know that the state is in a rejecting
                # state, so we know the string is invalid.
                valid = False

        if not(state in accepting_states):
            valid = False

        Print_Validity(valid)

        my_regular_expression.Clear_Attributes()

    input_file.close()

Main()