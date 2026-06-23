import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

conversation_messages= [
    {
        "role": "system",
        "content": "You are an nba knowledge expert assistant, knowing all nba facts and stats, that answers questions clearly and concisely"
    }
]

print("Assistant: Enter a prompt (or type 'quit' to exit)")
while True:
    input_text = input("\nYou: ")

    if input_text.lower() == "quit":
        print("Assistant: Goodbye!")
        break

    conversation_messages.append({"role": "user", "content": input_text})

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=conversation_messages
    )

    assistant_message = completion.choices[0].message.content
    print("\nAssistant: ", assistant_message)

    conversation_messages.append(
        {"role": "system", "content": assistant_message}
    )
