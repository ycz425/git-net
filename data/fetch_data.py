import requests
import json
import time
import os
import sqlite3
from dotenv import load_dotenv


def fetch_data(token: str, con: sqlite3.Connection) -> None:
    URL = 'https://api.github.com/search/repositories'
    NUM_REPO = 1000
    params = {'q': 'stars:>1000 is:public', 'sort': 'stars', 'order': 'desc', 'per_page': 100, 'page': 1}
    headers = {'Authorization': f'Bearer {token}'}

    count = 0

    cur = con.cursor()
    while count < NUM_REPO:
        response = requests.get(URL, params, headers=headers)

        if response.status_code != 200:
            print(f'Sleeping... (in fetch_data)')
            time.sleep(70)
            continue

        response = response.json()

        for repo in response['items']:
            cur.execute('INSERT INTO repositories VALUES (?, ?)', (repo['id'], json.dumps(repo)))
            success = _fetch_contributions(repo, token, con)
            if not success:
                cur.execute('DELETE FROM repositories WHERE id = ?', (repo['id'],))
                print(f'[{count + 1}/{NUM_REPO}] Failed to fetch data for {repo['full_name']} ')
            else:
                print(f'[{count + 1}/{NUM_REPO}] Fetched repository {repo['full_name']}')

            count += 1
            if count >= NUM_REPO:
                break
        
        params['page'] += 1

    con.commit()


def _fetch_contributions(repo: dict, token: str, con: sqlite3.Connection) -> bool:
    headers = {'Authorization': f'Bearer {token}'}
    params = {'anon': 0, 'per_page': 100, 'page': 1}
    cur = con.cursor()

    count = 0

    while True:
        response = requests.get(repo['contributors_url'], params, headers=headers)
        if response.status_code != 200 and response.json()['message'] == 'The history or contributor list is too large to list contributors for this repository via the API.':
            return False
        
        if response.status_code != 200:
            print(f'Sleeping... (in _fetch_contributions)')
            time.sleep(300)
            continue
    
        response = response.json()

        for contributor in response:
            cur.execute(
                'INSERT INTO contributions (repo_id, body) VALUES (?, ?)',
                (repo['id'], json.dumps(contributor))
            )
            count += 1

        params['page'] += 1

        if count >= 500 or len(response) == 0:
            break

    return True

        
def create_tables(con: sqlite3.Connection) -> None:
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS repositories(
                id INTEGER PRIMARY KEY,
                body TEXT NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS contributions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repo_id INTEGER NOT NULL,
            body TEXT NOT NULL,
            FOREIGN KEY (repo_id) REFERENCES repositories (id) ON DELETE CASCADE
        )
    ''')

    con.commit()


if __name__ == '__main__':
    response = requests.get('https://api.github.com/repositories')
    load_dotenv()
    TOKEN = os.getenv('GITHUB_FINE_GRAINED_ACCESS_TOKEN')
    
    con = sqlite3.connect('data/raw_data.db')
    create_tables(con)
    fetch_data(TOKEN, con)
