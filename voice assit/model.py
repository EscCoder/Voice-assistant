from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import data

X_train = []
y_train = []

for category, documents in data.data.items():
    X_train.extend(documents)
    y_train.extend([category] * len(documents))

    # Feature extraction
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)

    # Train a classifier
classifier = LogisticRegression()
classifier.fit(X_train_tfidf, y_train)

joblib.dump(classifier, 'saved_model/classifier_model.pkl')
joblib.dump(vectorizer, 'saved_model/vectorizer_model.pkl')