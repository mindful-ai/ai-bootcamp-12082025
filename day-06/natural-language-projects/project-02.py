import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize, ConditionalFreqDist
import random

# Download resources
nltk.download('punkt')

# Example dataset: AG News headlines (simplified demo)
headlines = [
    "Stocks rally after positive earnings report",
    "New study reveals climate change impact",
    "Local team wins championship final",
    "Government announces new economic policy",
    "Technology companies launch AI initiatives"
]

# Step 1: Tokenize
tokens = [word_tokenize(h.lower()) for h in headlines]
tokens = [["<s>"] + t + ["</s>"] for t in tokens]  # add sentence markers

# Flatten
flat_tokens = [w for sent in tokens for w in sent]

# Step 2: Build Bigrams
bigrams = list(nltk.bigrams(flat_tokens))
cfd_bigram = ConditionalFreqDist(bigrams)

# Step 3: Text generation (bigram model)
def generate_bigram_text(start_word="<s>", num_words=10):
    word = start_word
    sentence = []
    for i in range(num_words):
        if word not in cfd_bigram:
            break
        next_word = random.choice(list(cfd_bigram[word].keys()))
        if next_word == "</s>":
            break
        sentence.append(next_word)
        word = next_word
    return " ".join(sentence)

print("Generated Headlines (Bigram Model):")
for _ in range(5):
    print("-", generate_bigram_text())

# Step 4: Extend to Trigrams
trigrams = list(nltk.trigrams(flat_tokens))
cfd_trigram = ConditionalFreqDist(((w1, w2), w3) for w1, w2, w3 in trigrams)

def generate_trigram_text(start_words=("<s>",), num_words=10):
    w1, w2 = start_words if len(start_words) == 2 else ("<s>", start_words[0])
    sentence = []
    for i in range(num_words):
        if (w1, w2) not in cfd_trigram:
            break
        next_word = random.choice(list(cfd_trigram[(w1, w2)].keys()))
        if next_word == "</s>":
            break
        sentence.append(next_word)
        w1, w2 = w2, next_word
    return " ".join(sentence)

print("\nGenerated Headlines (Trigram Model):")
for _ in range(5):
    print("-", generate_trigram_text())
