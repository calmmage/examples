import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


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


role_map = {
    "system": "system",
    "user": "human",
    "assistant": "ai",
    "human": "human",
    "ai": "ai",
}


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
                messages.append((role_map[msg["role"]], msg["content"]))
        messages.extend(warmup_messages)

    # messages.append(HumanMessage(content=prompt_template))
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
    config = {}
    if use_langfuse:
        langfuse_callback = get_langfuse_callback()
        config["callbacks"] = [langfuse_callback]
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
    result = chain.invoke(input={"prompt": prompt}, config=config)

    return result.content


if __name__ == "__main__":
    load_dotenv()
    prompt = "Tell me a random scientific concept / theory"
    response = query_langchain(prompt, use_langfuse=True)
    print(response)
