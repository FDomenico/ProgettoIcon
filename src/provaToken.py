import nltk
import pandas as pd
from rake_nltk import Rake
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
# Carica il dataset con le descrizioni
df = pd.read_csv("../dataset/traffic_violations_preprocessing.csv")

# Inizializza l'oggetto Rake per l'estrazione delle parole chiave
r = Rake()


def pre_elaborazione(testo):
    # Tokenizzazione del testo
    words = word_tokenize(testo)
    # Rimozione delle stopwords
    words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    return ' '.join(words)


# Funzione per estrarre le parole chiave da una descrizione
def estrai_parole_chiave(testo):
    r.extract_keywords_from_text(testo)
    return r.get_ranked_phrases()[0] if r.get_ranked_phrases() else None


df['testo_pre_elaborato'] = df['description'].apply(pre_elaborazione)
# Applica la funzione per estrarre le parole chiave da ogni descrizione
df['parole_chiave'] = df['testo_pre_elaborato'].apply(estrai_parole_chiave)
#csv_description_keyword = df[['description', 'parole_chiave']]
#description_keyword = pd.DataFrame(csv_description_keyword)
#csv_parole_chiave = df['parole_chiave'].unique()
#keyword = pd.DataFrame(csv_parole_chiave)

# Visualizza il dataframe con le parole chiave generate
#print(description_keyword[['description', 'parole_chiave']])

# Salva il risultato in un file CSV
#description_keyword.to_csv("../dataset/parole_chiave_descrizione.csv", index=False)
#keyword.to_csv("../dataset/parole_chiave.csv", index=False)
drop_column_traffic = ['description', 'testo_pre_elaborato']
df.drop(drop_column_traffic, axis=1, inplace=True)

keyword_column = df.pop('parole_chiave')
df.insert(df.columns.get_loc('UniqueCode') + 1, 'parole_chiave', keyword_column)

df.to_csv("../dataset/traffic_violation_keyword.csv", index=False)
