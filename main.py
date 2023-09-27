#! /bin/python

with open('test.md', 'r') as f:
    text = f.read()

class Stage:
    def __init__(self, text):
        self.text = text

    def string_insert(self, position, str):
        self.text


    def format():
        pass

class Parser:
    def __init__(self, text):
        self.text = text

    # parse every @Q, @A and '--' for stopping 
    def parse(self):
        pass



print(text.index("@Q"))
