import random
import nltk
from nltk.corpus import gutenberg
from nltk import bigrams, trigrams
from collections import defaultdict

# Download required resources
nltk.download("gutenberg")
nltk.download("punkt")

# 1. Load Shakespeare text (Macbeth from Gutenberg corpus)
text = gutenberg.raw('shakespeare-macbeth.txt')

# 2. Preprocess - tokenize into words


# 3. Build a bigram model (word -> possible next words)


# 4. Function to generate text


# 5. Generate sentences

