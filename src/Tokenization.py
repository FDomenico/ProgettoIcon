import nltk
import pandas as pd
from rake_nltk import Rake
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def tokenization(df1: pd.DataFrame):
    df = df1
    nltk.download('punkt')
    nltk.download('stopwords')

    df['preprocessed_text'] = df['description'].apply(pre_elaborazione)
    # Applica la funzione per estrarre le parole chiave da ogni descrizione
    df['keywords'] = df['preprocessed_text'].apply(estrai_parole_chiave)

    drop_column_traffic = ['description', 'preprocessed_text']
    df.drop(drop_column_traffic, axis=1, inplace=True)

    keyword_column = df.pop('keywords')
    df.insert(df.columns.get_loc('unique_code') + 1, 'keywords', keyword_column)

    return df


def pre_elaborazione(testo):
    stop_words = set(stopwords.words('english'))

    words = word_tokenize(testo) # Tokenizzazione del testo
    words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words] # Rimozione delle stopwords

    return ' '.join(words)


# Funzione per estrarre le parole chiave da una descrizione
def estrai_parole_chiave(testo):
    r = Rake()

    r.extract_keywords_from_text(testo)
    return r.get_ranked_phrases()[0] if r.get_ranked_phrases() else None

