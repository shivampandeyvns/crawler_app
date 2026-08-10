import sqlite3
import joblib
import pandas as pd
import networkx as nx

from sklearn.metrics.pairwise import cosine_similarity


class PageRankEngine:

    def __init__(self):

        self.conn = sqlite3.connect("data/news.db")

        self.df = pd.read_sql(
            "SELECT * FROM articles",
            self.conn
        )

        self.tfidf = joblib.load(
            "data/tfidf.pkl"
        )

    def calculate_pagerank(self):

        similarity = cosine_similarity(self.tfidf)

        graph = nx.Graph()

        for i in range(len(self.df)):
            graph.add_node(i)

        TOP_NEIGHBOURS = 5

        for i in range(len(self.df)):

            similarities = []

            for j in range(len(self.df)):

                if i != j:

                    similarities.append(
                        (
                            j,
                            similarity[i][j]
                        )
                    )

            similarities.sort(
                key=lambda x: x[1],
                reverse=True
            )

            for neighbour, score in similarities[:TOP_NEIGHBOURS]:

                if score > 0.20:

                    graph.add_edge(
                        i,
                        neighbour,
                        weight=float(score)
                    )

                scores = nx.pagerank(
                    graph,
                    weight="weight"
                )

                self.df["pagerank"] = self.df.index.map(scores)

                self.df["pagerank"] = (
                    self.df.index
                    .map(scores)
                    .fillna(0)
                )

                return self.df, graph