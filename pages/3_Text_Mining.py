import streamlit as st

import sqlite3

import pandas as pd

from modules.preprocess import TextPreprocessor

from modules.indexer import IndexBuilder

from modules.visualization import wordcloud_plot

from modules.profiler import DocumentProfiler

from modules.keywords import KeywordExtractor

st.title("🧹 Text Mining")

conn=sqlite3.connect("data/news.db")

df=pd.read_sql(

    "SELECT * FROM articles",

    conn

)

if df.empty:

    st.warning("No articles available.")

    st.stop()

text=" ".join(df["content"])

if st.button("Run NLP Pipeline"):

    processor=TextPreprocessor()

    processed=processor.preprocess(text)

    IndexBuilder().build()

    st.success("Index Built")

    st.subheader("Document Profile")

    profile=DocumentProfiler().profile(text)

    st.json(profile)

    st.subheader("Top Keywords")

    keywords=KeywordExtractor().extract(

        processed["clean_text"]

    )

    st.dataframe(keywords)

    st.subheader("Word Cloud")

    fig=wordcloud_plot(

        processed["clean_text"]

    )

    st.pyplot(fig)

    st.subheader("Preprocessing Comparison")

    comparison = pd.DataFrame({

    "Stage": [
        "Original",
        "After Cleaning",
        "After Stopword Removal",
        "After Lemmatization"
    ],

    "Word Count": [
        len(text.split()),
        len(processor.clean(text).split()),
        len(processed["tokens"]),
        len(processed["lemmas"])
    ]

    })

    st.dataframe(comparison)

    st.bar_chart(
        comparison.set_index("Stage")
    )