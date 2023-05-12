from openai import ChatCompletion


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
