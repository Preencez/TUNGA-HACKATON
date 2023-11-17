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
    st.sidebar.image("https://th.bing.com/th/id/OIP.APmJvXP1CyR94wFUG8VgKwHaGh?rs=1&pid=ImgDetMain")
    st.sidebar.title("About the App")
    st.sidebar.markdown("This app generates a README file for your GitHub repository.")
    st.sidebar.markdown("It uses OpenAI to analyze your repository files and create a summary.")
    st.sidebar.markdown("Follow the steps below to use the app:")
    st.sidebar.markdown("1. Enter the GitHub repository URL.")
    st.sidebar.markdown("2. Enter your GitHub access token.")
    st.sidebar.markdown("3. Enter your OpenAI API key.")
    st.sidebar.markdown("4. Click the 'Generate README' button.")
    st.sidebar.markdown("5. Review the generated README in the main panel.")

     # Display image above the generated README content
    #t.image("https://th.bing.com/th/id/OIP.APmJvXP1CyR94wFUG8VgKwHaGh?rs=1&pid=ImgDetMain")

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

            # Save the generated README to a file
            with open("generated_readme.md", "w", encoding="utf-8") as readme_file:
                readme_file.write(readme_content)

            st.text_area("Generated README:", readme_content, height=300)
            st.markdown("Copy the above content and paste it into your README file.")

<<<<<<< HEAD
            user, repo = parse_github_url(repo_url)
            readme_file_name = find_next_readme_name(user, repo, token)
            create_commit_readme(user, repo, token, readme_file_name, readme_content)

            st.success(f"README file '{readme_file_name}' successfully created in the repository.")
            st.success(f"Generated README saved to 'generated_readme.md'.")
=======
            st.success("README content generated successfully. Please copy and paste it into your repository.")
>>>>>>> d61be2e5be9300921ba0c94e4ce36df19e4394f8

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
