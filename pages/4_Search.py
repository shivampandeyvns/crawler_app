import time
import streamlit as st

from modules.search_engine import SearchEngine
from modules.history import add, get
from modules.highlighter import highlight

st.set_page_config(page_title="Search", page_icon="🔍", layout="wide")

st.title("🔍 News Search Engine")

st.write(
    "Search articles using TF-IDF, BM25, Boolean, Phrase or Wildcard Search."
)

engine = SearchEngine()

query = st.text_input(
    "Enter Search Query",
    placeholder='Example: AI OR Healthcare'
)

method = st.selectbox(
    "Search Method",
    [
        "TF-IDF",
        "BM25",
        "Boolean",
        "Phrase",
        "Wildcard"
    ]
)

top_k = st.slider(
    "Top K Results",
    min_value=5,
    max_value=20,
    value=10
)

if st.button("🔍 Search"):

    if query.strip() == "":
        st.warning("Please enter a search query.")
        st.stop()

    start_time = time.time()

    if method == "TF-IDF":
        results = engine.tfidf_search(query, top_k)

    elif method == "BM25":
        results = engine.bm25_search(query, top_k)

    elif method == "Boolean":
        results = engine.boolean_search(query)

    elif method == "Phrase":
        results = engine.phrase_search(query)

    else:
        results = engine.wildcard_search(query)

    elapsed = round(time.time() - start_time, 3)

    add(query)

    st.success(
        f"Found {len(results)} result(s) in {elapsed} seconds."
    )

    if len(results) == 0:

        st.warning("No matching documents found.")

    else:

        for _, row in results.iterrows():

            title = row["title"] if row["title"] else "Untitled"

            with st.expander(f"📰 {title}"):

                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Source:** {row['source']}")
                    st.write(f"**Author:** {row['author']}")

                with col2:
                    st.write(f"**Published:** {row['published']}")

                    if "score" in row:
                        st.write(f"**Score:** {round(row['score'],4)}")

                preview = row["content"][:500] + "..."

                st.markdown(
                    highlight(preview, query),
                    unsafe_allow_html=True
                )

                if row["url"]:

                    st.link_button(
                        "🌐 Open Original Article",
                        row["url"]
                    )

st.divider()

st.subheader("🕒 Search History")

history = get()

if len(history) == 0:

    st.info("No searches performed yet.")

else:

    for item in history:

        st.write(
            f"**{item['time']}** — {item['query']}"
        )