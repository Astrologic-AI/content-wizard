from langchain_core.prompts import PromptTemplate
from telegram.ext import CommandHandler, ConversationHandler
from agents.custom_conversational_ai_agent import CustomConversationalAIAgent
from models.conversation_config import ConversationConfig
from models.agent_profile import AgentProfile
from models.information_requirement import InformationRequirement
from models.state import State
from models.output_requirement import OutputRequirement


def create_content_planning_config() -> ConversationConfig:
    # Define the configuration for content planning
    return ConversationConfig(
        name="Content Planning",
        purpose="Plan content for a specified time period and topics",
        output=[OutputRequirement(
            key="post_ideas", description="A list of Post Ideas object that will be inserted in the Content Calendar",
            validation="list[PostIdea]",)],
        states=[
            State(
                name="content_distribution",
                description="We will decide how to distribute the posts and topics over the time period",
                information_requirements=[
                    InformationRequirement(
                        key="time_period",
                        description="Specify the time period for content distribution, e.g. 1 week, 1 month, etc."
                                    "The format should be a list of two datetime objects, start and end time",
                        validation="List[datetime]"
                    ),
                    InformationRequirement(
                        key="post_distribution_frequency",
                        description="Specify the frequency of posts, e.g. daily, twice a day, etc.",
                        validation="str"
                    ),
                    InformationRequirement(
                        key="topics",
                        description="Specify topics for content distribution, which will be used to generate post ideas",
                        validation="list[str]"
                    )
                ],
                next_state_criteria="time_period and post_distribution_frequency and topics"
            ),
        ],
        agent_profile=AgentProfile(
            name="Content Planning Agent",
            description="A conversational AI agent to help plan content",
            model="gpt-3.5-turbo",
            prompt_template=PromptTemplate.from_template(
                template="You are a content planner. You need to generate post ideas based on the conversation "
                         "mantained with the user. The conversation is structured by step. Each step has a "
                         "specific purpose and information requirements. The conversation starts with the user and based"
                         "on the current step the user will be asked to provide specific information. The information "
                         "will be used to generate post ideas. The conversation will conclude when all step are done"
                         "and the Output Requirement is met. "
                         "This is the current state: {current_state.name}.  {current_state.purpose}."
                         "The information requirements are: {current_state.information_requirements}."
                         "The output requirement is: {output_requirement}."),
            tools=[]
        ),
    )


def add_content_planning_conversation_handler() -> ConversationHandler:
    # Initialize CustomConversationalAIAgent with the conversation config
    conversation_config = create_content_planning_config()
    custom_agent = CustomConversationalAIAgent(conversation_config)

    # Use the generated conversation handler from the custom agent
    conversation_handler = custom_agent.generate_conversation_handler()

    # Additional setup or customization of the handler can be done here if necessary

    return conversation_handler
