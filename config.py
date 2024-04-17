import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("TELEGRAM_TOKEN")
NOTION_SERVICE_BASE_URL = os.environ.get("NOTION_SERVICE_BASE_URL")
TWITTER_SERVICE_BASE_URL = os.environ.get("TWITTER_SERVICE_BASE_URL")
MAX_CONTENT_GENERATION_BY_POST_IDEA = int(os.environ.get("MAX_CONTENT_GENERATED_BY_POST_IDEA", 3))
GROUP_CHAT_ID = int(os.environ.get("GROUP_CHAT_ID", -4107698917))
