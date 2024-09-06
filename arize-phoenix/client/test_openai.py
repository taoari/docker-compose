import phoenix as px
from phoenix.trace.openai import OpenAIInstrumentor

# # To view traces in Phoenix, you will first have to start a Phoenix server. You can do this by running the following:
# session = px.launch_app()

# Initialize OpenAI auto-instrumentation
OpenAIInstrumentor().instrument()

import os
from openai import OpenAI

# Initialize an OpenAI client
client = OpenAI()

# Define a conversation with a user message
conversation = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, can you help me with something?"}
]

# Generate a response from the assistant
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=conversation,
)

# Extract and print the assistant's reply
# The traces will be available in the Phoenix App for the above messsages
assistant_reply = response.choices[0].message.content
print(assistant_reply)

import pdb; pdb.set_trace()
