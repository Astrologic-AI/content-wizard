import asyncio
import os
import random
from datetime import datetime, timedelta

from langchain.prompts import ChatPromptTemplate
import pandas as pd
from langchain_core.messages import HumanMessage
from langchain_ollama.llms import OllamaLLM
from langchain_core.tools import tool
from geckoterminal_py import GeckoTerminalAsyncClient
import operator
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import START, END, StateGraph
from services.twitter_client import TwitterClient
from dotenv import load_dotenv

load_dotenv()
client = GeckoTerminalAsyncClient()
twitter_client = TwitterClient(base_url="http://localhost:3000")

agents = {
    "quantitative_analyst": {
        "model": OllamaLLM(model="llama3.2", temperature=0.2),
        "system_message": "You are a helpful assistant that generates a quantitative analysis of the current crypto market trends.",
        "prompt_message": "The available market data is: {pools}, generate a list of 10 sentences each containing a single fact with less than 20 words. The insights should include information about top performers, interesting ratios between volume and liquidity, notable market cap changes, and any other statistically significant metrics or patterns. Always start with the coin name with a $ sign and then the fact.",
    },
    "twitter_writer": {
        "model": OllamaLLM(model="llama3.2", temperature=0.7),
        "system_message": "You are Eminem rapper plus quantitative analyst that writes tweets with rap style about pumping coins. Write controversial and contrarian tweets that rhyme, is forbidden to use hashtags and is required to include numerical insights.",
        "prompt_message": "Write one single-sentence tweet with less than 100 characters about one coin, using only these market highlights: {facts} and is forbidden to talk about the same coin as in the previous tweets or use the same phrases: {previous_tweets}, h1 is last hour, h24 is last 24 hours. Always use $ before the coin name!"
    }
}

def get_agent_prompt_and_model(agent_name: str):
    agent = agents[agent_name]
    return ChatPromptTemplate.from_messages([
        ("system", agent["system_message"]),
        ("human", agent["prompt_message"]),
    ]), agent["model"]


class State(TypedDict):
    pools: Annotated[list, operator.add]
    previous_tweets: Annotated[list, operator.add]
    facts: Annotated[list, operator.add]

async def update_data(state: State) -> State:
    recent_tweets = await twitter_client.get_user_tweets("1274406877326172160")
    tweets = recent_tweets.get("data", [])
    tweets_text = [tweet.get("text", "") for tweet in tweets[-4:]]
    pools = await client.get_trending_pools_by_network("solana")
    pools["name"] = pools["name"].apply(lambda x: x.split("/")[0])
    pools["volume_liquidity_ratio"] = pd.to_numeric(pools["volume_usd_h24"]) / pd.to_numeric(pools["reserve_in_usd"])
    pools = pools[["name", 'price_change_percentage_h1', 'price_change_percentage_h24', 
                  'transactions_h1_buys', 'transactions_h1_sells', 'volume_usd_h24', 'volume_liquidity_ratio']]
    return {"pools": [pools.head(40)],
            "previous_tweets": tweets_text}

async def call_analyst(state: State, analyst_type: str, chunks: int = 2) -> State:
    pools = state["pools"][-1]
    step = len(pools) // chunks
    pool_chunks = [pools[i * step:(i+1) * step] for i in range(chunks)]
    
    analyst_prompt, analyst_model = get_agent_prompt_and_model(analyst_type)
    prompts = [analyst_prompt.format_messages(pools=chunk) for chunk in pool_chunks]
    model_tasks = [analyst_model.ainvoke(prompt) for prompt in prompts]
    facts = await asyncio.gather(*model_tasks)
    return {"facts": [facts]}

async def call_quantitative_analyst(state: State) -> State:
    return await call_analyst(state, "quantitative_analyst")

async def call_tweet_writer(state: State) -> State:
    analyst_prompt, analyst_model = get_agent_prompt_and_model("twitter_writer")
    prompt = analyst_prompt.format_messages(facts=state["facts"], previous_tweets=state["previous_tweets"])
    tweet = await analyst_model.ainvoke(prompt)
    await twitter_client.post_tweet(tweet.replace('"', ''))

builder = StateGraph(State)
builder.add_node("update_data", update_data)
builder.add_node("call_quantitative_analyst", call_quantitative_analyst)
builder.add_node("call_tweet_writer", call_tweet_writer)

builder.add_edge(START, "update_data")
builder.add_edge("update_data", "call_quantitative_analyst")
builder.add_edge("call_quantitative_analyst", "call_tweet_writer")
builder.add_edge("call_tweet_writer", END)

graph = builder.compile()

async def refresh_auth_task():
    while True:
        try:
            await twitter_client.refresh_auth()
            print(f"Auth refreshed at: {datetime.now()}")
        except Exception as e:
            print(f"Error refreshing auth: {e}")
        await asyncio.sleep(15 * 60)  # Sleep for 15 minutes

async def run_graph():
    inputs = {"facts": []}
    await graph.ainvoke(inputs)

async def main():
    # Create and start the refresh_auth task
    refresh_task = asyncio.create_task(refresh_auth_task())

    try:
        while True:
            await run_graph()
            wait_time = random.randint(40 * 60, 150 * 60)  # Random time between 15 and 45 minutes in seconds
            next_run = datetime.now() + timedelta(seconds=wait_time)
            print(f"Next run scheduled at: {next_run}")
            await asyncio.sleep(wait_time)
    except asyncio.CancelledError:
        # Cancel the refresh_auth task when the main task is cancelled
        refresh_task.cancel()
        await refresh_task
    except Exception as e:
        print(f"An error occurred in the main loop: {e}")
        refresh_task.cancel()
        await refresh_task
    finally:
        # Ensure the refresh_auth task is properly cancelled and cleaned up
        if not refresh_task.done():
            refresh_task.cancel()
            await refresh_task

if __name__ == "__main__":
    asyncio.run(main())
