import os
from langchain.agents import initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from typing import Type, Callable, Any
from pydantic import BaseModel, Field


class CurrentRecipeInput(BaseModel):
    """Inputs for AlternativeSustainableRecipeTool"""
    recipe: str = Field(description="Name of the recipe")


class AlternativeSustainableRecipeTool(BaseTool):
    name = "AlternativeSustainableRecipeTool"
    description = """
        Useful when you want to get alternative recipes to a given recipe. This tool return a an alternative recipe.
        """

    args_schema: Type[BaseModel] = CurrentRecipeInput


    get_alternative_recipe: Callable = None

    def __init__(self, **data):
        super().__init__(**data)
        self.get_alternative_recipe = data.get('get_alternative_recipe_func')

    def _run(self, recipe: str):
        recipes_response = self.get_alternative_recipe(recipe)
        return recipes_response

    def _arun(self, recipe: str):
        raise NotImplementedError("AlternativeSustainableRecipeTool does not support async")


class Agent:
    def __init__(self, tools, open_ai_key, model_name='gpt-3.5-turbo', memory_size=10, temperature=0):
        # Set up the turbo LLM
        os.environ["OPENAI_API_KEY"] = open_ai_key

        self.turbo_llm = ChatOpenAI(
            temperature=temperature,
            model_name=model_name
        )

        # Conversational agent memory
        self.memory = ConversationBufferWindowMemory(
            memory_key='chat_history',
            k=memory_size,
            return_messages=True
        )

        # Create our agent
        self.conversational_agent = initialize_agent(
            agent='chat-conversational-react-description',
            tools=tools,
            llm=self.turbo_llm,
            verbose=False,
            max_iterations=3,
            early_stopping_method='generate',
            memory=self.memory,
            handle_parsing_errors=True
        )

    def ask(self, question):
        response = self.conversational_agent(question)
        return response['output']
