import os

from openai import OpenAI
from dotenv import load_dotenv

system_prompt = "You are a travel assistant that provides information on travel services available from all platforms and suggest the best option and the next best alternative."
last_response_id = None
tools = [{"type": "web_search"}]

load_dotenv()
model_deployment = os.getenv("MODEL_DEPLOYMENT")
openai_client = OpenAI()

print("Travel Assistant: Enter a prompt (or type 'quit' to exit)")
while True:
    input_text = input("\nYou: ")
    if input_text.lower() == "quit":
        print("Assistant: Goodbye!")
        break
    if len(input_text) == 0:
        print("Please enter a prompt.")
        continue

    response = openai_client.responses.create(
        model=model_deployment,
        instructions=system_prompt,
        input=input_text,
        previous_response_id=last_response_id,
        tools=tools
    )

    assistant_response = response.output_text
    print("\n Assistant: ", assistant_response)
    last_response_id = response.id


