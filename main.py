import argparse
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

def generate_content(client, messages, user_prompt, verbose=False):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )

    if response.usage is None:
        raise RuntimeError("Failed API request")

    if verbose:
        print(
            f"""
            "User prompt: {user_prompt}"
            "Prompt tokens: {response.usage.prompt_tokens}"
            "Response tokens: {response.usage.completion_tokens}"
            """
        )

    message_return = response.choices[0].message
    if message_return.tool_calls is not None:
        for tool_call in message_return.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")

            result_message = call_function(tool_call, verbose)
            
            if not ("content" in result_message and result_message["content"] != ""):
                raise Exception("empty or nonexistent result message from tool call (function call)")

            if verbose:
                print(f"-> {result_message['content']}")
    else:    
        print(message_return.content)

    
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