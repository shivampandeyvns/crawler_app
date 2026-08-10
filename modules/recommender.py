import sqlite3
import joblib
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity


class RecommendationEngine:

    def __init__(self):

        self.conn = sqlite3.connect("data/news.db")

        self.df = pd.read_sql(
            "SELECT * FROM articles",
            self.conn
        )

        self.tfidf = joblib.load(
            "data/tfidf.pkl"
        )

        self.similarity = cosine_similarity(
            self.tfidf
        )

    def recommend(self, article_title, top_k=5):

        matches = self.df.index[
            self.df["title"] == article_title
        ]

        if len(matches) == 0:
            return pd.DataFrame()

        idx = matches[0]

        scores = list(
            enumerate(
                self.similarity[idx]
            )
        )

        scores = sorted(
            scores,
            key=lambda x: x[1],
            reverse=True
        )

        scores = scores[1:top_k+1]

        rows = []

        for index, score in scores:

            row = self.df.iloc[index].copy()

            row["similarity"] = round(score, 4)

            rows.append(row)

        return pd.DataFrame(rows)