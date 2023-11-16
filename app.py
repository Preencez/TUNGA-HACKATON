import streamlit as st
from utils import parse_github_url, get_repo_files, get_file_content, find_next_readme_name, create_commit_readme
from generate_readme import generate_readme
import json

def main():
    st.title("GitHub README Generator")

    # User inputs
    repo_url = st.text_input("Enter the GitHub repository URL:")
    token = st.text_input("Enter your GitHub access token:", type="password")
    openai_api_key = st.text_input("Enter your OpenAI API key:", type="password")

    generate_button = st.button("Generate README")

    if generate_button and repo_url and token and openai_api_key:
        try:
            # Extract user and repo from the URL
            user, repo = parse_github_url(repo_url)

            # Get files from the repo
            file_data = get_repo_files(user, repo, token)
            
            # Prepare content for README generation
            repo_content = {}
            for file_name, file_url in file_data:
                file_content = get_file_content(file_url, token)
                repo_content[file_name] = file_content

            # Generate README content
            json_data = json.dumps(repo_content, indent=4)
            readme_content = generate_readme(openai_api_key, json_data)

            # Display generated README
            st.text_area("Generated README:", readme_content, height=300)

            # Find a suitable name for the README file
            readme_file_name = find_next_readme_name(user, repo, token)

            # Commit the README file to the repo
            create_commit_readme(user, repo, token, readme_file_name, readme_content)

            st.success(f"README file '{readme_file_name}' successfully created in the repository.")

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
