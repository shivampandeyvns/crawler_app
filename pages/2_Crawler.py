import streamlit as st

from modules.crawler import NewsCrawler

from modules.config import RSS_FEEDS

st.title("🌐 News Crawler")

st.write("Download articles from RSS feeds.")

selected = st.multiselect(

    "Choose News Sources",

    list(RSS_FEEDS.keys()),

    default=["BBC"]

)

if st.button("Start Crawling"):

    crawler = NewsCrawler()

    with st.spinner("Downloading Articles..."):

        total = crawler.crawl(selected)

    st.success(f"{total} articles added.")