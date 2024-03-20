from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Platform(Enum):
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    PINTEREST = "pinterest"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    BLOG = "blog"
    NEWSLETTER = "newsletter"
    OTHER = "other"


class Status(Enum):
    IDEA_GENERATED = "idea_generated"
    READY_TO_REVIEW = "ready_to_review"
    READY_TO_PUBLISH = "ready_to_publish"
    PUBLISHED = "published"


class PostIdea(BaseModel):
    notion_id: Optional[str] = None
    title: str
    publish_date: datetime
    platform: Platform
    description: str
    notes: Optional[str]
    status: Status


class ContentGenerated(BaseModel):
    notion_id: Optional[str] = None
    name: str
    post_idea_id: str
    text: str
    media: Optional[str] = None
    selected: bool
