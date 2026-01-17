from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What jobs make good money?"},
    ],
    max_tokens=50,
)

print(completion.choices[0].message.content)