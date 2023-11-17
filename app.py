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

    # Additional information about the app in the sidebar
    st.sidebar.image("https://images.unsplash.com/photo-1546776310-eef45dd6d63c?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cm9ib3R8ZW58MHx8MHx8fDA%3D")
    st.sidebar.title("About the App")
    st.sidebar.markdown("This app generates a README file for your GitHub repository.")
    st.sidebar.markdown("It uses OpenAI to analyze your repository files and create a summary.")
    st.sidebar.markdown("Follow the steps below to use the app:")
    st.sidebar.markdown("1. Enter the GitHub repository URL.")
    st.sidebar.markdown("2. Enter your GitHub access token.")
    st.sidebar.markdown("3. Enter your OpenAI API key.")
    st.sidebar.markdown("4. Click the 'Generate README' button.")
    st.sidebar.markdown("5. Review the generated README then copy and paste the result in your README.md file.")

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
            st.markdown("Copy the above content and paste it into your README file.")

            st.success("README content generated successfully. Please copy and paste it into your repository.")

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
