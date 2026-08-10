import feedparser
import newspaper

from datetime import datetime

from modules.database import get_connection

from modules.utils import generate_hash

from modules.config import RSS_FEEDS


class NewsCrawler:

    def __init__(self):

        self.conn = get_connection()

    def crawl(self, selected_sources):

        cursor = self.conn.cursor()

        total = 0

        for source in selected_sources:

            feed = feedparser.parse(RSS_FEEDS[source])

            for item in feed.entries:

                try:

                    article = newspaper.Article(item.link)

                    article.download()

                    article.parse()

                    text = article.text

                    if len(text) < 200:
                        continue

                    hash_value = generate_hash(text)

                    cursor.execute(
                        "SELECT id FROM articles WHERE hash=?",
                        (hash_value,)
                    )

                    if cursor.fetchone():
                        continue

                    cursor.execute("""

                    INSERT OR IGNORE INTO articles(

                    title,

                    content,

                    summary,

                    source,

                    author,

                    published,

                    category,

                    url,

                    crawl_date,

                    word_count,

                    hash

                    )

                    VALUES(?,?,?,?,?,?,?,?,?,?,?)

                    """,

                    (

                    article.title,

                    text,

                    article.summary,

                    source,

                    ",".join(article.authors),

                    item.published if "published" in item else "",

                    "",

                    item.link,

                    datetime.now(),

                    len(text.split()),

                    hash_value

                    )

                    )

                    total += 1

                except:

                    continue

        self.conn.commit()

        return total