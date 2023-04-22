import openai
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get('API_KEY')


def imagine(prompt, n=1, size="1024x1024"):
    response = openai.Image.create(
        prompt=prompt,
        n=n,
        size=size
    )
    response = requests.get(response['data'][0]['url'])

    with open(f"images/{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg", "wb") as f:
        f.write(response.content)
    return "Image downloaded successfully!"
