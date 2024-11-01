import httpx


class TwitterClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def refresh_auth(self):
        url = self.base_url + "/api/twitter/refreshAuth"
        response = await self.client.get(url)
        return response.json()

    async def get_me(self):
        url = self.base_url + "/api/twitter/me"
        response = await self.client.get(url)
        return response.json()

    async def post_tweet(self, tweet: str):
        url = self.base_url + "/api/twitter/post"
        response = await self.client.post(url, json={"text": tweet})
        return response.json()
    
    async def delete_tweet(self, tweet_id: str):
        url = self.base_url + f"/api/twitter/delete-tweet/{tweet_id}"
        response = await self.client.post(url)
        return response.json()

    async def get_user_tweets(self, user_id: str):
        url = self.base_url + f"/api/twitter/tweets-by-user/{user_id}"
        response = await self.client.get(url)
        return response.json()
    
    async def search_tweets(self, query: str):
        url = self.base_url + f"/api/twitter/search"
        response = await self.client.get(url, params={"query": query})
        return response.json()
