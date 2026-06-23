import os
import glob

from openai import OpenAI
from dotenv import load_dotenv

system_prompt = "You are a travel assistant that provides information on travel services available from all platforms and suggest the best option and the next best alternative."
last_response_id = None

load_dotenv()
model_deployment = os.getenv("MODEL_DEPLOYMENT")
openai_client = OpenAI()

print("Creating vector store")
vector_store = openai_client.vector_stores.create(
    name="travel_brochures"
)

file_streams = [open(f, "rb") for f in glob.glob("travel_pdfs/*pdf")]

if not file_streams:
    print("No PDF files in travel_pdfs folder")
    os.exit(1)
file_batch = openai_client.vectore_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id,
    files=file_streams
)
for f in file_streams:
    f.close()
print(f"Vector Store create with {file_batch.file_counts.completed} files.")

tools = [
    {
        "type": "file_search",
        "vector_store_ids": [vector_store.id]
    },
    {
        "type": "web_search"
    }
]
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


