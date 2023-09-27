#! /bin/python

with open('test.md', 'r') as f:
    text = f.read()

class Stage:
    def __init__(self, text):
        self.text = text
        common_stop = "--"
        self.identifiers = {"@D": (common_stop, "@Q"), "@Q": (common_stop, "@A"), "@A": (common_stop, "@Q")]

    def custom_str(self, string, pad="\n"):
        return f"{pad}{string}{pad}"


    def format(self):
        formatted = ""
        skip = False

        for i in range(len(self.text)):

            # skiping an iteration for certain conditions
            if skip == True:
                skip = False

            else:
                char = self.text[i]
                two_char = self.text[i:i+2]
                
                if two_char in self.identifiers:


                    formatted += custom_str(two_char)
                    skip = True
                



class Parser:
    def __init__(self, text):
        self.text = text

    # parse every @Q, @A and '--' for stopping 
    def parse(self):
        pass



print(Stage(text).format())
