from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from agents.conversational_ai_agent import ConversationalAIAgent
from models.conversation_config import ConversationConfig
from langchain.chat_models import ChatOpenAI


class CustomConversationalAIAgent(ConversationalAIAgent):
    def __init__(self, conversation_config: ConversationConfig):
        super().__init__(conversation_config)
        self.model = self.initialize_model()
        self.collected_data = {}  # To store collected data from each state

    def initialize_model(self):
        return ChatOpenAI(model=self.conversation_config.agent_profile.model)

    def generate_conversation_handler(self) -> ConversationHandler:
        state_handlers = {
            state.name: [MessageHandler(Filters.text & ~Filters.command, self.process_user_input)]
            for state in self.conversation_config.states
        }

        return ConversationHandler(
            entry_points=[CommandHandler("start", self.entry_function)],
            states=state_handlers,
            fallbacks=[CommandHandler("cancel", self.cancel_conversation)],
            conversation_timeout=600
        )

    async def entry_function(self, update: Update, context: CallbackContext):
        intro_message = "Welcome to our conversation. Here's what we'll cover:"
        intro_message += f"\nGoal: {self.conversation_config.purpose}"
        intro_message += f"\nFinal Output: {self.conversation_config.output}"
        await update.message.reply_text(intro_message)

        await self.present_stage(update, context)

    async def present_stage(self, update: Update, context: CallbackContext):
        if self.current_state_index < len(self.conversation_config.states):
            current_stage = self.conversation_config.states[self.current_state_index]
            await update.message.reply_text(f"Now in stage: {current_stage.name}. {current_stage.description}")
        else:
            await self.conclude_conversation(update, context)

    async def process_user_input(self, update: Update, context: CallbackContext):
        user_input = update.message.text
        # Process the input using the model here...
        # For simplicity, let's assume user input is directly stored
        self.collected_data[self.current_state_index] = user_input

        # Move to the next state
        self.current_state_index += 1
        await self.present_stage(update, context)

    async def conclude_conversation(self, update: Update, context: CallbackContext):
        # Process the collected data as per the output requirements
        # For simplicity, let's just send back the collected data
        await update.message.reply_text(f"Here's what we've gathered: {self.collected_data}")
        await update.message.reply_text("Conversation concluded.")

    async def cancel_conversation(self, update: Update, context: CallbackContext):
        await update.message.reply_text("Conversation cancelled.")
        return ConversationHandler.END

    # Additional methods for handling validation and output formatting can be added here
