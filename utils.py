import requests
import re
import base64
import json

def parse_github_url(url):
    match = re.search(r"github\.com/([^/]+)/([^/]+)(?:/tree|/blob)/([^/]+)", url)
    if match:
        return match.group(1), match.group(2), match.group(3)
    else:
        # Return user, repo, and a default branch if not specified
        return None, None, 'main'

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

def create_readme_in_branch(user, repo, token, content, branch='main'):
    file_name, _ = get_unique_readme_name(user, repo, token, branch)
    file_path = f"{file_name}.md"
    message = f"Create {file_path}"
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    # Check if file exists and get its sha
    sha = get_file_sha(user, repo, token, file_path, branch)
    if sha:
        message = f"Update {file_path}"

    data = {
        "message": message,
        "content": encoded_content,
        "branch": branch
    }

    if sha:
        data['sha'] = sha

    url = f"https://api.github.com/repos/{user}/{repo}/contents/{file_path}"
    headers = {'Authorization': f'token {token}'}
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()

def get_unique_readme_name(user, repo, token, branch):
    files = get_repo_files(user, repo, token, branch)
    base_name = "aiREADME"
    extension = ".md"
    index = 0

    # Generate unique file name
    while any(f"{base_name}{index if index else ''}{extension}" in file for file, _ in files):
        index += 1

    file_name = f"{base_name}{index if index else ''}"

    return file_name, False

def get_file_sha(user, repo, token, file_path, branch):
    url = f"https://api.github.com/repos/{user}/{repo}/contents/{file_path}?ref={branch}"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('sha')
    return None


