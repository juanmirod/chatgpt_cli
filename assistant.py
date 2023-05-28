import json
from openai import ChatCompletion, Embedding


def chat_completion(system, messages, temperature):
    try:
        result = execute(system, messages, temperature)
    except Exception as e:
        result = (str(e), 0)
    return result


def execute(system, messages, temperature):
    system_message = {"role": "system", "content": system}
    completion = ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[system_message] + messages,
        temperature=temperature)
    token_total = completion["usage"]["total_tokens"]
    response = completion["choices"][0]["message"]["content"]
    return (response, token_total)


def memorize(text):
    response = Embedding.create(
        engine="text-embedding-ada-002",
        input=text
    )
    new_embedding = {"text": text, "embedding": response["data"][0]["embedding"]}
    with open("db/tmp_db_rows.md", "a") as f:
        f.write(json.dumps(new_embedding) + '\n')
