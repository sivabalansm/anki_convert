#! /bin/python3
import argparse
import genanki

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stage", type=str)
parser.add_argument("-c", "--commit", type=str)
args = parser.parse_args()



# just reading from a file complexified a little :)
def get_text(file=""):
    if file != "":
        with open(file, 'r') as f:
            text = f.read()
        return text
    else:
        raise Exception("Need a file Name")



# prepeation of files
class Stage:
    def __init__(self, text):
        self.text = text
        self.common_stop = "@@"
        # follow up after a field in anki
        self.identifiers = {"@D": "@Q", "@Q": "@A", "@A": "@Q"}

    def custom_str(self, string, pad="\n\n\n"):
        return f"{pad}{string}{pad}"


    def format(self):
        formatted = ""
        held_chars = tuple(self.identifiers.keys())[0]
        skip = False

        for i in range(len(self.text)):

            # skiping an iteration for certain conditions
            if skip == True:
                skip = False

            else:
                char = self.text[i]
                two_char = self.text[i:i+2]
                
                if two_char == self.common_stop:
                    # adding two chars, then we must skip an iteration to go to the third char
                    formatted += self.custom_str(two_char)
                    skip = True

                elif two_char == held_chars:
                    # adding two chars, then we must skip an iteration to go to the third char
                    # changing the next character to be the one that supposed to follow like Q -> A or D -> Q
                    held_chars = self.identifiers[held_chars]
                    formatted += self.custom_str(two_char)
                    skip = True

                else:
                    formatted += char

        return formatted
                

class Commit:
    def __init__(self, text):
        self.text = text

    # parse every @Q, @A and '--' for stopping 
    def parse(self):
        pass



print(Stage(text).format())
