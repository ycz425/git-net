import sqlite3


def get_repositories() -> list[dict]:
    con = sqlite3.connect('data/processed_data.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT id, full_name, stargazers_count FROM repositories')
    rows = cur.fetchall()

    result = []
    for row in rows:
        row = dict(row)
        row['id'] = f'repo_{row['id']}'
        result.append(row)

    return result


def get_forks() -> list[dict]:
    con = sqlite3.connect('data/processed/data.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT id, parent_id FROM repositories GROUP BY id, parent_id')
    rows = cur.fetchall()

    result = []
    for row in rows:
        row = dict(row)
        row['id'] = f'repo_{row['id']}'
        row['parent_id'] = f'repo_{row['parent_id']}' if row['parent_id'] else None
        result.append(row)
    
    return result


def get_users() -> list[dict]:
    con = sqlite3.connect('data/processed/data.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()

    result = []
    for row in rows:
        row = dict(row)
        row['id'] = f'user_{row['id']}'
        result.append(row)

    return result


def get_stars() -> list[dict]:
    con = sqlite3.connect('data/processed/data.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM stars')
    rows = cur.fetchall()

    result = []
    for row in rows:
        row = dict(row)
        row['user_id'] = f'user_{row['user_id']}'
        row['repo_id'] = f'repo_{row['repo_id']}'
        result.append(row)

    return result