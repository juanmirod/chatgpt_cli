import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get('GIST_TOKEN')


def upload(file_path, name='file', description=''):
    url = 'https://api.github.com/gists'
    headers = {'Authorization': f'token {token}'}

    with open(file_path, 'r') as file:
        data = {
            "description": description,
            "public": True,
            "files": {
                f"{name}.md": {
                    "content": file.read()
                }
            }
        }
    response = requests.post(url, headers=headers, json=data)
    gist_url = response.json()['html_url']
    print(f"Gist created at {gist_url}")
