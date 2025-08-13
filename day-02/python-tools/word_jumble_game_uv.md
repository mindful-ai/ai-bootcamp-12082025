# Packaging Word Jumble Game with Astral UV

## 1) Project Structure

```
word-jumble-game/
├── pyproject.toml
├── README.md
├── word_jumble_game/
│   ├── __init__.py
│   └── cli.py
```

---

## 2) pyproject.toml

```toml
[project]
name = "word-jumble-game"
version = "0.1.0"
description = "A fun Python word jumble game with CLI support."
authors = [{ name = "Your Name", email = "you@example.com" }]
license = { text = "MIT" }
readme = "README.md"
requires-python = ">=3.7"
dependencies = []

[project.scripts]
word-jumble-game = "word_jumble_game.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

## 3) word_jumble_game/__init__.py

```python
__version__ = "0.1.0"
```

---

## 4) word_jumble_game/cli.py

```python
import random
import time
import argparse

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
        print("Welcome to the Word Jumble Game!")
        for _ in range(rounds):
            self.play_round()
        print(f"Game Over! Your final score is {self.score}")

class TimedWordJumbleGame(WordJumbleGame):
    def __init__(self, words, time_limit=5):
        super().__init__(words)
        self.time_limit = time_limit

    def play_round(self):
        word = self.get_random_word()
        jumbled = self.jumble_word(word)
        print(f"Jumbled word: {jumbled}")
        print(f"You have {self.time_limit} seconds to answer!")

        start_time = time.time()
        guess = input("Your guess: ")
        elapsed_time = time.time() - start_time

        if elapsed_time > self.time_limit:
            print("⏱ Time’s up!")
        elif guess.lower() == word:
            print("✅ Correct!")
            self.score += 1
        else:
            print(f"❌ Wrong! The correct word was '{word}'.")

def main():
    parser = argparse.ArgumentParser(description="Play the Word Jumble Game!")
    parser.add_argument("--rounds", type=int, default=3, help="Number of rounds to play")
    parser.add_argument("--timed", action="store_true", help="Enable timed mode")
    parser.add_argument("--time-limit", type=int, default=5, help="Time limit for each round in timed mode")
    args = parser.parse_args()

    words = ["python", "programming", "object", "inheritance", "polymorphism"]

    if args.timed:
        game = TimedWordJumbleGame(words, time_limit=args.time_limit)
    else:
        game = WordJumbleGame(words)

    game.play(rounds=args.rounds)

if __name__ == "__main__":
    main()
```

---

## 5) Install Astral UV

```bash
pip install uv
# OR
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 6) Initialize Environment

```bash
uv init word-jumble-game
```
*(or create the files manually as above)*

---

## 7) Sync Dependencies

```bash
uv sync
```

---

## 8) Build Package

```bash
uv build
```
Generates:
```
dist/word_jumble_game-0.1.0.tar.gz
dist/word_jumble_game-0.1.0-py3-none-any.whl
```

---

## 9) Install Locally

```bash
uv pip install dist/word_jumble_game-0.1.0-py3-none-any.whl
```

---

## 10) Run the Game

```bash
word-jumble-game --rounds 5
```
or  
```bash
uv run word-jumble-game --rounds 5
```

---

## 11) Publish to PyPI

```bash
uv publish --token <YOUR_PYPI_TOKEN>
```
