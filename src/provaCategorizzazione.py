import pandas as pd
from rake_nltk import Rake

# Carica il dataset con le parole chiave singole
df = pd.read_csv("../dataset/parole_chiave_singole.csv")

# Definisci le categorie
categorie = {
    "Violation": ["driving", "failure", "exceeding", "illegal", "reckless", "jaywalking"],
    "License": ["license", "suspended", "revoked"],
    "Safety": ["safety", "improper", "negligent", "seatbelt"],
    "Traffic Signs": ["traffic control device", "stop", "yield", "intersection"],
    # Aggiungi altre categorie con le parole chiave pertinenti
}


def categorizza_parola_chiave(parole_chiave):
    # Esegui la corrispondenza della parola chiave con le categorie
    for categoria, parole_chiave_categoria in categorie.items():
        for parola in parole_chiave.lower().split():
            if parola in parole_chiave_categoria:
                return categoria
    return "Altro"  # Se non corrisponde a nessuna categoria


# Applica la funzione per categorizzare le parole chiave
df['categoria'] = df['parole_chiave'].apply(categorizza_parola_chiave)

# Salva il risultato con le categorie in un nuovo file CSV
df.to_csv("../dataset/parole_chiave_categorizzate.csv", index=False)