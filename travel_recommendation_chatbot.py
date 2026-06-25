import os
import glob
import base64
from pathlib import Path

# from openai import OpenAI
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

OUTPUT_DIR = Path("agents_outputs")

def get_output_path(filename):
    """Create a unique path for generated files."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    file_name = Path(filename).name
    stem = Path(file_name).stem or "output"
    suffix = Path(file_name).suffix
    output_path = OUTPUT_DIR / file_name

    counter = 1
    while output_path.exists():
        output_path = OUTPUT_DIR / f"{stem}_{counter}{suffix}"
        counter += 1

    return output_path


def save_bytes(file_bytes, filename):
    """Save binary content to a local file."""
    output_path = get_output_path(filename)
    with open(output_path, "wb") as file_handle:
        file_handle.write(file_bytes)
    return output_path


def save_image(image_data, filename):
    """Save base64 image data to a file."""
    return save_bytes(base64.b64decode(image_data), filename)


def download_container_file(openai_client, annotation, downloaded_files):
    """Download a cited container file once and return its local path."""
    cache_key = (annotation.container_id, annotation.file_id)
    if cache_key in downloaded_files:
        return downloaded_files[cache_key]

    file_content = openai_client.containers.files.content.retrieve(
        file_id=annotation.file_id,
        container_id=annotation.container_id,
    )
    output_path = save_bytes(
        file_content.read(),
        annotation.filename or f"{annotation.file_id}.bin",
    )
    downloaded_files[cache_key] = output_path
    return output_path


def format_output_text(content_item, openai_client, downloaded_files):
    """Replace sandbox file citations with local file paths."""
    text = content_item.text or ""
    replacements = []
    referenced_files = set()

    for annotation in content_item.annotations or []:
        if getattr(annotation, "type", "") != "container_file_citation":
            continue

        output_path = download_container_file(openai_client, annotation, downloaded_files)
        replacement_text = f"{annotation.filename} (saved to {output_path})"
        referenced_files.add(output_path)

        start_index = getattr(annotation, "start_index", None)
        end_index = getattr(annotation, "end_index", None)
        if start_index is not None and end_index is not None:
            replacements.append((start_index, end_index, replacement_text))
            continue

        annotated_text = getattr(annotation, "text", "")
        if annotated_text:
            text = text.replace(annotated_text, replacement_text)

    for start_index, end_index, replacement_text in sorted(replacements, reverse=True):
        text = f"{text[:start_index]}{replacement_text}{text[end_index:]}"

    return text, referenced_files

def main():
    # system_prompt = "You are a travel assistant that provides information on travel services available from all platforms and suggest the best option and the next best alternative."
    # last_response_id = None

    load_dotenv()
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    agent_name = os.getenv("AGENT_NAME")

    if not project_endpoint:
        print("Error: PROJECT_ENDPOINT environment variable not set")
        print("Please set it in your .env file or environment")
        return
    
    print("Connecting to Microsoft Foundry project...")
    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        credential=credential,
        endpoint=project_endpoint
    )

    # model_deployment = os.getenv("MODEL_DEPLOYMENT")
    openai_client = project_client.get_openai_client()

    print(f"Loading agent: {agent_name}")
    agent = project_client.agents.get(agent_name=agent_name)
    print(f"Connected to agent: {agent.name} (id: {agent.id})")

    conversation = openai_client.conversations.create(items=[])
    print(f"Conversation created (id: {conversation.id})")

    # Chat loop
    print("\n" + "="*60)
    print("Travel Support Agent Ready!")
    print("Ask questions, request data analysis, or get help.")
    print("Type 'exit' to quit.")
    print("="*60 + "\n")

    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Add user message to conversation
        openai_client.conversations.items.create(
            conversation_id=conversation.id,
            items=[{"type": "message", "role": "user", "content": user_input}]
        )
        
        # Get response from agent
        print("\n[Agent is thinking...]")
        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
            input=""
        )

        # Display response and save any generated files locally
        handled_output = False
        downloaded_files = {}
        referenced_files = set()
        image_count = 0

        if hasattr(response, "output") and response.output:
            for item in response.output:
                item_type = getattr(item, "type", "")

                if item_type == "message" and getattr(item, "content", None):
                    for content_item in item.content:
                        if getattr(content_item, "type", "") != "output_text":
                            continue

                        formatted_text, message_files = format_output_text(
                            content_item,
                            openai_client,
                            downloaded_files,
                        )
                        referenced_files.update(message_files)

                        if formatted_text:
                            print(f"\nAgent: {formatted_text}\n")
                            handled_output = True

                elif hasattr(item, "text") and item.text:
                    print(f"\nAgent: {item.text}\n")
                    handled_output = True

                elif item_type == "image":
                    image_count += 1
                    filename = f"chart_{image_count}.png"

                    if hasattr(item, "image") and hasattr(item.image, "data"):
                        file_path = save_image(item.image.data, filename)
                        print(f"\n[Agent generated a chart - saved to: {file_path}]")
                    else:
                        print("\n[Agent generated an image]")
                    handled_output = True

            for file_path in downloaded_files.values():
                if file_path not in referenced_files:
                    print(f"\n[Agent generated a file - saved to: {file_path}]")
                    handled_output = True

        if not handled_output and hasattr(response, "output_text") and response.output_text:
            print(f"\nAgent: {response.output_text}\n")

    # print("Creating vector store")
    # vector_store = openai_client.vector_stores.create(
    #     name="travel_brochures"
    # )

    # file_streams = [open(f, "rb") for f in glob.glob("travel_pdfs/*.pdf")]

    # if not file_streams:
    #     print("No PDF files in travel_pdfs folder")
    #     os.exit(1)

    # file_batch = openai_client.vector_stores.file_batches.upload_and_poll(
    #     vector_store_id=vector_store.id,
    #     files=file_streams
    # )
    # for f in file_streams:
    #     f.close()
    # print(f"Vector Store create with {file_batch.file_counts.completed} files.")

    # tools = [
    #     {
    #         "type": "file_search",
    #         "vector_store_ids": [vector_store.id]
    #     },
    #     {
    #         "type": "web_search"
    #     }
    # ]
    # print("Travel Assistant: Enter a prompt (or type 'quit' to exit)")
    # while True:
    #     input_text = input("\nYou: ")
    #     if input_text.lower() == "quit":
    #         print("Assistant: Goodbye!")
    #         break
    #     if len(input_text) == 0:
    #         print("Please enter a prompt.")
    #         continue

    #     response = openai_client.responses.create(
    #         model=model_deployment,
    #         instructions=system_prompt,
    #         input=input_text,
    #         previous_response_id=last_response_id,
    #         tools=tools
    #     )

    #     assistant_response = response.output_text
    #     print("\n Assistant: ", assistant_response)
    #     last_response_id = response.id
if __name__ == "__main__":
    main()
