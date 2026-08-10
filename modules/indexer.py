import sqlite3
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi


class IndexBuilder:

    def __init__(self):

        self.conn = sqlite3.connect("data/news.db")

    def build(self):

        df = pd.read_sql(
            "SELECT * FROM articles",
            self.conn
        )

        corpus = df["content"].fillna("").tolist()

        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000,
            ngram_range=(1,2)
        )

        tfidf = vectorizer.fit_transform(corpus)

        tokenized = [
            doc.lower().split()
            for doc in corpus
        ]

        bm25 = BM25Okapi(tokenized)

        joblib.dump(vectorizer,"data/vectorizer.pkl")
        joblib.dump(tfidf,"data/tfidf.pkl")
        joblib.dump(bm25,"data/bm25.pkl")

        return df