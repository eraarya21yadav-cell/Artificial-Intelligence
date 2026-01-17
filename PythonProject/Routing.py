import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def calculate_expression(expression: str) -> str:
    try:
        return str(eval(expression))
    except:
        return "Error in calculation."

tools = {"calculate_expression": calculate_expression}

MATH_TOOL_SCHEMA = [
    {"type": "function", "function": {
        "name": "calculate_expression",
        "description": "does a math expression and gives the result.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "The math expression as a string."},
            },
            "required": ["expression"],
        },
    }}
]

def run_agent(system_instruction: str, user_query: str, tool_schemas: list) -> str:
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_query}
    ]

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=messages,
        tools=tool_schemas,
        tool_choice="auto",
    )

    message = response.choices[0].message

    if message.tool_calls:
        messages.append(message)

        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            func_response = tools[func_name](**func_args)

            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": func_name,
                "content": func_response,
            })

        final_response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages,
        )
        return final_response.choices[0].message.content.strip()

    return message.content.strip()

def math_agent(query: str) -> str:
    print("-> Math Agent: Running calculation.")
    INST = "You are a Math Solver. You use 'calculate_expression' tool to find answer"
    return run_agent(INST, query, MATH_TOOL_SCHEMA)

def creative_agent(query: str) -> str:
    print("-> Creative Agent: Generating content.")
    INST = "You are a creative agent."
    return run_agent(INST, query, [])

def default_agent(query: str) -> str:
    print("-> Default Agent: Consulting general knowledge.")
    INST = "You are an AI assistant. Provide answer based on your knowledge."
    return run_agent(INST, query, [])

def ai_router(user_query: str) -> str:
    query_lower = user_query.lower()

    if any(k in query_lower for k in ["calculate", "multiply", "square root", "times", "plus", "sum", "math"]):
        return math_agent(user_query)

    elif any(k in query_lower for k in ["write a poem", "tell me a story", "creative", "whimsical"]):
        return creative_agent(user_query)

    else:
        return default_agent(user_query)

query1 = "What is 5 times 8 and then add 12?"
result1 = ai_router(query1)
print(f"\nQUERY: {query1}\nRESULT:\n{result1}")

query2 = "Write a short poem about a robot."
result2 = ai_router(query2)
print(f"\nQUERY: {query2}\nRESULT:\n{result2}")

query3 = "Tell me about the latest tech trends"
result3 = ai_router(query3)
print(f"\nQUERY: {query3}\nRESULT:\n{result3}")