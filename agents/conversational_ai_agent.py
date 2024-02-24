from abc import ABC, abstractmethod
from telegram.ext import ConversationHandler, CallbackContext
from telegram import Update, InlineKeyboardMarkup
from models.conversation_config import ConversationConfig
from typing import Callable, Tuple


class ConversationalAIAgent(ABC):
    def __init__(self, conversation_config: ConversationConfig):
        self.conversation_config = conversation_config
        self.current_state = None
        self.contextual_memory = {}

    @abstractmethod
    def generate_conversation_handler(self, entry_function: Callable) -> ConversationHandler:
        pass

    @abstractmethod
    async def introduce_conversation(self, update: Update, context: CallbackContext):
        pass

    @abstractmethod
    async def present_stage(self, update: Update, stage: str, context: CallbackContext):
        pass

    @abstractmethod
    async def process_user_input(self, update: Update, context: CallbackContext) -> Tuple[bool, InlineKeyboardMarkup]:
        pass

    @abstractmethod
    async def validate_information(self, update: Update, context: CallbackContext):
        pass

    @abstractmethod
    async def conclude_conversation(self, update: Update, context: CallbackContext):
        pass
