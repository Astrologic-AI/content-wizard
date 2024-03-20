import httpx


class TwitterClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def post_tweet(self, tweet: str):
        url = self.base_url + "/api/twitter/tweet/post"
        response = await self.client.post(url, json={"text": tweet})
        return response.json()
