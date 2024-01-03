import pandas as pd

dc = pd.read_csv("../dataset/stat_cluster.csv")

dataset_ordinato = dc.sort_values(by='cluster')

# Sostituisci 'nome_file_output.csv' con il percorso e il nome desiderato per il file CSV
dataset_ordinato.to_csv("../dataset/stat_cluster2.csv", index=False)
