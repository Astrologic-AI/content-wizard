from telegram.ext import ConversationHandler, CommandHandler, filters, MessageHandler

CONTENT_PLANNING = 1
END = ConversationHandler.END

async def handle_content_planning(update, context):
    """
    Handle the content planning process by starting a conversation with the user.
    """
    await update.message.reply_text("📝 Let's start the content planning process. Please enter your time period and topics.")
    return CONTENT_PLANNING

def cancel_content_planning(update, context):
    """
    Cancel the content planning process and end the conversation.
    """
    update.message.reply_text("‼️ Content planning cancelled. You can start again by typing `/content_planning`.")
    return END


def add_content_planning_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("content_planning", handle_content_planning)],
        states={
            CONTENT_PLANNING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_content_planning)],
            END: [],
        },
        fallbacks=[CommandHandler("cancel", cancel_content_planning)],
    )