import sqlite3
import pandas as pd
import streamlit as st

from modules.recommender import RecommendationEngine

st.title("👍 Content-Based Recommendation System")

conn = sqlite3.connect("data/news.db")

df = pd.read_sql(
    "SELECT * FROM articles",
    conn
)

if df.empty:

    st.warning("No articles available.")

    st.stop()

title = st.selectbox(

    "Select an Article",

    sorted(df["title"])

)

top_k = st.slider(

    "Number of Recommendations",

    3,
    10,
    5

)

if st.button("Recommend"):

    engine = RecommendationEngine()

    recommendations = engine.recommend(
        title,
        top_k
    )

    if recommendations.empty:

        st.warning(
            "No recommendations found."
        )

    else:

        st.success(
            f"{len(recommendations)} recommendations found."
        )

        for _, row in recommendations.iterrows():

            with st.expander(row["title"]):

                st.write(
                    f"**Similarity Score:** {row['similarity']}"
                )

                st.write(
                    f"**Source:** {row['source']}"
                )

                st.write(
                    row["content"][:400] + "..."
                )

                if row["url"]:

                    st.link_button(
                        "Open Article",
                        row["url"]
                    )