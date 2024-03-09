# content-wizard


## content_generation

#### Description
Application that manages the content generation, receives some post properties and it will return generated content. We will serve the application as an api through HTTP protocol.

1. Next Iteration 
   1. GET/POST endpoint accepting  **date** , **post_idea** 
      1. We are accepting plane text, we would like to accept casted inputs and use them within our chain.
   2. Returns 3 variants of X(twitter) posts

- Generate prompt template optimized for content creation in X (Twitter), it should have a humman tone and leverage vectordb content (if needed)
- Inputs:
    - Post idea
    - Publishing Date
- Output:
    - Tweet proposal 1
    - Tweet proposal 2
    - Tweet proposal 3
  
We will follow [this approach](https://www.youtube.com/watch?v=dA1cHGACXCo&ab_channel=LangChain)

#### Keys 
How to get the key
* [OPENAI_API_KEY](https://platform.openai.com/api-keys)
* [EXA_API_KEY](https://dashboard.exa.ai/overview)
* [LANGCHAIN_API_KEY](https://smith.langchain.com/) 


