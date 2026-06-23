import os

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv
from openai import OpenAI

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

response = openai_client.responses.create(
    model="gpt-4.1-mini",
    input="What is Microsoft Foundry?"
)

print(f"Response: {response.output_text}")
print(f"Response ID: {response.id}")
print(f"Tokens used: {response.usage.total_tokens}")
print(f"Status: {response.status}")
