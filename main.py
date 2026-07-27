import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key == None:
    raise RuntimeError("OpenRouter API not found")


from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages = [
    {
        "role": "user",
        "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    }
]

response = client.chat.completions.create(model= "openrouter/free", messages= messages)

if response.usage == None:
    raise RuntimeError("Failed API request")
print(f"Prompt tokens: {response.usage.prompt_tokens}")
print(f"Response tokens: {response.usage.completion_tokens}")
print(response.choices[0].message.content)

def main():
    # print("Hello from mega-brain!")
    if __name__ == "__main__":
        main()
