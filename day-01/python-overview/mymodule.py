import random

def get_random_word():
    words = ["python", "programming", "object", "inheritance", "polymorphism"]
    return random.choice(words)

def jumble_word(word):
    return ''.join(random.sample(word, len(word)))

def play_game():
    word = get_random_word()
    jumbled = jumble_word(word)
    print("Welcome to the Word Jumble Game!")
    print(f"Jumbled word: {jumbled}")

    guess = input("Your guess: ")
    if guess.lower() == word:
        print("Correct! You guessed it right!")
    else:
        print(f"Oops! The correct word was '{word}'.")

print("__name__ (mymodule) = ", __name__)
if __name__ == "__main__":
    play_game()

