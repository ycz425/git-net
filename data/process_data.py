import sqlite3
import json


def process_repos(con_processed: sqlite3.Connection, con_raw: sqlite3.Connection) -> None:
    cur_processed = con_processed.cursor()
    cur_raw = con_raw.cursor()

    cur_raw.execute('SELECT * FROM repositories')
    for repo in cur_raw.fetchall():
        body = json.loads(repo[2])
        cur_processed.execute('INSERT OR IGNORE INTO repositories VALUES (?, ?, ?, ?)', (repo[0], repo[1], body['full_name'], body['stargazers_count']))

    con_processed.commit()


def process_users(con_processed: sqlite3.Connection, con_raw: sqlite3.Connection) -> None:
    cur_processed = con_processed.cursor()
    cur_raw = con_raw.cursor()

    cur_raw.execute('SELECT id, body FROM stargazers WHERE id IN(SELECT id FROM stargazers GROUP BY id HAVING COUNT(id) >= 2)')
    for user in cur_raw.fetchall():
        body = json.loads(user[1])
        cur_processed.execute('INSERT OR IGNORE INTO users VALUES (?, ?, ?)', (user[0], body['login'], body['avatar_url']))
       
    con_processed.commit()


def process_stars(con_processed: sqlite3.Connection, con_raw: sqlite3.Connection) -> None:
    cur_processed = con_processed.cursor()
    cur_raw = con_raw.cursor()

    cur_raw.execute('SELECT id, repo_id FROM stargazers WHERE id IN(SELECT id FROM stargazers GROUP BY id HAVING COUNT(id) >= 2)')
    for star in cur_raw.fetchall():
        cur_processed.execute('INSERT OR IGNORE INTO stars VALUES (?, ?)', (star[0], star[1]))

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

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            login TEXT NOT NULL,
            avatar_url TEXT NOT NULL
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS stars(
            user_id,
            repo_id,
            PRIMARY KEY (user_id, repo_id),
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (repo_id) REFERENCES repositories (id) ON DELETE CASCADE
        )
    ''')

    con.commit()


if __name__ == '__main__':
    con_processed = sqlite3.connect('data/processed_data.db')
    con_raw = sqlite3.connect('data/raw_data.db')
    create_table(con_processed)
    process_repos(con_processed, con_raw)
    process_users(con_processed, con_raw)
    process_stars(con_processed, con_raw)
