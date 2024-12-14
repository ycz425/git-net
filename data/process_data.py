import sqlite3
import json


def _process_repositories(con_processed: sqlite3.Connection, con_raw: sqlite3.Connection) -> None:
    cur_processed = con_processed.cursor()
    cur_raw = con_raw.cursor()

    cur_raw.execute('SELECT * FROM repositories')
    for repo in cur_raw.fetchall():
        cur_processed.execute('INSERT INTO repositories VALUES (?, ?)', (repo[0], json.loads(repo[1])['name']))

    con_processed.commit()

    
def _process_users(con_processed: sqlite3.Connection, con_raw: sqlite3.Connection) -> None:
    cur_processed = con_processed.cursor()
    cur_raw = con_raw.cursor()

    cur_raw.execute('SELECT body FROM contributions')
    for user in cur_raw.fetchall():
        body = json.loads(user[0])
        cur_processed.execute('INSERT OR IGNORE INTO users VALUES (?, ?)', (body['id'], body['login']))

    con_processed.commit()


def _process_repositories_users(con_processed: sqlite3.Connection, con_raw: sqlite3.Connection) -> None:
    cur_processed = con_processed.cursor()
    cur_raw = con_raw.cursor()

    cur_raw.execute('SELECT repo_id, body FROM contributions')
    for user in cur_raw.fetchall():
        body = json.loads(user[1])
        cur_processed.execute(
            'INSERT INTO repositories_users VALUES (?, ?, ?)', 
            (user[0], body['id'], body['contributions'])
        )

    con_processed.commit()


def process_data(con_processed: sqlite3.Connection, con_raw: sqlite3.Connection) -> None:
    _process_repositories(con_processed, con_raw)
    _process_users(con_processed, con_raw)
    _process_repositories_users(con_processed, con_raw)


def create_tables(con: sqlite3.Connection) -> None:
    cur = con.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS repositories(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            login TEXT NOT NULL
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS repositories_users(
            repo_id INTEGER,
            user_id INTEGER,
            contributions INTEGER NOT NULL,
            PRIMARY KEY (repo_id, user_id)
            FOREIGN KEY (repo_id) REFERENCES repositories (id) ON DELETE CASCADE
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    con.commit()


if __name__ == '__main__':
    con_processed = sqlite3.connect('data/processed_data.db')
    con_raw = sqlite3.connect('data/raw_data.db')
    create_tables(con_processed)
    process_data(con_processed, con_raw)
