from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, Runner
from dotenv import load_dotenv
import os

load_dotenv(override=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")
#check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
#Reference: https://ai.google.dev/gemini-api/docs
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model = "gemini-flash-latest",
    openai_client = external_client
)
config = RunConfig(
    model=model,
    model_provider = external_client,
    tracing_disabled = True
)
agent = Agent(
    name = "Translator",
    instructions="You are a helpful translator. Always translate English Sentences into clear and simple urdu."
)
response = Runner.run_sync(
    agent,
    input= "My name is shariq hussain.",
    run_config= config
)
print(response)