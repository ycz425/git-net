import requests
import json
import time
import os
import sqlite3
from dotenv import load_dotenv


def fetch_forks(url: str, params: dict, token: str, parent_id: int, con: sqlite3.Connection, num: int, depth: int) -> bool:
    headers = {'Authorization': f'Bearer {token}'}
    cur = con.cursor()

    count = 0
    while count < num:
        response = requests.get(url, params, headers=headers)

        if response.status_code in {500, 404}:
            print(f'[Remaining depth: {depth}] [{count + 1}/{num}] Fork fetch failed: {url}')
            return False
        
        if response.status_code != 200:
            print('Sleeping... (5 min)')
            time.sleep(300)
            continue

        response = response.json()
        if 'items' in response:
            response = response['items']

        if len(response) == 0:
            print(f'[Remaining depth: {depth}] Found no forks: {url}')
            break

        for fork in response:
            if depth == 0 or fetch_forks(
                url=fork['forks_url'],
                params={'sort': 'stargazers', 'per_page': 100, 'page': 1},
                token=token,
                parent_id=fork['id'],
                con=con,
                num=num,
                depth=depth - 1
            ):
                cur.execute('INSERT OR IGNORE INTO repositories VALUES (?, ?, ?)', (fork['id'], parent_id, json.dumps(fork)))
                count += 1
                print(f'[Remaining depth: {depth}] [{count}/{num}] Fork fetched successfully: {fork['full_name']}')
                if count >= num:
                    break

        params['page'] += 1
    
    con.commit()
    return True
        

def fetch_stargazers(con: sqlite3.Connection, token: str, num: int):
    headers = {'Authorization': f'Bearer {token}'}
    cur = con.cursor()

    cur.execute('SELECT id, body FROM repositories')
    repos = cur.fetchall()

    for index, repo in enumerate(repos):
        params = {'per_page': 100, 'page': 1}
        count = 0
        repo_id = repo[0]
        body = json.loads(repo[1])
        while count < num:
            response = requests.get(body['stargazers_url'], params, headers=headers)

            if response.status_code in {500, 404} or len(response.json()) == 0:
                print(f'[Repo: {index + 1}/{len(repos)}] Stargazer fetch failed or response was empty')
                break

            if response.status_code != 200:
                print(response.json())
                print('Sleeping... (5 min)')
                time.sleep(300)
                continue

            response = response.json()

            for stargazer in response:
                cur.execute('INSERT OR IGNORE INTO stargazers VALUES (?, ?, ?)', (stargazer['id'], repo_id, json.dumps(stargazer)))
                count += 1
                print(f'[Repo: {index + 1}/{len(repos)}] [Stargazer: {count}/{num}] Stargazer fetched successfully: {stargazer['login']}')
                if count >= num:
                    break
            
            params['page'] += 1

    con.commit()


def create_table(con: sqlite3.Connection) -> None:
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS repositories(
            id INTEGER PRIMARY KEY,
            parent_id INTEGER,
            body TEXT NOT NULL,
            FOREIGN KEY (parent_id) REFERENCES repositories (id) ON DELETE CASCADE
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS stargazers(
            id INTEGER,
            repo_id INTEGER,
            body TEXT NOT NULL,
            PRIMARY KEY (id, repo_id),
            FOREIGN KEY (repo_id) REFERENCES repositories (id) ON DELETE CASCADE
        )
    ''')

    con.commit()


if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('GITHUB_FINE_GRAINED_ACCESS_TOKEN')
    
    con = sqlite3.connect('data/raw/data.db')
    create_table(con)
    fetch_forks(
        url='https://api.github.com/search/repositories',
        params={'q': 'stars:>1000 is:public', 'sort': 'forks', 'order': 'desc', 'per_page': 100, 'page': 1},
        token=TOKEN,
        parent_id=None,
        con=con,
        num=10,
        depth=3
    )

    fetch_stargazers(con=con, token=TOKEN, num=1000)
