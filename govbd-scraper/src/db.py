import sqlite3

def initialize_database(db_name='gov_websites.db'):
    """Initialize the SQLite database and create the websites table."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE
        )
    ''')
    conn.commit()
    return conn, cursor

def save_url(cursor, url):
    """Save a unique URL to the database."""
    try:
        cursor.execute('INSERT OR IGNORE INTO websites (url) VALUES (?)', (url,))
    except Exception as e:
        print(f"Error saving {url} to database: {e}")