import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, PicklePersistence

from config import TOKEN
from content_planning import handle_content_planning
from content_summary import generate_content_summary
from utils import connect_to_content_manager_api

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start the conversation and display the main menu."""
    reply_text = """
🚀 **Welcome to ContentWizard!** Your AI assistant for social media content creation and scheduling.

🎛️ Quick Commands:

🔸 `/content_planning`: Interact with an AI agent to create post ideas.
🔸 `/content_summary`: Summarize available content and identify opportunities.

🔍 Need help? Type `/help` for assistance.

Let's make your social media management magical with ContentWizard!
"""
    await update.message.reply_text(reply_text, parse_mode="MarkdownV2")

async def content_planning(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the content planning process."""
    await handle_content_planning(update, context)

async def content_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate a summary of the content."""
    await generate_content_summary(update, context)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
🚀 *Welcome to ContentWizard Help* 🚀

ContentWizard is your AI assistant for managing social media content. Here's how you can use its features:

🔹 `/content_planning` - Create post ideas with an AI agent. Define your time period and topics, and receive a list of PostIdeas.
🔹 `/content_summary` - Summarize your content from Notion, identify opportunities, and detect anomalies.

💡 *Tips*:
   - Use `/content_planning` regularly to keep your content fresh and engaging.
   - Rely on `/content_summary` to stay informed about your content's performance and opportunities.

🔍 Need more assistance or have feedback? Just reply with your question or feedback!

Make your social media management effortless with ContentWizard!
"""
    await update.message.reply_text(help_text, parse_mode="MarkdownV2")

# Main Function
def main() -> None:
    """Run the bot."""
    persistence = PicklePersistence(filepath="contentwizard_persistence")
    application = Application.builder().token(TOKEN).persistence(persistence).build()

    # Adding handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("content_planning", content_planning))
    application.add_handler(CommandHandler("content_summary", content_summary))
    application.add_handler(CommandHandler("help", help))

    application.run_polling()

if __name__ == "__main__":
    main()
