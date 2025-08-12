# Python Workshop: Word Jumble Game

In this workshop, we'll explore **procedural** and **object-oriented** approaches in Python using a single project: **Word Jumble Game**.

---

## Part 1 – Non-OOP Word Jumble Game

```python
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

if __name__ == "__main__":
    play_game()
```

### Drawbacks of the Non-OOP Approach
- **Poor scalability**: Adding difficulty levels, scoring, or multiple players means rewriting multiple functions.
- **Code duplication**: Logic might repeat if we add new modes.
- **Harder to maintain**: No clear structure; related data and behavior are scattered.
- **Limited reusability**: Can't easily reuse the game logic in other applications.

---

## Part 2 – OOP Word Jumble Game

Here we’ll use **classes, objects, inheritance, and polymorphism**.

```python
import random

class WordGame:
    def __init__(self, words):
        self.words = words

    def get_random_word(self):
        return random.choice(self.words)

    def jumble_word(self, word):
        return ''.join(random.sample(word, len(word)))

class WordJumbleGame(WordGame):
    def __init__(self, words):
        super().__init__(words)
        self.score = 0

    def play_round(self):
        word = self.get_random_word()
        jumbled = self.jumble_word(word)
        print(f"Jumbled word: {jumbled}")

        guess = input("Your guess: ")
        if guess.lower() == word:
            print("✅ Correct!")
            self.score += 1
        else:
            print(f"❌ Wrong! The correct word was '{word}'.")

    def play(self, rounds=3):
        print("Welcome to the OOP Word Jumble Game!")
        for _ in range(rounds):
            self.play_round()
        print(f"Game Over! Your final score is {self.score}")
```

---

### Polymorphism Example – Timed Version

```python
import time

class TimedWordJumbleGame(WordJumbleGame):
    def play_round(self):
        word = self.get_random_word()
        jumbled = self.jumble_word(word)
        print(f"Jumbled word: {jumbled}")
        print("You have 5 seconds to answer!")

        start_time = time.time()
        guess = input("Your guess: ")
        elapsed_time = time.time() - start_time

        if elapsed_time > 5:
            print("⏱ Time’s up!")
        elif guess.lower() == word:
            print("✅ Correct!")
            self.score += 1
        else:
            print(f"❌ Wrong! The correct word was '{word}'.")

if __name__ == "__main__":
    words = ["python", "programming", "object", "inheritance", "polymorphism"]
    game = TimedWordJumbleGame(words)
    game.play()
```

---

## Advantages of OOP
- **Encapsulation**: Data (`words`, `score`) and methods are packaged together.
- **Reusability**: The base `WordGame` class can be reused for other word-based games.
- **Extensibility**: Adding features like timed rounds just requires subclassing.
- **Polymorphism**: Different game types can share the same interface (`play_round`), making the code more flexible.
- **Maintainability**: Structured and modular, easier for teams to work on.

---

## Suggested Exercises
1. Add **difficulty levels** (easy, medium, hard) with different word lengths.
2. Add a **hint system** that reveals one letter at a time.
3. Implement a **multiplayer mode** where two players take turns.
4. Store high scores in a **file** for persistence.

---
