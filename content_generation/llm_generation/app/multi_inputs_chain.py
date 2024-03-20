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


retriever = ExaSearchRetriever(k=3, highlights=True)

document_prompt = PromptTemplate.from_template(
    """
<source>
    <url>{url}</url>
    <highlights>{highlights}</highlights>
</source>
"""
)

document_chain = (
    RunnableLambda(
        lambda document: {
            "highlights": document.metadata["highlights"],
            "url": document.metadata["url"],
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
Step 1: Look up astrological information for the date {publish_date}. This should include details about planetary positions, sign ascendants, and solar activity. Please base your response on scientifically-backed information.

Step 2: Write an engaging  post for "platform" based on the following "description" and "title"  and the astrological insights obtained in Step 1:

CONDITION : Your output can not be longer than  "max_characters". 

<max_characters>
{max_characters}
</max_characters>


<Platform>
{platform}
</Platform>

<title> : 
{title}
</title>

<description> : 
{description}
</description>
---
Astrological Insights:
- Planetary Positions
- Sign Ascendants
- Solar Activity
<context>
{context}
</context>

OUTPUT: Only return the {platform} post content as text
""",
        ),
    ]
)

# llm = Ollama(model="llama2") #un comment to use Ollama instead of ChatOpenAI
llm = ChatOpenAI()


today = date.today()

multi_input_chain = (
    {
        "context": itemgetter("description") | retrieval_chain,
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
