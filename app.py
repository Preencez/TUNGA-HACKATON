import streamlit as st
import json
from utils import parse_github_url, get_repo_files, get_file_content
from generate_readme import generate_readme

def main():
    st.title("GitHub README Generator")

    # User inputs
    repo_url = st.text_input("Enter the GitHub repository URL:")
    token = st.text_input("Enter your GitHub access token:", type="password")
    openai_api_key = st.text_input("Enter your OpenAI API key:", type="password")

    generate_button = st.button("Generate README")

    if generate_button and repo_url and token and openai_api_key:
        try:
            user, repo = parse_github_url(repo_url)
            file_data_pairs = get_repo_files(user, repo, token)
            file_contents = {}

            for file_name, url in file_data_pairs:
                content = get_file_content(url, token)
                file_contents[file_name] = content

            json_data = json.dumps(file_contents, indent=4)
            readme_content = generate_readme(openai_api_key, json_data)

            st.text_area("Generated README:", readme_content, height=300)

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
