from langserve import add_routes
from fastapi import FastAPI
from chain import chain
from multi_inputs_chain import multi_input_chain

app = FastAPI()

add_routes(app, chain, path="/generate_post_content")
add_routes(app, multi_input_chain, path="/multi_inputs")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# poetry run python server.py
