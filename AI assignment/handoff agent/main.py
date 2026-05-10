from agents import Agent, Runner, handoff
import asyncio
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os

load_dotenv(override=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-flash-latest",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

billing_agent = Agent(
    name="Billing Agent",
    instructions="You only answer questions related to billing."
)

refund_agent = Agent(
    name="Refund Agent",
    instructions="You are responsible only for handling refund-related requests and guiding users through the refund process."
)

custon_refund_handoff = handoff(
    agent=refund_agent,
    tool_name_override="custom_refund_tool",
    tool_description_override="Handle user refund requests with extra care."
)

demage_refund_handoff = handoff(
    agent=refund_agent,
    tool_name_override="demage_refund_tool",
    tool_description_override="Handle refund due to damaged item."
)

late_delivery_refund_handoff = handoff(
    agent=refund_agent,
    tool_name_override="late_delivery_refund_tool",
    tool_description_override="Handle refund due to late delivery."
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="Read the user's request and decide which agent is best suited to handle it.",
    handoffs=[billing_agent, custon_refund_handoff, demage_refund_handoff, late_delivery_refund_handoff]
)

async def main():
    result = await Runner.run(
        triage_agent,
         "I need a refund for my recent purchase.",
        #"My order arrived 10 days late. I want a refund.",
        run_config=config
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())