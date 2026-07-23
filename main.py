import os
import argparse
import json
import sys
from call_function import available_functions, call_function
from openai import OpenAI
from dotenv import load_dotenv
from prompts import system_prompt

#========================================================================
# Environment Variables Ingestion
#========================================================================
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

#========================================================================
# Parser Setup
#========================================================================
parser = argparse.ArgumentParser(description="AI-Agent")
parser.add_argument("user_prompt", type=str, help="User prompt for the ai agent")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

#========================================================================
# LLM Interfacing
#========================================================================
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,

)

#========================================================================
# Main Work
#========================================================================
messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},   
]

# Agent Loop
final_response = False
for _ in range(20):
    response = client.chat.completions.create(model="openrouter/free", 
    # temperature=0 # more deterministic output
    messages=messages,
    tools=available_functions,
    )

    # print(response)
    if args.verbose:
        if response.usage is not None:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        else:
            raise RuntimeError("failed to access usage data")

    # Tool Calls
    message = response.choices[0].message
    messages.append(message)

    if message.tool_calls is not None:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
            result_message = call_function(tool_call, args.verbose)
            messages.append(result_message)

            if not result_message['content']:
                raise RuntimeError("missing tool call content")
            
            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        final_response = True
        print("Response: " + response.choices[0].message.content)
        break

if not final_response:
    print("Final response not reached in alloted iterations")
    sys.exit(1)
