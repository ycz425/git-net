import sqlite3
import json


def process_data(con_processed: sqlite3.Connection, con_raw: sqlite3.Connection) -> None:
    cur_processed = con_processed.cursor()
    cur_raw = con_raw.cursor()

    cur_raw.execute('SELECT * FROM repositories')
    for repo in cur_raw.fetchall():
        body = json.loads(repo[2])
        cur_processed.execute('INSERT INTO repositories VALUES (?, ?, ?, ?)', (repo[0], repo[1], body['full_name'], body['stargazers_count']))

    con_processed.commit()


def create_table(con: sqlite3.Connection) -> None:
    cur = con.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS repositories(
            id INTEGER PRIMARY KEY,
            parent_id INTEGER,
            full_name TEXT NOT NULL,
            stargazers_count INTEGER NOT NULL,
            FOREIGN KEY (parent_id) REFERENCES repositories (id) ON DELETE CASCADE
        )
    ''')

    con.commit()


if __name__ == '__main__':
    con_processed = sqlite3.connect('data/processed_data.db')
    con_raw = sqlite3.connect('data/raw_data.db')
    create_table(con_processed)
    process_data(con_processed, con_raw)
