import argparse
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions

def generate_content(client, messages, user_prompt, verbose=False):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )

    if response.usage is None:
        raise RuntimeError("Failed API request")

    if verbose == True:
        print(
            f"""
            "User prompt: {user_prompt}"
            "Prompt tokens: {response.usage.prompt_tokens}"
            "Response tokens: {response.usage.completion_tokens}"
            """
        )

    message_result = response.choices[0].message
    if message_result.tool_calls is not None:
        for tool_call in message_result.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
    else:
        print(message_result.content)

    
def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key == None:
        raise RuntimeError("OpenRouter API not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt}
    ]

    generate_content(client, messages, args.user_prompt, args.verbose)    

if __name__ == "__main__":
    main()