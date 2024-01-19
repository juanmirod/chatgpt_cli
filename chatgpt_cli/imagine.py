import os
import requests
import argparse
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def imagine(prompt, output=None, n=1, size="1024x1024"):
    if output is None:
        output = f"images/imagine_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=n,
    )
    image = requests.get(response.data[0].url)

    with open(output, "wb") as f:
        f.write(image.content)
    return (response.data[0].revised_prompt, "Image downloaded successfully!")


def main():
    # Create the arguments parser
    default_output_file = f"images/imagine_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    parser = argparse.ArgumentParser(
        description="Generate an image given a prompt.")
    parser.add_argument(
        'prompt',
        type=str,
        help='The prompt used to generate the image.')
    parser.add_argument('-o', '--output', type=str,
                        default=default_output_file,
                        help='The output file to write to. Defaults to "images/imagine_yyyymmdd_hhmmss.mp3".')
    
    # Parse the arguments
    args = parser.parse_args()
    (revised_prompt, msg) = imagine(args.prompt, args.output)
    print(revised_prompt)
    print(msg)


if __name__ == '__main__':
    main()
