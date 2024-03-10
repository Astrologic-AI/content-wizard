# %%
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
from pathlib import Path
from langchain.prompts import ChatPromptTemplate

#### Environment variables ####
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
openai_api_key = os.getenv("OPENAI_API_KEY")
langchain_tracing_v2 = os.getenv("LANCHAIN_TRACING_V2")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
langchain_project = os.getenv("LANGCHAIN_PROJECT")
langchain_endpoint = os.getenv("LANGCHAIN_ENDPOINT")

# Config
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
output_parser = StrOutputParser()

# Prompts & Chains
text_post_content_from_post_idea = "Based on astrology facts for today, craft an engaging tweet using the following outline: {post_idea}. Be sure to incorporate relevant scientific facts into your tweet. Limit your post to 256 characters. Conclude with a compelling call to action."
prompt_post_content_from_post_idea = ChatPromptTemplate.from_template(
    text_post_content_from_post_idea
)

content_generation_chain = prompt_post_content_from_post_idea | llm | StrOutputParser()

system_prompt = ChatPromptTemplate.from_template(
    "act as expert social media content creator"
)
endpoint_chain = (
    {"context": content_generation_chain, "post_idea": RunnablePassthrough()}
    | system_prompt
    | llm
    | output_parser
)
# %%
from datetime import date

if __name__ == "__main__":
    post_date = str(date.today())
    result = endpoint_chain.invoke(
        {"post_idea": "How the moon will impact love of people", "post_date": post_date}
    )
    print(result)

# %%
