import random

class WordJumbleGame(object):

    files = ['words.txt']

    # Constructor
    def __init__(self, name, level=0):
        self.name = name
        self.points = 0
        self.words = self.fetch_words(WordJumbleGame.files[level])

    # Jumble
    def jumble(self, w):
        temp = list(w)
        random.shuffle(temp)
        return ''.join(temp)

    # Word Fetch
    def fetch_words(self, file):
        f = open(file)
        content = f.read()
        f.close()
        return [word.strip() for word in content.split(',')]

    # Run function
    def run(self):
        # for every word in list of words
        random.shuffle(self.words)

        for word in self.words:

            print("\n")

            # jumble the word
            jumbled_word = self.jumble(word)

            # show to the user
            print(jumbled_word)

            # ask user input
            user_word = input("Can you guess -> ")

            # compare user input and update points
            if(user_word == word):
                self.points += 1
                print("\U00002705 Correct")
            else:
                print("\U00002745 In-correct")

        self.display_results()


    # Results
    def display_results(self):
        print("\n")
        print("NAME".ljust(10), ' -> ', self.name)
        print("-"*80)
        if(self.points > 6):
            print("You have played well")
        else:
            print("You need to improve on your vocabulary")

# Test

if __name__ == "__main__":

    p = WordJumbleGame("Purushotham")
    p.run()
