from dotenv import load_dotenv
from openai import OpenAI

_ = load_dotenv()

client = OpenAI()


def chatgpt(prompt):
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    ).dict()["choices"][0]["message"]["content"]
