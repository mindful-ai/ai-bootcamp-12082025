import random

# List of words
LW = ["apple", "banana", "cherry", "laptop", "mobile", "computer"]
random.shuffle(LW)
points = 0

# Pick a word
for word in LW:

    # Jumble the word
    t = list(word)
    random.shuffle(t)
    jword = ''.join(t)

    # Show the jumbled word
    print("Jumbled Word -> ", jword.upper())

    # Ask the user and let the user input the guessed word
    userInput = input("Guess the word -> ")

    # Compare the guessed and picked word; offer the points
    if(userInput.lower() == word.lower()):
        points += 1
        print("Correct\n")
    else:
        print("Incorrect\n")

# Repeat the process

# Show the results to the user
if(points > 3):
    print("Excellent playing!")
else:
    print("Need to improve")