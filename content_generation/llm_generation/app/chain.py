import os
from dotenv import load_dotenv

# from langchain.llms import Ollama #un comment for using Ollama
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
    RunnableParallel,
)
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_exa import ExaSearchRetriever
from langchain_core.output_parsers import StrOutputParser


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
            "You are an expert astrologist with a knack for crafting viral Twitter posts. Your responses are infused with astrological insights and written in a captivating manner.",
        ),
        (
            "human",
            """
Please  base your response in the information present in the sources. TASK: Write an engaging twitter content based on the following query. The tweet should be 255 characters lengh max :
     
Query: {query}
---
<context>
{context}
</context>
""",
        ),
    ]
)

# llm = Ollama(model="llama2") #un comment to use Ollama instead of ChatOpenAI
llm = ChatOpenAI()

chain = (
    RunnableParallel(
        {
            "query": RunnablePassthrough(),
            "context": retrieval_chain,
        }
    )
    | generation_prompt
    | llm
    | StrOutputParser()
).with_types(input_type=str)
