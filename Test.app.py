import requests
import re
import base64
import json

def parse_github_url(url):
    """
    Extracts the username and repository name from a GitHub URL.
    """
    match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if match:
        return match.group(1), match.group(2)
    else:
        raise ValueError("Invalid GitHub URL")

def get_repo_files(user, repo, token, branch='main'):
    """
    Retrieves the file URLs and names from a given GitHub repository.
    """
    base_url = f"https://api.github.com/repos/{user}/{repo}/git/trees/{branch}?recursive=1"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()

    tree = response.json().get('tree', [])
    file_data = [(item['path'], item['url']) for item in tree if item['type'] == 'blob']
    return file_data

def get_file_content(url, token):
    """
    Retrieves the content of a file from its GitHub API URL. 
    Decodes from base64 and handles different file types.
    """
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    content = response.json().get('content', '')
    decoded_content = base64.b64decode(content)

    # Check if the file is likely to be a text file
    if response.json().get('encoding') == 'base64':
        try:
            # Try decoding as utf-8
            return decoded_content.decode('utf-8')
        except UnicodeDecodeError:
            # If utf-8 decoding fails, handle the error
            return "Error: Cannot decode content"
    else:
        # For binary files or other content types
        return "Binary file or non-utf-8 content detected"

def generate_readme(file_contents):
    """
    Generates a well-structured README based on the content of the files.
    """
    readme_content = "# Project README\n\n"
    readme_content += "Welcome to the project! Below is an overview of the files in this repository.\n\n"

    for file_name, content in file_contents.items():
        readme_content += f"## {file_name}\n\n"
        readme_content += "```python\n"
        readme_content += content
        readme_content += "\n```\n\n---\n"

    # Save to README file
    with open('README_generated.md', 'w', encoding='utf-8') as readme_file:
        readme_file.write(readme_content)

    print("README file has been successfully generated as README_generated.md.")
def main():
    repo_url = input("Enter the GitHub repository URL: ")
    token = input("Enter your GitHub access token: ")

    try:
        user, repo = parse_github_url(repo_url)
        file_data_pairs = get_repo_files(user, repo, token)
        file_contents = {}

        for file_name, url in file_data_pairs:
            content = get_file_content(url, token)
            file_contents[file_name] = content

        generate_readme(file_contents)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
