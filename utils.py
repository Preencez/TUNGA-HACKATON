import requests
import re
import base64
import json

def parse_github_url(url):
    match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if match:
        return match.group(1), match.group(2)
    else:
        raise ValueError("Invalid GitHub URL")

def get_repo_files(user, repo, token, branch='main'):
    base_url = f"https://api.github.com/repos/{user}/{repo}/git/trees/{branch}?recursive=1"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()

    tree = response.json().get('tree', [])
    # Filter out .md and .txt files
    return [(item['path'], item['url']) for item in tree if item['type'] == 'blob' and not (item['path'].endswith('.md') or item['path'].endswith('.txt'))]

def get_file_content(url, token):
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    content = response.json().get('content', '')
    decoded_content = base64.b64decode(content)

    if response.json().get('encoding') == 'base64':
        try:
            return decoded_content.decode('utf-8')
        except UnicodeDecodeError:
            return "Error: Cannot decode content"
    else:
        return "Binary file or non-utf-8 content detected"

