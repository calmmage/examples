from openai import Client
from dotenv import load_dotenv


def query_openai(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    system="You're a helpful assistant",
    **kwargs
):
    client = Client()

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        model=model,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    load_dotenv()
    prompt = "Tell me a random scientific concept / theory"
    response = query_openai(prompt)
    print(response)
