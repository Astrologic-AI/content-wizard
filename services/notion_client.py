from services.models import Status, PostIdea, ContentGenerated
import httpx


class NotionClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def get_all_post_ideas(self):
        url = self.base_url + "/postIdeas"
        post_ideas = await self.client.get(url)
        return [PostIdea(**post_idea) for post_idea in post_ideas.json()]

    async def get_all_post_ideas_by_status(self, status: Status):
        post_ideas = await self.get_all_post_ideas()
        return [post_idea for post_idea in post_ideas if post_idea.status == status]

    async def get_content_generated_by_post_idea(self, post_idea_id: str):
        url = self.base_url + "/contentGenerated"
        content_generated = await self.client.get(url=url, params={"post_idea_id": post_idea_id})

    async def add_content_generated(self, content_generated: ContentGenerated):
        url = self.base_url + "/contentGenerated"
        response = await self.client.post(url, json=content_generated.dict())
        return response.json()
