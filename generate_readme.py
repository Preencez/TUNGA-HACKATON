# from langchain.chains import LLMChain
import os
import openai
from dotenv import load_dotenv


def generate_readme(api_key, repo_content):
    openai.api_key = api_key

    formatted_prompt = f"Generate a comprehensive README with the correct markdown format for the following GitHub repository content:\n\n{repo_content}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a professional assistant skilled at generating README files from GitHub repository content provided."},
            {"role": "user", "content": formatted_prompt}
        ],
        max_tokens=10000
    )

    return response.choices[0].message['content'].strip()
