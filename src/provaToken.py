import nltk
import pandas as pd
from rake_nltk import Rake


nltk.download('stopwords')
# Carica il dataset con le descrizioni
df = pd.read_csv("../dataset/traffic_violations_preprocessing.csv")

# Inizializza l'oggetto Rake per l'estrazione delle parole chiave
r = Rake()


# Funzione per estrarre le parole chiave da una descrizione
def estrai_parole_chiave(testo):
    r.extract_keywords_from_text(testo)
    return r.get_ranked_phrases()[0] if r.get_ranked_phrases() else None


# Applica la funzione per estrarre le parole chiave da ogni descrizione
df['parole_chiave'] = df['description'].apply(estrai_parole_chiave)
csv_description_keyword = df[['description', 'parole_chiave']]
description_keyword = pd.DataFrame(csv_description_keyword)

# Visualizza il dataframe con le parole chiave generate
print(description_keyword[['description', 'parole_chiave']])

# Salva il risultato in un file CSV
description_keyword.to_csv("../dataset/parole_chiave_singole.csv", index=False)
