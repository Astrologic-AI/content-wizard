import os
from dotenv import load_dotenv
from datetime import date
from pathlib import Path
# from langchain.llms import Ollama #un comment for using Ollama
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
)
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_exa import ExaSearchRetriever
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

# Get the path to the root directory of your project
env_path = Path(__file__).resolve().parents[3] / '.env'
# Load environment variables from .env file
load_dotenv(dotenv_path=env_path)

# Access environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
exa_api_key = os.getenv("EXA_API_KEY")
langchain_tracing_v2 = os.getenv("LANCHAIN_TRACING_V2")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
langchain_project = os.getenv("LANGCHAIN_PROJECT")
langchain_endpoint = os.getenv("LANGCHAIN_ENDPOINT")

astro_domains_to_include = [
    "https://cafeastrology.com",
    "https://www.astrology.com",
    "https://www.astro-seek.com",
    "https://astrostyle.com",
    "https://www.astrologyzone.com"
]

retriever = ExaSearchRetriever(k=2,
                               domains_to_include=astro_domains_to_include,
                               #exclude_domains=["https://twitter.com/", "https://whattotweet.com/"],
                               use_autoprompt=True)
#  )

document_prompt = PromptTemplate.from_template(
    """
<source>
    <page_content>{page_content}</page_content>
</source>
"""
)

document_chain = (
        RunnableLambda(
            lambda document: {
                "page_content": document.page_content,
            }
        )
        | document_prompt
)

retrieval_chain = (
        retriever | document_chain.map() | (lambda docs: "\n".join([i.text for i in docs]))
)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert astrologist with a knack for crafting viral {platform} posts. Your responses are infused with astrological insights and written in a captivating manner.",
        ),
        (
            "human",
            """
            Sum up information from "content" to generate a text post to be published on {publish_date} in the platform : {platform}.

CONDITION I : The content should sound human written and with basic english. Use basic words. Mimic a human writing.
CONDITION II : ONLY USE INFORMATION FROM the given "context"
CONDITION  III : The length of the output has to be lower than {max_characters} characters.
 
 
<context>
{context}
</context>


""",
        ),
    ]
)

llm = ChatOpenAI(max_tokens=100, temperature=0.3)

today = date.today()

multi_input_chain = (
        {
            "context": itemgetter("info_to_search") | retrieval_chain,
            "description": itemgetter("description"),
            "platform": itemgetter("platform"),
            "publish_date": itemgetter("publish_date"),
            "title": itemgetter("title"),
            "max_characters": itemgetter("max_characters"),
        }
        | RunnablePassthrough.assign(context=itemgetter("context"))
        | {"response": generation_prompt | llm, "context": itemgetter("context")}
)

# todo: return a dictionary with the response .
