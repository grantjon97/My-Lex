# Jonathan Grant
# regularlanguage.py
# Lexical Analyzer
# 10 November 2017
#
# To test the FSA in main.py, we will use email addresses as our regular language.
# Our simplified definition of the regular language for email addresses is as follows:
#
# An email address has a username, '@' symbol, host, and domain.
# The username may contain any combination of letters and numbers,
# and one '.' which cannot be the first or last character.
# The host may be any combination of letters, i.e. one name.
# The host and domain are separated by a '.'
# The domain may be any combination of letters, followed by a '.',
# and then another combination of letters. (ex. "wcusd5.net")

class email:
    """ Splits an email into tokens by communinicating with a corresponding FSA. """

    username = ''
    local_host = ''
    sld = ''
    tld = ''

    def Print_Attributes(self):
        """ Displays the individual parts of the email address, i.e. tokens """

        print("\nUsername:   ", self.username)
        print("Local Host: ", self.local_host)
        print("SLD:        ", self.sld)
        print("TLD:        ", self.tld)

    def Clear_Attributes(self):
        """ Resets the object's attributes to be used for another input string. """

        self.username = ''
        self.local_host = ''
        self.sld = ''
        self.tld = ''
        
    def Mealy(self, character, previous_state):
        """ Builds tokens based off of the previous state and current character. """

        # Inside this conditional, we know we are looking at the part of
        # the email address after the '@' symbol.
        if (4 <= int(previous_state) <= 7):

            # We assume that the last character we saw was part of the TLD.
            # If the character is a '.' then we shift the contents of the SLD 
            # to the local host, and we shift the contents of the TLD to the SLD.

            if character == '.':

                if self.local_host != '':
                    self.local_host = self.local_host + '.' + self.sld
                else:
                    self.local_host = self.local_host + self.sld

                self.sld = self.tld
                self.tld = ''

            else:

                self.tld = self.tld + character


    def Moore(self, character, next_state):
        """ Builds tokens based off of the next state and current character. """

        # If we still haven't encountered an '@' symbol, then we will keep
        # adding each character to the username.
        if (1 <= int(next_state) <= 3):

            self.username = self.username + character

def Initialize_Class():

    return email()