from dotenv import load_dotenv
from anthropic import Anthropic
import os

# Load the API key from your .env file
load_dotenv()

# Create the client (it automatically reads ANTHROPIC_API_KEY from the environment)
client = Anthropic()

# Send a simple test message
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Say hello and confirm you're working, in one short sentence."}
    ]
)

print(response.content[0].text)