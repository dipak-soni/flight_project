import base64
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# Function to handle image vision task
def vision(file):
    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Encoding the provided image file
    base64_image = encode_image(file)

    # Making the API request to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "retrive all teh text of the given image",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":  f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
    )

    # Returning the model's response

    return response.choices[0]

# # Example usage
# file_path = "/home/raghav/Downloads/15_flight_project/home/app/files/Screenshot from 2024-10-22 17-26-03.png"
# result = vision(file_path)
# print(result)
