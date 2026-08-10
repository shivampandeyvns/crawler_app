import streamlit as st
import plotly.express as px

from modules.search_engine import SearchEngine
from modules.evaluation import IREvaluator

import pandas as pd

st.title("📊 Information Retrieval Evaluation")

engine = SearchEngine()

evaluator = IREvaluator()

query = st.text_input("Evaluation Query")

method = st.selectbox(

    "Ranking Method",

    [

        "TF-IDF",

        "BM25"

    ]

)

if st.button("Evaluate"):

    if method == "TF-IDF":

        results = engine.tfidf_search(query, 20)

    else:

        results = engine.bm25_search(query, 20)

    retrieved = results.index.tolist()

    relevant = engine.relevant_documents(query)

    precision = evaluator.precision(retrieved, relevant)

    recall = evaluator.recall(retrieved, relevant)

    f1 = evaluator.f1(precision, recall)

    p5 = evaluator.precision_at_k(
        retrieved,
        relevant,
        5
    )

    r5 = evaluator.recall_at_k(
        retrieved,
        relevant,
        5
    )

    ap = evaluator.average_precision(
        retrieved,
        relevant
    )

    rr = evaluator.reciprocal_rank(
        retrieved,
        relevant
    )

    ndcg = evaluator.ndcg(
        retrieved,
        relevant
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Precision", round(precision, 3))
    c2.metric("Recall", round(recall, 3))
    c3.metric("F1", round(f1, 3))

    c1, c2, c3 = st.columns(3)

    c1.metric("Precision@5", round(p5, 3))
    c2.metric("Recall@5", round(r5, 3))
    c3.metric("MAP", round(ap, 3))

    st.metric("MRR", round(rr, 3))

    st.metric("NDCG", round(ndcg, 3))

    metrics = {

        "Metric":[

            "Precision",
            "Recall",
            "F1",
            "P@5",
            "R@5",
            "MAP",
            "MRR",
            "NDCG"

        ],

        "Score":[

            precision,
            recall,
            f1,
            p5,
            r5,
            ap,
            rr,
            ndcg

        ]

    }

    fig = px.bar(

        metrics,

        x="Metric",

        y="Score",

        color="Score",

        title="Evaluation Metrics"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Comparison of Ranking Methods")

    tfidf = engine.tfidf_search(query, 20)
    bm25 = engine.bm25_search(query, 20)

    retrieved_tfidf = tfidf.index.tolist()
    retrieved_bm25 = bm25.index.tolist()

    comparison = {
        "Metric": [
            "Precision",
            "Recall",
            "F1",
            "MAP",
            "MRR",
            "NDCG"
        ],
        "TF-IDF": [
            evaluator.precision(retrieved_tfidf, relevant),
            evaluator.recall(retrieved_tfidf, relevant),
            evaluator.f1(
                evaluator.precision(retrieved_tfidf, relevant),
                evaluator.recall(retrieved_tfidf, relevant)
            ),
            evaluator.average_precision(retrieved_tfidf, relevant),
            evaluator.reciprocal_rank(retrieved_tfidf, relevant),
            evaluator.ndcg(retrieved_tfidf, relevant)
        ],
        "BM25": [
            evaluator.precision(retrieved_bm25, relevant),
            evaluator.recall(retrieved_bm25, relevant),
            evaluator.f1(
                evaluator.precision(retrieved_bm25, relevant),
                evaluator.recall(retrieved_bm25, relevant)
            ),
            evaluator.average_precision(retrieved_bm25, relevant),
            evaluator.reciprocal_rank(retrieved_bm25, relevant),
            evaluator.ndcg(retrieved_bm25, relevant)
        ]
    }

    comparison_df = pd.DataFrame(comparison)

    st.dataframe(comparison_df)

    fig = px.bar(
        comparison_df,
        x="Metric",
        y=["TF-IDF", "BM25"],
        barmode="group",
        title="TF-IDF vs BM25 Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)