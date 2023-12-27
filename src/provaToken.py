import nltk
from nltk.tokenize import word_tokenize
import pandas as pd
import re

nltk.download("punkt")
df = pd.read_csv("../dataset/traffic_violations_preprocessing.csv")

descriptions = df["description"]
tokenized_descriptions = descriptions.apply(lambda x: word_tokenize(str(x)))

df["tokenized_description"] = tokenized_descriptions
print(df[["description", "tokenized_description"]])

parole_chiave = [
    "expired registration plate",
    "driving under the influence",
    "exceeding maximum speed",
    "failure to display registration card"
]


def trova_parole_chiave(testo):
    for keyword in parole_chiave:
        if re.search(keyword, str(testo), re.IGNORECASE):
            return keyword
    return None


# Applica la funzione alle descrizioni per trovare le parole chiave
df['parola_chiave'] = df['description'].apply(trova_parole_chiave)

# Visualizza le righe che contengono parole chiave
righe_con_parole_chiave = df[df['parola_chiave'].notnull()]
print(righe_con_parole_chiave[['description', 'parola_chiave']])

df_output = righe_con_parole_chiave[['description', 'parola_chiave']]
df_output.to_csv("../dataset/parole_chiave.csv", index=False)



