import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Load environment variables from the .env file
load_dotenv()

# Retrieve the OpenAI API key from the environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Template for conversation prompts
PROMPT_TEMPLATE = """
You are an assistant for question-answering tasks. Your responses must be 
consistent, provided in a single sentence, and always in the third person. Include emojis that summarize the content 
of your answer. Below are the context and the question from the user: 
context = {context} 
question = {question}

Translate your response to {language}.Return only a single sentence.
"""

# Instantiate the ChatOpenAI model
LLM = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Create a prompt template from the defined template
PROMPT = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

# Directory to store files
DIRECTORY = "files"

# Dictionary to store databases
DBS = {}

# Dictionary to keep data in memory
MEMORY = {}

# Dictionary to store user prompts
PROMPTS = {}
