# from langchain.chains import LLMChain
import sys
print(sys.path)

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os
import openai
from dotenv import load_dotenv

# load_dotenv()
# openai.api_key = os.environ.get('OPENAI_API_KEY')

import openai

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

# content = """
 #from langchain.chains import LLMChain
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate

# def generate_readme(api_key, repo_content):
# llm = OpenAI(api_key=api_key)

# prompt_template = PromptTemplate.from_template(
# '''
# You are the best writer of README files. 
# I will present the content of the files in a json format containing the name
# and the content of the file. Generate the README content in the correct markdown
# format. Here is the content of the whole repo: ```{text}```
# '''
# )

# formatted_prompt = prompt_template.format(text=repo_content)
# llm_chain = LLMChain(llm)
# return llm_chain(formatted_prompt)

# """