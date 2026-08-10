import streamlit as st
import plotly.express as px

from modules.ranker import PageRankEngine

st.title("⭐ PageRank Ranking")

st.write(
    """
    PageRank assigns an importance score to each article based on
    its connections with other similar articles in the corpus.
    """
)

if st.button("Calculate PageRank"):

    engine = PageRankEngine()

    df, graph = engine.calculate_pagerank()

    ranked = (
        df.sort_values(
            "pagerank",
            ascending=False
        )
        .reset_index(drop=True)
    )

    st.success("PageRank calculated successfully!")

    # -----------------------------
    # Graph Statistics
    # -----------------------------

    st.subheader("📊 Corpus Statistics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Articles",
        graph.number_of_nodes()
    )

    col2.metric(
        "Connections",
        graph.number_of_edges()
    )

    avg_degree = (
        sum(dict(graph.degree()).values())
        / graph.number_of_nodes()
    )

    col3.metric(
        "Average Degree",
        round(avg_degree, 2)
    )

    col4.metric(
        "Highest PageRank",
        round(ranked.iloc[0]["pagerank"], 4)
    )

    st.divider()

    # -----------------------------
    # Ranking Table
    # -----------------------------

    st.subheader("🏆 Top Ranked Articles")

    table = ranked[
        [
            "title",
            "source",
            "pagerank"
        ]
    ].head(20)

    table = table.rename(
        columns={
            "title": "Article",
            "source": "Source",
            "pagerank": "PageRank Score"
        }
    )

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # -----------------------------
    # Bar Chart
    # -----------------------------

    st.subheader("📈 Top 10 PageRank Scores")

    top10 = ranked.head(10)

    fig = px.bar(
        top10,
        x="pagerank",
        y="title",
        orientation="h",
        text="pagerank"
    )

    fig.update_traces(
        texttemplate="%{text:.4f}",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="PageRank Score",
        yaxis_title="Article",
        showlegend=False,
        height=600
    )

    fig.update_yaxes(
        autorange="reversed"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # -----------------------------
    # Interpretation
    # -----------------------------

    st.info("""
### Interpretation

• Articles with higher PageRank are considered more influential within the news corpus.

• The algorithm evaluates article importance based on graph connectivity rather than keyword frequency alone.

• Graph-based ranking complements TF-IDF and BM25 by identifying globally important documents.

• Such ranking can be used to improve search result ordering and recommendation quality.
""")