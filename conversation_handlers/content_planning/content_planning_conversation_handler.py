from telegram.ext import CommandHandler, ConversationHandler
from agents.custom_conversational_ai_agent import CustomConversationalAIAgent
from models.conversation_config import ConversationConfig
from models.agent_profile import AgentProfile
from models.state import State
from models.output_requirement import OutputRequirement


def create_content_planning_config() -> ConversationConfig:
    # Define the configuration for content planning
    return ConversationConfig(
        name="Content Planning",
        purpose="Plan content for a specified time period and topics",
        output=[OutputRequirement()],  # Define output requirements
        states=[
            State(name="TimePeriod", description="Enter the time period for content ()"),
            State(name="Topics", description="Specify topics for content ()")
            # Add other states as needed
        ],
        agent_profile=AgentProfile(),  # Define the agent profile
        contextual_memory=["time_period", "topics"]
    )


def add_content_planning_conversation_handler() -> ConversationHandler:
    # Initialize CustomConversationalAIAgent with the conversation config
    conversation_config = create_content_planning_config()
    custom_agent = CustomConversationalAIAgent(conversation_config)

    # Use the generated conversation handler from the custom agent
    conversation_handler = custom_agent.generate_conversation_handler()

    # Additional setup or customization of the handler can be done here if necessary

    return conversation_handler
