import os
import json
from multiprocessing.pool import ThreadPool
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


def ai_square_number(number):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a calculator. Only return the numerical answer."},
                {"role": "user", "content": f"What is {number} squared?"}
            ],
            max_tokens=10
        )
        result = response.choices[0].message.content.strip()
        return int(result)
    except Exception as e:
        return f"Error with {number}: {e}"


if __name__ == '__main__':
    data = [1, 2, 3, 4, 5]

    print("-> Sending requests to AI in parallel...")
    with ThreadPool(processes=len(data)) as pool:
        results = pool.map(ai_square_number, data)

    print(f"Results from AI: {results}")