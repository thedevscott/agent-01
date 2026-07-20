import os
import argparse
from openai import OpenAI
from dotenv import load_dotenv

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
response = client.chat.completions.create(model="openrouter/free", 
messages=[
    {
        "role": "user",
        "content": args.user_prompt,
    }
]
)

# print(response)
if args.verbose:
    if response.usage is not None:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    else:
        raise RuntimeError("failed to access usage data")
    
print("Response: " + response.choices[0].message.content)
