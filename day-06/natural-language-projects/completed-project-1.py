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

# Step 3: Preprocess text
stop_words = set(stopwords.words('english'))
def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    return tokens

df['tokens'] = df['headline'].apply(preprocess)

# Step 4: Train Word2Vec model
model = Word2Vec(sentences=df['tokens'], vector_size=100, window=5, min_count=1, workers=4)

# Step 5: Create document embeddings
def get_doc_embedding(tokens, model):
    vectors = [model.wv[word] for word in tokens if word in model.wv]
    if len(vectors) == 0:
        return [0]*100
    return sum(vectors)/len(vectors)

df['embedding'] = df['tokens'].apply(lambda x: get_doc_embedding(x, model))

# Step 6: Apply KMeans clustering
X = list(df['embedding'])
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X)

# Step 7: Visualize with PCA
pca = PCA(n_components=2)
reduced = pca.fit_transform(X)
plt.scatter(reduced[:,0], reduced[:,1], c=df['cluster'])
for i, txt in enumerate(df['headline']):
    plt.annotate(i, (reduced[i,0], reduced[i,1]))
plt.title("News Headline Clusters using Word2Vec + KMeans")
plt.show()

# Step 8: Print results
for cluster in range(3):
    print(f"\nCluster {cluster}:")
    print(df[df['cluster']==cluster]['headline'].tolist())
