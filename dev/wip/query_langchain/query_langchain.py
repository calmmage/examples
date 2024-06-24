from openai import Client
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate

# from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(
#     model="gpt-4o",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     # api_key="...",  # if you prefer to pass api key in directly instaed of using env vars
#     # base_url="...",
#     # organization="...",
#     # other params...
# )
from dotenv import load_dotenv
import os


def get_langfuse_callback(
    public_key: str = None, secret_key: str = None, host: str = None
):
    from langfuse.callback import CallbackHandler

    if public_key is None:
        load_dotenv()
        public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    if secret_key is None:
        load_dotenv()
        secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    if host is None:
        load_dotenv()
        host = os.getenv("LANGFUSE_HOST")

    return CallbackHandler(public_key=public_key, secret_key=secret_key, host=host)


def escape_curly_braces(text):
    return text.replace("{", "{{").replace("}", "}}")


def _assume_alternating_messages(warmup_messages):
    for i, msg in enumerate(warmup_messages):
        if i % 2 == 0:
            # yield HumanMessage(content=msg)
            yield ("human", msg)
        else:
            # yield AIMessage(content=msg)
            yield ("ai", msg)


def build_langchain_prompt(
    system: str, warmup_messages=None, prompt_template="{prompt}"
) -> ChatPromptTemplate:
    # messages = [SystemMessage(content=system)]
    messages = [("system", system)]
    if warmup_messages:
        # option 1: list of strings -> assume alternating messages
        # option 2: list of dicts (role, content) -> convert to messages
        # option 3: list of Message objects -> use as is
        if isinstance(warmup_messages[0], str):
            warmup_messages = _assume_alternating_messages(warmup_messages)
        elif isinstance(warmup_messages[0], dict):
            for msg in warmup_messages:
                # if msg["role"] == "system":
                #     messages.append(SystemMessage(content=msg["content"]))
                # elif msg["role"] == "user":
                #     messages.append(HumanMessage(content=msg["content"]))
                # elif msg["role"] == "assistant":
                #     messages.append(AIMessage(content=msg["content"]))
                if msg["role"] == "system":
                    messages.append(("system", msg["content"]))
                elif msg["role"] == "user":
                    messages.append(("human", msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(("ai", msg["content"]))
        messages.extend(warmup_messages)
    # messages.append(HumanMessage(content=escape_curly_braces(prompt_template)))
    # messages.append(HumanMessage(content=prompt_template))
    # messages.append(("human", escape_curly_braces(prompt_template)))
    messages.append(("human", prompt_template))
    return ChatPromptTemplate.from_messages(messages=messages)


def query_langchain(
    prompt: str,
    system: str = "You're a helpful assistant",
    model_name="gpt-3.5-turbo",
    use_langfuse=False,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    **kwargs
) -> str:
    if use_langfuse:
        langfuse_callback = get_langfuse_callback()
        kwargs["callbacks"] = langfuse_callback
    # Initialize the language model
    llm = ChatOpenAI(
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
        max_retries=max_retries,
        **kwargs
    )

    # Build the prompt
    chat_prompt = build_langchain_prompt(system)

    # Set up the LangChain chain
    chain = chat_prompt | llm
    # Run the query
    response = chain.invoke(
        input={"prompt": prompt}
        # input={},
        # prompt=prompt,
    )

    return response.content


#
# def query_langchain(
#     prompt: str,
#     model: str = "gpt-3.5-turbo",
#     system="You're a helpful assistant",
#     **kwargs
# ):
#     client = Client()
#
#     response = client.chat.completions.create(
#         messages=[
#             {"role": "system", "content": system},
#             {"role": "user", "content": prompt},
#         ],
#         model=model,
#     )
#     return response.choices[0].message.content
# def query_langchain_wrapper(
#     prompt: str,
#     model: str = "gpt-3.5-turbo",
#     system="You're a helpful assistant",
#     **kwargs
# ):
#     # Build the langchain prompt
#     langchain_prompt = build_langchain_prompt(system)
#
#     # Run the query using the langchain prompt and the provided model
#     response = query_langchain(prompt=prompt, system=system, model_name=model, **kwargs)
#
#     return response


# Example usage
if __name__ == "__main__":
    # system_message = "You are a helpful assistant

    load_dotenv()
    prompt = "Tell me a random scientific concept / theory"
    # response = query_openai(prompt)
    response = query_langchain(prompt)
    print(response)
