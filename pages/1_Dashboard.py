import pandas as pd
import streamlit as st
import sqlite3

conn = sqlite3.connect("data/news.db")

df = pd.read_sql(
    "SELECT * FROM articles",
    conn
)

total_articles = len(df)

sources = df["source"].nunique()

words = df["word_count"].sum()

col1,col2,col3=st.columns(3)

col1.metric("Articles",total_articles)

col2.metric("Sources",sources)

col3.metric("Words",words)