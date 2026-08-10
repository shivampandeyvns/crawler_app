import sqlite3
import joblib
import pandas as pd
import re

from sklearn.metrics.pairwise import cosine_similarity


class SearchEngine:

    def __init__(self):

        self.conn = sqlite3.connect("data/news.db")

        self.df = pd.read_sql(
            "SELECT * FROM articles",
            self.conn
        )

        # Replace missing values
        self.df = self.df.fillna("")

        try:
            self.vectorizer = joblib.load("data/vectorizer.pkl")
            self.tfidf = joblib.load("data/tfidf.pkl")
            self.bm25 = joblib.load("data/bm25.pkl")
        except FileNotFoundError:
            raise Exception(
                "Search indexes not found.\n"
                "Please run the Text Mining page first."
            )

    ####################################################
    # TF-IDF SEARCH
    ####################################################

    def tfidf_search(self, query, k=10):

        query_vector = self.vectorizer.transform([query])

        scores = cosine_similarity(
            query_vector,
            self.tfidf
        )[0]

        result = self.df.copy()

        result["score"] = scores

        result = result.sort_values(
            by="score",
            ascending=False
        )

        result = result[result["score"] > 0]

        return result.head(k)

    ####################################################
    # BM25 SEARCH
    ####################################################

    def bm25_search(self, query, k=10):

        scores = self.bm25.get_scores(
            query.lower().split()
        )

        result = self.df.copy()

        result["score"] = scores

        result = result.sort_values(
            by="score",
            ascending=False
        )

        result = result[result["score"] > 0]

        return result.head(k)

    ####################################################
    # BOOLEAN SEARCH
    ####################################################

    def boolean_search(self, query):

        query_upper = query.upper()

        if " AND " in query_upper:

            left, right = query_upper.split(" AND ")

            mask = (

                self.df["content"].str.contains(
                    left,
                    case=False,
                    na=False
                )

                &

                self.df["content"].str.contains(
                    right,
                    case=False,
                    na=False
                )

            )

            result = self.df[mask].copy()

            result["score"] = 1.0

            return result

        elif " OR " in query_upper:

            left, right = query_upper.split(" OR ")

            mask = (

                self.df["content"].str.contains(
                    left,
                    case=False,
                    na=False
                )

                |

                self.df["content"].str.contains(
                    right,
                    case=False,
                    na=False
                )

            )

            result = self.df[mask].copy()

            result["score"] = 1.0

            return result

        elif " NOT " in query_upper:

            left, right = query_upper.split(" NOT ")

            mask = (

                self.df["content"].str.contains(
                    left,
                    case=False,
                    na=False
                )

                &

                ~

                self.df["content"].str.contains(
                    right,
                    case=False,
                    na=False
                )

            )

            result = self.df[mask].copy()

            result["score"] = 1.0

            return result

        return self.tfidf_search(query)

    ####################################################
    # PHRASE SEARCH
    ####################################################

    def phrase_search(self, phrase):

        phrase = phrase.replace('"', "")

        mask = self.df["content"].str.contains(
            phrase,
            case=False,
            na=False
        )

        result = self.df[mask].copy()

        result["score"] = 1.0

        return result

    ####################################################
    # WILDCARD SEARCH
    ####################################################

    def wildcard_search(self, pattern):

        prefix = pattern.replace("*", "")

        regex = rf"\b{re.escape(prefix)}\w*"

        mask = self.df["content"].str.contains(
            regex,
            case=False,
            regex=True,
            na=False
        )

        result = self.df[mask].copy()

        result["score"] = 1.0

        return result

    ####################################################
    # RELEVANT DOCUMENTS
    ####################################################

    def relevant_documents(self, query):

        words = query.lower().split()

        relevant = []

        for idx, row in self.df.iterrows():

            text = row["content"].lower()

            if any(word in text for word in words):

                relevant.append(idx)

        return relevant

    ####################################################
    # SEARCH SUGGESTIONS
    ####################################################

    def suggestions(self, prefix, limit=5):

        titles = self.df["title"].dropna().tolist()

        suggestions = []

        prefix = prefix.lower()

        for title in titles:

            if title.lower().startswith(prefix):

                suggestions.append(title)

        return suggestions[:limit]