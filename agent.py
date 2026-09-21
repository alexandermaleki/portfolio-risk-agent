import os
import json
from datetime import date

from dotenv import load_dotenv
from openai import OpenAI

from schemas import TOOLS
from tools import get_volatility, get_max_drawdown, get_correlation

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-5.6-luna"
MAX_STEPS = 6

SYSTEM_PROMPT = f"""You are a portfolio risk assistant.
Use the provided tools for every calculation. Never compute or guess numbers yourself.
Today's date is {date.today().isoformat()}.
When the user refers to "last year", use the full previous calendar year.
Explain results in plain language."""

# Maps the name the model asks for to the actual Python function
TOOL_FUNCTIONS = {
    "get_volatility": get_volatility,
    "get_max_drawdown": get_max_drawdown,
    "get_correlation": get_correlation,
}


def run_tool(name, args):
    """Run one tool the model asked for. Errors are returned as text."""
    if name not in TOOL_FUNCTIONS:
        return f"Error: unknown tool '{name}'."

    try:
        return TOOL_FUNCTIONS[name](**args)
    except Exception as e:
        return f"Error running {name}: {e}"


def run_agent(question):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
	    reasoning_effort="none",
        )
        message = response.choices[0].message

        # No tool requested: the model is done.
        if not message.tool_calls:
            return message.content

        # The model asked for tools. Record its request first.
        messages.append(message)

        for call in message.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments)

            print(f"  [step {step + 1}] {name}({args})")
            result = run_tool(name, args)
            print(f"           -> {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result),
            })

    return "Stopped: reached the maximum number of steps."


if __name__ == "__main__":
    answer = run_agent("What was the volatility of Investor B in 2024?")
    print("\n" + answer)
