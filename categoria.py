import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Carica il dataset con le violazioni e parole chiave
df = pd.read_csv("dataset/traffic_violation_keyword.csv")

# Creazione del vettore TF-IDF basato sulle parole chiave
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['parole_chiave'].astype(str))

# Clustering delle violazioni con K-Means
num_clusters = 25
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(tfidf_matrix)

# Visualizza il DataFrame con i cluster assegnati
print(df[['parole_chiave', 'cluster']])

stat_dls = df[['parole_chiave', 'cluster']]
df_stat_dls = pd.DataFrame(stat_dls)

# Salva il risultato in un nuovo file CSV
df.to_csv("../dataset/dataset_clusterizzato.csv", index=False)
df_stat_dls.to_csv("../dataset/stat_cluster.csv", index=False)

dc = pd.read_csv("dataset/stat_cluster.csv")
# Definisci le colonne da visualizzare per ciascun cluster
colonne_da_visualizzare = ['parole_chiave']

# Stampa i valori delle colonne per ciascun cluster
lista_numeri = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
cluster_df = pd.DataFrame(columns=['cluster'] + colonne_da_visualizzare)
for cluster_id in lista_numeri:
    cluster_df = dc[dc['cluster'] == cluster_id]

cluster_df.to_csv("../dataset/stat_cluster2.csv", index=False)
