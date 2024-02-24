from telegram.ext import ConversationHandler, CommandHandler

from conversation_handlers.conversation_states import END


async def handle_content_summary(update, context):
    """
    Handle the content summary process by starting a conversation with the user.
    """
    await update.message.reply_text("📊 Let's summarize your content and identify opportunities. For now this method is not implemented, please try again later.")
    return END

async def cancel_content_summary(update, context):
    """
    Cancel the content summary process and end the conversation.
    """
    update.message.reply_text("‼️ Content summary cancelled. You can start again by typing `/content_summary`.")
    return END

def add_content_summary_conversation_handler() -> ConversationHandler:
    """
    Create the content summary conversation handler.
    """
    return ConversationHandler(
        entry_points=[CommandHandler("content_summary", handle_content_summary)],
        states={END: []},
        fallbacks=[CommandHandler("cancel", cancel_content_summary)],
    )
