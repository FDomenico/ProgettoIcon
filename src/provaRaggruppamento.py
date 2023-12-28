from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

df = pd.read_csv("../dataset/traffic_violations_preprocessing.csv")
# Prepara i dati (X: descrizioni)
X = df['description']

# Vettorizzazione delle parole
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Applica l'algoritmo di raggruppamento
k = 587  # Numero di cluster desiderati
kmeans = KMeans(n_clusters=k)
kmeans.fit(X_vectorized)

# Etichette di cluster assegnate
labels = kmeans.labels_

# Aggiungi le etichette di cluster al DataFrame
df['cluster'] = labels

# Visualizza le descrizioni e i rispettivi cluster
print(df[['description', 'cluster']])
