import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

print("AI Assistant available!")

while True:
    user_message = input("You: ")

    if user_message.lower() == 'quit':
        print("AI: Goodbye!")
        break

    messages.append({"role": "user", "content": user_message})

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    ai_response = completion.choices[0].message.content

    print(f"AI: {ai_response}")

    messages.append({"role": "assistant", "content": ai_response})
