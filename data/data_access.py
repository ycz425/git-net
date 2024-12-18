import sqlite3


def get_repositories() -> list[dict]:
    con = sqlite3.connect('data/processed_data.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT id, full_name, stargazers_count FROM repositories')
    rows = cur.fetchall()

    result = []
    for row in rows:
        result.append(dict(row))

    return result


def get_forks() -> list[dict]:
    con = sqlite3.connect('data/processed_data.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('SELECT id, parent_id FROM repositories GROUP BY id, parent_id')
    rows = cur.fetchall()

    result = []
    for row in rows:
        result.append(dict(row))
    
    return result

