import os
import requests
import argparse
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def variant(original, output):
    response = client.images.create_variation(
        image=open(original, "rb"),
        n=1,
        size="512x512",
    )

    image = requests.get(response.data[0].url)
    with open(output, "wb") as f:
        f.write(image.content)

    return "Image downloaded successfully!"

def main():
    # Create the arguments parser
    default_output_file = f"images/variant_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    parser = argparse.ArgumentParser(
        description="Takes an image file and returns a variation of the image.")
    parser.add_argument(
        'input_file',
        type=str,
        help='The input file to process.')
    parser.add_argument('-o', '--output', type=str,
                        default=default_output_file,
                        help='The output file to write to. Defaults to "images/variant_yyyymmdd_hhmmss.mp3".')
    
    # Parse the arguments
    args = parser.parse_args()
    variant(args.input_file, args.output)

    
if __name__ == '__main__':
    main()
