import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get('API_KEY')


def imagine(prompt, n=1, size="1024x1024"):
    response = openai.Image.create(
        prompt=prompt,
        n=n,
        size=size
    )
    return response['data'][0]['url']
