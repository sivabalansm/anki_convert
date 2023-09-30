#! /bin/python3
import argparse
import datetime
import genanki

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stage", type=str)
parser.add_argument("-c", "--commit", type=str)
args = parser.parse_args()


# get current time 
def get_time(switch):
    now = datetime.datetime.now()
    if bool(switch):
        return int(now.strftime("%m%d%H%M%S"))
    else:
        return now.strftime("%Y%m%d_%H%M%S")

# just reading from a file complexified a little :)
def get_text(file=""):
    if bool(file): # if file not empty string
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
            if skip:
                skip = False

            else:
                char = self.text[i]
                two_chars = self.text[i:i+2]
                
                if two_chars == self.common_stop:
                    # adding two chars, then we must skip an iteration to go to the third char
                    formatted += self.custom_str(two_chars)
                    skip = True

                elif two_chars == held_chars:
                    # adding two chars, then we must skip an iteration to go to the third char
                    # changing the next character to be the one that supposed to follow like Q -> A or D -> Q
                    held_chars = self.identifiers[held_chars]
                    formatted += self.custom_str(two_chars)
                    skip = True

                else:
                    formatted += char

        return formatted
                




class Commit:
    def __init__(self, text):
        self.text = text
        self.parsed = ()
        self.identifiers = {"@D": "@Q", "@Q": "@A", "@A": "@Q"}
        self.common_stop = "@@"

    def clean_string(self, string):
        clean_str = string
        bad_chars = ("@X", "@X", self.common_stop)

        for bchar in bad_chars: 
            clean_str = clean_str.replace(bchar, "")

        return clean_str.strip()

    def array_pairing(self, array):
        paired_array = []
        array_len = len(array)
        if array_len > 0 and array_len % 2 == 0:
            for i in range(0, array_len, 2):
                paired_array.append([array[i], array[i+1]])

        return paired_array



    # parse every @Q, @A and '--' for stopping 
    def parse(self):
        notes = []
        skip = False
        erase = False
        deck_name = ""
        deck_chars = tuple(self.identifiers.keys())[0]
        held_chars = tuple(self.identifiers.keys())[1]
        held_str = ""

        for i in range(len(self.text)):
            char = self.text[i]
            two_chars = self.text[i:i+2]


            # skip 1 character, usually the D, Q or A in @D, @Q or @A
            if skip:
                skip = False

            # set the deck name and erase everything behind for clean start
            elif two_chars == deck_chars:
                held_str = ""

                skip = True
                deck_naming = True


            # main checks

            elif two_chars == self.common_stop:
                #held_chars = self.identifiers[held_chars]

                # we must erase the held_str in the next loops
                erase = True

                if deck_naming: 
                    deck_name = self.clean_string(held_str)
                    deck_naming = False
                else:
                    notes.append(self.clean_string(held_str))

                skip = True
                held_str = "" 

            elif two_chars == held_chars:
                held_chars = self.identifiers[held_chars]

                # this is where the erasure happens set by common_stop
                if erase:
                    erase = False

                # default adds
                elif deck_naming: 
                    deck_name = self.clean_string(held_str)
                    deck_naming = False
                else:
                    notes.append(self.clean_string(held_str))

                skip = True
                held_str = ""

            # main string summation, all relies on this
            else:
                held_str += char


        self.parsed = (deck_name, self.array_pairing(notes))
        return self.parsed

    def write(self, name_gen, file):
        if len(self.parsed) > 0:
            deck_name, notes = self.parsed
            if not deck_name:
                deck_name = name_gen()
            my_model = genanki.Model(
              1607392319,
              'Simple Model',
              fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
              ],
              templates=[
                {
                  'name': 'Card 1',
                  'qfmt': '{{Question}}',
                  'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                },
              ])
            deck = genanki.Deck(name_gen('-y'), deck_name)

            for note in notes:
                q, a = note
                deck.add_note(genanki.Note(model=my_model, fields=[q.replace("\n", "<br>"),a.replace("\n", "<br>")]))


            genanki.Package(deck).write_to_file(f'{file}.apkg')




        else:
            raise Exception("Empty deck data")


def main():
    raw_file = args.stage
    pre_commit_file = args.commit

    if bool(raw_file) and not pre_commit_file:
        text = get_text(raw_file)
        staged_text = Stage(text).format()

        with open(f'{raw_file}.acs', 'w') as f:
            f.write(staged_text)

    elif bool(pre_commit_file) and not raw_file:
        text = get_text(pre_commit_file)
        deck_data = Commit(text)
        deck_name,notes = deck_data.parse()

        print(deck_name)
        for note in notes:
            print(f"QUESTION:\n{note[0]}\n\nANSWER:\n{note[1]}\n\n\n")

        if input("This is what is about to be committed, are you sure (y/n): ").lower() == "y":
            deck_data.write(get_time, pre_commit_file)


        else: 
            print("Not committing, exiting...")
            exit()

            
    else:
        raise Exception("You have to set 1 flag at a time")

        
#commit_array = Commit(staged_text).parse()
#
#for i in commit_array[1]:
#    print(i)
#    print('----')
#print(args.commit)
main()
#add_note(genanki.Note(fields=note))
