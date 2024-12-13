import requests
import json
import time
import os
from dotenv import load_dotenv


def fetch_repositories(num: int, token: str) -> list[dict]:
    URL = 'https://api.github.com/repositories'
    params = {'since': 0}
    headers = {'Authorization': f'Bearer {token}'}

    data = []
    while len(data) < num:
        response = requests.get(URL, params, headers=headers).json()

        if type(response) != list:
            print('Sleeping...')
            time.sleep(3600)
            continue

        for repo in response:
            data.append(repo)
            print(f'Fetched repository {len(data)}/{num}')
            if len(data) >= num:
                break
        
        params['since'] = data[-1]['id']

    return data


def add_contributors(data: list[dict], token: str) -> None:
    headers = {'Authorization': f'Bearer {token}'}
    for index, repo in enumerate(data):
        response = requests.get(repo['contributors_url'], headers=headers)

        while type(response) != list:
            print('Sleeping...')
            time.sleep(3600)
            response = requests.get(repo['contributors_url'])
        
        data['contributors'] = response.json()
        print(f'Add contributors for repository {index + 1}/{len(data)}')


if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('GITHUB_FINE_GRAINED_ACCESS_TOKEN')
    data = fetch_repositories(50000, TOKEN)
    add_contributors(data, TOKEN)

    with open('data/raw/repositories_raw_data.json', 'w') as file:
        json.dump(data, file, indent=4)

