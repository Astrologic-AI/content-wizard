from langserve import add_routes
from fastapi import FastAPI
from chain import chain

app = FastAPI()

add_routes(app, chain, path="/generate_post_content")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# poetry run python indexing.py
