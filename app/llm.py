from dotenv import load_dotenv
import os

load_dotenv()
from openai import OpenAI

def llm_res(text,airport_code):
    client = OpenAI(api_key=os.getenv('OPENAI_KEY_KEY'))

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are an assistant that returns flight details in JSON format. Based on the document provided below, return the flight details in the following format:
            
            {{
                "single_trip": {{
                    "flight_no": "",
                    "passenger_name":"",
                    "source_location":"",
                    "departure_date":"",
                    "departure_time":"",
                    "arrival_date":"",
                    "arrival_time":"",
                    "arrival_location":"",
                    "airline_name":""
                }},
                "round_trip": {{
                    "flight_no": "",
                    "passenger_name":"",
                    "source_location":"",
                    "departure_date":"",
                    "departure_time":"",
                    "arrival_date":"",
                    "arrival_time":"",
                    "arrival_location":"",
                    "airline_name":""
                }}
            }}
            Instructions:
            1. If you get only single trip information from the context then only provide single_trip field in json.
            2. If you get both single trip and round trip inforamtions from the context then include both single_trip and round_trip field in Json.
            3. If you get only round trip information from the context then only provide round_trip field in json.
            4. You have to figure out the correct airport city using airport code provided by user, retreive airport name from airport_code and get the airport city wher this airport is located.
            5. If you got the airport city then you have to extract the details for single_trip field( above written json field ) where source_location is that either airport city or that airport name and extract the round_trip field(above written json field) where arrival_location is the either airport city or airport name.
            6. source_location in single_trip field and arrival_location should be equal.
            
            Answer query from user question
            
            Answer:
        """
            },
            {
            "role":"user",
            "content":text
            },
            {
            "role":"user",
            "content":"This is airport code "+airport_code
            }
            
        ]
    )
    return completion.choices[0].message.content

