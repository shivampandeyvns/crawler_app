import sqlite3

DATABASE = "data/news.db"

def get_connection():
    return sqlite3.connect(DATABASE)

def create_database():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS articles(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,

        content TEXT,

        summary TEXT,

        source TEXT,

        author TEXT,

        published TEXT,

        category TEXT,

        url TEXT UNIQUE,

        crawl_date TEXT,

        word_count INTEGER,

        hash TEXT UNIQUE

    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()