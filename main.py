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
        tools=available_functions
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

    output_message = response.choices[0].message
    if output_message.tool_calls is not None:
        for tool_call in output_message.tool_calls:
            call_function_result = call_function(tool_call, verbose)
            
            if "content" not in call_function_result or call_function_result["content"] == "":
                raise Exception("Non-existent or empty result message from tool call")

            if verbose:
                print(f"-> {call_function_result['content']}")
    else:    
        print(output_message.content)

    
def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("OpenRouter API not found")

    # Authenticate for OpenAI usage
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