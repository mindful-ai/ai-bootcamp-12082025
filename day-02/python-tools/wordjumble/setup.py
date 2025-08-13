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