import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, PicklePersistence

from config import TOKEN
from conversation_handlers.content_planning.content_planning_conversation_handler import add_content_planning_conversation_handler
from conversation_handlers.content_summary.content_summary_conversation_handler import \
    add_content_summary_conversation_handler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start the conversation and display the main menu."""
    reply_text = """
🚀 **Welcome to ContentWizard\!** Your AI assistant for social media content creation and scheduling\.

🎛️ Quick Commands:

🔸 `/content_planning`: Interact with an AI agent to create post ideas\.
🔸 `/content_summary`: Summarize available content and identify opportunities\.

🔍 Need help? Type `/help` for assistance\.

Let's make your social media management magical with ContentWizard\!
"""
    await update.message.reply_text(reply_text, parse_mode="MarkdownV2")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
🚀 *Welcome to ContentWizard Help\!* 🚀

ContentWizard is your AI assistant for managing social media content\. Here's how you can use its features:

🔹 `/content_planning` \- Create post ideas with an AI agent\. Define your time period and topics, and receive a list of PostIdeas\.
🔹 `/content_summary` \- Summarize your content from Notion, identify opportunities, and detect anomalies\.

💡 *Tips*:
   \- Use `/content_planning` regularly to keep your content fresh and engaging\.
   \- Rely on `/content_summary` to stay informed about your content's performance and opportunities\.

🔍 Need more assistance or have feedback? Just reply with your question or feedback\!

Make your social media management effortless with ContentWizard\!
"""
    await update.message.reply_text(help_text, parse_mode="MarkdownV2")

# Main Function
def main() -> None:
    """Run the bot."""
    persistence = PicklePersistence(filepath="contentwizard_persistence")
    application = Application.builder().token(TOKEN).persistence(persistence).build()

    # Adding handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(add_content_planning_conversation_handler())
    application.add_handler(add_content_summary_conversation_handler())
    application.add_handler(CommandHandler("help", help))

    application.run_polling()

if __name__ == "__main__":
    main()
