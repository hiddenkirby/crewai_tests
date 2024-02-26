import os
import json
from openai import OpenAI
from dotenv import load_dotenv
# load environment variables from .env file
load_dotenv()


client = OpenAI()

# TODO: move into tools dir
tools = [
    {
        "type": "function",
        "function": {
            "name": "joke_of_the_day",
            "description": "Get a random joke of the day",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g., San Francisco, CA"
                    }
                },
                "required": ["location"]
            }
        }
    },
]

chat_completion = client.chat.completions.create(
    messages=[{
        "role": "user",
        "content": "How is the weather in Berlin?"
    }],
    model="gpt-3.5-turbo",
    tools=tools
)

tool_call = chat_completion.choices[0].message.tool_calls[0]
print(tool_call)

function_name = tool_call.function.name
arguments = json.loads(tool_call.function.arguments)


def joke_of_the_day(arguments):
    return "Random joke of the day"

def get_current_weather(arguments):
    location = arguments.get('location')
    return f"It's hot in {location}"


function_map = {
    "joke_of_the_day": joke_of_the_day,
    "get_current_weather": get_current_weather
}

func = function_map.get(function_name)
result = func(arguments)
print(result)