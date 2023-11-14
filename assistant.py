from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def chat_completion(system, messages, temperature, model="gpt-3.5-turbo",
                    functions=None
                    ):
    try:
        result = execute(system, messages, functions, temperature, model)
    except Exception as e:
        result = (str(e), 0)
    return result


def execute(system, messages, functions=None, temperature=0.2, model="gpt-3.5-turbo"):
    system_message = {"role": "system", "content": system}
    if functions is None:
        completion = client.chat.completions.create(
            model=model,
            messages=[system_message] + messages,
            temperature=temperature
        )
    else:
        completion = client.chat.completions.create(
            model=model,
            messages=[system_message] + messages,
            temperature=temperature,
            functions=functions
        )
    response = completion.choices[0].message.content
    total_tokens = completion.usage.total_tokens
    return (response, total_tokens)


# def memorize(text):
#     response = Embedding.create(
#         engine="text-embedding-ada-002",
#         input=text
#     )
#     new_embedding = {"text": text, "embedding": response["data"][0]["embedding"]}
#     with open("db/tmp_db_rows.md", "a") as f:
#         f.write(json.dumps(new_embedding) + '\n')
