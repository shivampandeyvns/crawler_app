import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

st.title("📈 Performance Analytics")

conn = sqlite3.connect("data/news.db")

df = pd.read_sql(
    "SELECT * FROM articles",
    conn
)

if df.empty:

    st.warning("No articles found.")
    st.stop()

st.subheader("Corpus Statistics")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Articles",
    len(df)
)

c2.metric(
    "Sources",
    df["source"].nunique()
)

c3.metric(
    "Average Words",
    int(df["word_count"].mean())
)

st.divider()

st.subheader("Articles by Source")

source = df.groupby(
    "source"
).size().reset_index(name="Count")

fig = px.pie(
    source,
    names="source",
    values="Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Word Count Distribution")

fig = px.histogram(
    df,
    x="word_count",
    nbins=20
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Publication Timeline")

if "published" in df.columns:

    timeline = df.groupby(
        "published"
    ).size().reset_index(name="Articles")

    fig = px.line(
        timeline,
        x="published",
        y="Articles"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.subheader("Dataset Preview")

st.dataframe(df.head(20))