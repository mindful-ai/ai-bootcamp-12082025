# Step 1: Import libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import gensim
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import string

nltk.download('punkt')
nltk.download('stopwords')

# Step 2: Load dataset (small news headlines dataset)
data = [
    "Apple unveils new iPhone with better camera",
    "Samsung releases foldable phone in global market",
    "Stock markets see biggest drop in two years",
    "Investors worried about economic slowdown",
    "NASA announces new mission to explore Jupiter",
    "SpaceX successfully launches Starlink satellites",
    "Football World Cup final breaks TV viewership records",
    "Olympics postponed due to global health crisis"
]

df = pd.DataFrame(data, columns=['headline'])

# Step 3: Preprocess text - tokenize and remove stop words


# Step 4: Train Word2Vec model


# Step 5: Create document embeddings


# Step 6: Apply KMeans clustering


# Step 7: Visualize with PCA


# Step 8: Print results

