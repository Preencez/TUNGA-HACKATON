from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

def generate_readme(api_key, repo_content):
    llm = OpenAI(api_key=api_key)

    prompt_template = PromptTemplate.from_template(
        '''
        You are the best writer of README files. 
        I will present the content of the files in a json format containing the name
        and the content of the file. Generate the README content in the correct markdown
        format. Here is the content of the whole repo: ```{text}```
        '''
    )

    formatted_prompt = prompt_template.format(text=repo_content)
    llm_chain = LLMChain(llm)
    return llm_chain(formatted_prompt)
