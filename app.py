import streamlit as st
import json
from utils import parse_github_url, get_repo_files, get_file_content, create_or_update_readme
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
    st.sidebar.markdown("This app assists in generating a README file for your GitHub repository.")
    st.sidebar.markdown("It utilizes OpenAI to analyze your repository files and create a README file.")
    st.sidebar.markdown("Follow the steps below to use the app:")

    steps = [
        "Enter the GitHub repository URL.",
        "Generate a GitHub access token (Make sure to give the appropriate permissions). [Learn how to generate an access token](https://docs.github.com/en/enterprise-server@3.6/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)",
        "Enter your GitHub access token.",
        "Generate an OpenAI API key. [Learn how to generate an API key](https://platform.openai.com/docs/quickstart?context=python)",
        "Enter your OpenAI API key.",
        "Click the 'Generate README' button.",
        "The README file is now created in your repo. Follow the link to view."
    ]

    for index, step in enumerate(steps, start=1):
        if index == 2:
            st.sidebar.markdown(f"{index}. {step}")
        elif index == 4:
            st.sidebar.markdown(f"{index}. {step}")
        else:
            st.sidebar.markdown(f"{index}. {step}")

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

            # Create or update the README in the GitHub repository
            response = create_or_update_readme(user, repo, token, readme_content)
            readme_url = response.get('content', {}).get('html_url', 'URL not available')

            st.success(f"README content generated and updated in the repository. You can view it [here]({readme_url}).")

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
