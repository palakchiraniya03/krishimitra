import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=api_key
)


def generate_llm_response(prompt: str) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    response = generate_llm_response(
        "Say hello. You are the AI assistant of KrishiMitra."
    )

    print(response)