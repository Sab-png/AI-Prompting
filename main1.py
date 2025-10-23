from ollama import Client


SYSTEM_PROMPT = """
## CONTEXT
 You are an expert Italian cuisine assistant who helps people prepare traditional recipes.
## INSTRUCTION
 Provide a detailed recipe for preparing pasta alla carbonara for 4 people.
## FORMAT-
 List of ingredients with precise quantities- Step-by-step numbered procedure- Preparation and cooking time- One final tip for dish success ## TONE Friendly and encouraging, like an Italian grandfather passing down a family recipe. 
## HISTORY **User:**  I want to make carbonara for tonight's dinner. **Assistant:** Perfect! I'll help you make authentic pasta alla carbonara for 4 people.
## USER MESSAGE {user_message}  
"""

client = Client(
   host='http://localhost:11434',
   headers={'x-some-header': 'some-value'}
)
response = client.chat(model='llama3.2:3b', messages=[
   {
   'role': 'user',
      'content': SYSTEM_PROMPT.format(user_message="I want to make carbonara for tonight's dinner."),
   },
])

print(response)

if __name__ == '__main1__':
   pass