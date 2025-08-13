# Packaging Word Jumble Game with setuptools

## Directory Structure
```
wordjumble/
│
├── setup.py
├── README.md
├── LICENSE
├── wordjumble
│   ├── __init__.py
│   ├── cli.py
```
---

## 1. setup.py
```python
from setuptools import setup, find_packages

setup(
    name="wordjumble",
    version="1.0.0",
    author="Purushotham",
    author_email="purushotham.s@mindfullearning.in",
    description="A fun Word Jumble game in Python",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "wordjumble=wordjumble.cli:main",
        ],
    },
    python_requires=">=3.6",
)
```
**Explanation:**
- `find_packages()` detects the `wordjumble` folder as a package.
- `entry_points` lets you run the game directly using `wordjumble` in the terminal.

---

## 2. README.md
```markdown
# Word Jumble Game

A simple command-line word jumble game built with Python.

## Installation
```bash
pip install .
```

## Usage
```bash
wordjumble --rounds 5 --timed --time-limit 10
```
```

---

## 3. LICENSE
You can use MIT License or any open-source license.

---

## 4. wordjumble/__init__.py
```python
# Empty file to make this a package
```

---

## 5. wordjumble/cli.py
```python
# Full game code here (from your existing cli.py file)
```

---

## 6. Installation and Running

From the project root:
```bash
pip install .
```

Run the game:
```bash
wordjumble --rounds 5 --timed --time-limit 10
```

---

## 7. Notes
- Ensure you have Python 3.6+ installed.
- The `console_scripts` entry point eliminates the need to run `python wordjumble/cli.py` directly.
- This setup can be extended to publish your package to PyPI.
