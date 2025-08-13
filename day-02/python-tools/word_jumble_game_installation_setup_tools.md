# Word Jumble Game – Installable Package with setuptools

## 1) Files & Package Layout

```
word_jumble_game_pkg/
├── LICENSE
├── README.md
├── pyproject.toml
├── setup.cfg
├── setup.py
└── word_jumble_game/
    ├── __init__.py
    └── cli.py
```

`word_jumble_game/cli.py` contains the OOP version of the game plus a `main()` function used as the console entry point. `__init__.py` defines the package version.

---

## 2) Commands to Build

```bash
# inside the project root (where setup.py & setup.cfg live)
python setup.py sdist bdist_wheel
```

Artifacts generated in the `dist/` folder:
- `dist/word_jumble_game-0.1.0.tar.gz` (sdist)
- `dist/word_jumble_game-0.1.0-py3-none-any.whl` (wheel)

---

## 3) Build Output (Essential Parts)

```
running sdist
running egg_info
creating word_jumble_game.egg-info
writing word_jumble_game.egg-info/PKG-INFO
writing entry points to word_jumble_game.egg-info/entry_points.txt
...
creating 'dist/word_jumble_game-0.1.0-py3-none-any.whl'
adding 'word_jumble_game/__init__.py'
adding 'word_jumble_game/cli.py'
adding 'word_jumble_game-0.1.0.dist-info/METADATA'
adding 'word_jumble_game-0.1.0.dist-info/WHEEL'
adding 'word_jumble_game-0.1.0.dist-info/entry_points.txt'
adding 'word_jumble_game-0.1.0.dist-info/RECORD'
removing build/bdist.linux-x86_64/wheel
```

---

## 4) Install & Run

### Install from Wheel
```bash
pip install dist/word_jumble_game-0.1.0-py3-none-any.whl
```

### Install from Source Tarball
```bash
pip install dist/word_jumble_game-0.1.0.tar.gz
```

### Install from GitHub (after pushing repo)
```bash
pip install git+https://github.com/<your-username>/word_jumble_game.git
```

---

## 5) Running the Game

After install:
```bash
word-jumble-game
word-jumble-game --rounds 5
word-jumble-game --timed
```

Run without installing:
```bash
python -m word_jumble_game.cli --rounds 2
```

---

## 6) Notes & Improvements

- Current package is minimal; `input()` blocks execution.
- Add automated tests with `pytest`.
- Add GitHub Actions for CI/CD.
- Consider moving fully to `pyproject.toml` builds with `python -m build`.
