from ollama import chat
from ollama import ChatResponse

MODEL = 'llama3.1:8b '

response: ChatResponse = chat(model=MODEL, messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)