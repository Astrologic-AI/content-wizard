import os
from dotenv import load_dotenv
from datetime import date

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

# Load environment variables from .env file
load_dotenv()

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
Step 1: Look up astrological information for the date {post_date}. This should include details about planetary positions, sign ascendants, and solar activity. Please base your response on scientifically-backed information.

Step 2: Write an engaging  post for "platform" based on the following "post_idea_description" and "post_idea_title"  and the astrological insights obtained in Step 1:

<Platform>
{platform}
</Platform>

<post_idea_title> : 
{post_idea_title}
</post_idea_title>

<post_idea_description> : 
{post_idea_description}
</post_idea_description>
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
        "context": itemgetter("post_idea_description") | retrieval_chain,
        "post_idea_description": itemgetter("post_idea_description"),
        "platform": itemgetter("platform"),
        "post_date": itemgetter("post_date"),
        "post_idea_title": itemgetter("post_idea_title"),
    }
    | RunnablePassthrough.assign(context=itemgetter("context"))
    | {"response": generation_prompt | llm, "context": itemgetter("context")}
)

#todo: return a dictionary with the response .