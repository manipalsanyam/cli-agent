from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Type something:")
user_input = input(">> ")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": user_input}]
)

print("\nResponse:")
print(response.choices[0].message.content)