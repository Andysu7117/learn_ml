import os

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
import asyncio

load_dotenv()

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

project_endpoint=os.getenv("PROJECT_ENDPOINT")
project_client = AIProjectClient(
    credential=DefaultAzureCredential,
    endpoint=project_endpoint
)

# openai_chat_client = project_client.get_openai_client()

# openai_client = OpenAI(
#     base_url=os.getenv("OPENAI_ENDPOINT"),
#     api_key=os.getenv("AZURE_OPENAI_API_KEY")
# )

openai_client = OpenAI()

last_response_id = None
print("Assistant: Enter a prompt (or type 'quit' to exit)")
while True:
    input_text = input('\nYou: ')
    if input_text.lower() == "quit":
        print("Assistant: Goodbye!")
        break
    if len(input_text) == 0:
        print("Please enter a prompt.")
        continue

    response = openai_client.responses.create(
        model="gpt-4.1-mini",
        instructions="You are an nba knowledge expert assistant, knowing all nba facts and stats, that answers questions clearly and concisely",
        input=input_text,
        max_output_tokens=200,
        previous_response_id=last_response_id
    )
    assistant_text = response.output_text
    print(f"\nAssistant: {assistant_text}")
    last_response_id = response.id

# response1 = openai_client.responses.create(
#     model="gpt-4.1-mini",
#     instructions="You are an nba knowledge expert assistant, knowing all nba facts and stats, that answers questions clearly and concisely",
#     input="Who are to top 5 all time scorers?",
#     max_output_tokens=200
# )

# print(f"Assistant: {response1.output_text}")
# print(f"Response ID: {response.id}")
# print(f"Tokens used: {response.usage.total_tokens}")
# print(f"Status: {response.status}")

# Continue the conversation
# response2 = openai_client.responses.create(
#     model="gpt-4.1-mini",
#     instructions="You are an nba knowledge expert assistant, knowing all nba facts and stats, that answers questions clearly and concisely",
#     input="how many more games does Lebron need to be the all time scorer?",
#     previous_response_id=response1.id,
#     max_output_tokens=200
# )

# print(f"Assistant: {response2.output_text}")
client = AsyncOpenAI()

async def stream_response():
    stream = await client.responses.create(
        model="gpt-4o-mini",
        input="Write a haiku about coding",
        stream=True
    )

    async for event in stream:
        print(event, end="", flush=True)

asyncio.run(stream_response())
