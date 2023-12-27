from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# Preparazione dei dati
df = pd.read_csv("../dataset/parole_chiave.csv")  # Sostituisci con il tuo DataFrame
X = df['description'].astype(str)
y = df['parola_chiave']  # Sostituisci con la tua colonna di categorie

# Estrazione delle caratteristiche
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Divisione in set di training e test
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

# Creazione e addestramento del modello
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Valutazione del modello
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print(f"Classification Report:\n{report}")
