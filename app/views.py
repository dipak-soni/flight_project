from django.shortcuts import render
import os
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from PIL import Image
import pytesseract  # OCR
import cohere
import fitz  # PyMuPDF
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import requests
import time
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path accordingly
# from langchain.llms.openai import OpenAI
from langchain_openai import OpenAI
import shutil
from .image import vision
import csv
from django.conf import settings
import ast
from .json_to_csv import get_csv
from dotenv import load_dotenv 
load_dotenv()

# global variables 
extra=dict()
json_data=[]

def llm_response():
    # if request.method == 'POST':
    # data = json.loads(request.body)
    # user_input=data['user_input']  
    
    directory= str(os.getcwd()).replace('\\','/')+'/app/files'
    # file_names = os.listdir(directory)
    # Specify the directory path
    directory_path = directory

    # List all file paths in the directory
    file_paths = [str(os.path.join(directory_path, f)).replace('\\','/') for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    print(file_paths)
    global json_data
    for file in file_paths:
        
        # file_path=directory+'/'+str(file_names[-1])
        text=save_chunks(file)
        # time.sleep(5)
        response=get_json(text)
        # check_return(text)
        # response=cohere_answer_question(text)
        # # Loop to keep asking questions
        try:
            json_data.append(json.loads(response))
        except:
            pass
       
        # return JsonResponse({'output':response})
    try:
        with open('data.json', 'w') as json_file:
             json.dump(json_data, json_file, indent=4)  # 'indent=4' for pretty formatting
        return json.dumps({"data":json_data})
    except:
        print(json_data)
        print("error occured in assembling json ")




def upload_files(request):

    if request.method == 'POST':
        files = request.FILES.getlist('files')
        upload_dir = os.path.join(os.getcwd(), 'app/files')
        path= upload_dir
        shutil.rmtree(path)
        global json_data
        
        # Create the directory if it does not exist
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        
        for file in files:
            file_path = os.path.join(upload_dir, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        # if file uploaded successfully then call the llm function
        response= llm_response()
        try:
            data=json.loads(response)
            global extra
            extra=data
            template=render(request,'show_details.html',context={'flight':data} )
            # csv_creator(json_data)
            get_csv()
            json_data=[]
            return template
        except:
            print("error occured in data")
            template=render(request,'show_details.html',context={'flight':json_data} )
            # csv_creator(json_data)
            get_csv()
            json_data=[]
            return template

def get_json(text):
    # response=dict()
    # listprompts=['give departure date in json {"departure_date":""}',
    # 'give departure time in json {"departure_time":""}',
    # 'give arrival date in json {"arrival_date":""}',
    # 'give arrival time in json {"arrival_time":""}',
    # 'give arrival location in json {"arrival_location":""}',
    # 'give airline name in json {"airline_name":""}',
    # 'give flight no in json {"flight_no":""}'
    # ]
    # for x in listprompts:
    #     data=cohere_answer_question(x,text)
    #     try:
    #         response.update(json.loads(data))
    #     except:
    #         print('error in ',data)
    # return response
    prompt = f"""
        You are an assistant that returns flight details in JSON format. Based on the document provided below, return the flight details in the following format:
        
        {{
            "single_trip": {{
                "flight_no": ""
                "departure_date":"",
                "departure_time":"",
                "arrival_date":"",
                "arrival_time":"",
                "arrival_location":"",
                "airline_name":""
            }},
            "round_trip": {{
                "flight_no": "",
                "departure_date":"",
                "departure_time":"",
                "arrival_date":"",
                "arrival_time":"",
                "arrival_location":"",
                "airline_name":""
            }}
        }}
        instructions:
        1. If the fields in round-trip information are empty string, exclude the "round_trip" field from response.
        2. If flight_no in round-trip information and flight_no in single trip information is equal then exclude and remove round_trip field.
        Remember to not give any details without having a file do not pridict anything from your own
        Document: {text}
        
        Answer:
    """
    data=opanai_answer(prompt)
    return data


def save_chunks(file):
    if file.endswith('.pdf'):
        doc = fitz.open(file)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    elif file.endswith((".png", ".jpg", ".tiff", ".webp", ".jpeg")):
        text = vision(file)  # Assuming vision() is already defined for image processing
        return text
    else:
        raise ValueError("Unsupported file format")

def show_details(request):
    return render(request,'show_details.html')


def push_json(request):
    if request.method == 'POST':
       if json.loads(request.body)['data']==1:    # print in dict
            response=requests.post('https://webhook.site/74fe7401-3802-4d5d-aab7-9112add794e7',json.dumps(extra))
            return JsonResponse({'data':'pushed'})


def opanai_answer(question):
    os.getenv("OPENAI_API_KEY")
    llm=OpenAI()
    return llm.invoke(question)

# def csv_creator(json_data):
#     csv_file_path='output.csv'
#     # Get the keys from the first dictionary in the JSON data
#     keys = json_data[0].keys()

#     # Write to CSV file
#     with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
#         writer = csv.DictWriter(csv_file, fieldnames=keys)
#         writer.writeheader()  # Write the header
#         writer.writerows(json_data)  # Write the data rows




# def show_csv(request):
           
#     csv_file_path = os.path.join(settings.BASE_DIR, 'output.csv')  # Specify your CSV file path
#     single_trip_data = []
#     round_trip_data = []

#     with open(csv_file_path, mode='r', encoding='utf-8') as file:
#         csv_reader = csv.reader(file)
#         header = next(csv_reader)  # Skip header row
#         for row in csv_reader:
            
#             if not row:  # Skip empty rows
#                 continue
#             if len(row) < 2:  # Ensure there are at least 2 elements
#                 continue

#             try:
#                 single_trip = ast.literal_eval(row[0]) if row[0] else {}
#                 round_trip = ast.literal_eval(row[1]) if row[1] else {}
#                 single_trip_data.append(single_trip)
#                 round_trip_data.append(round_trip)
#             except (SyntaxError, ValueError) as e:
#                 print(f"Error parsing row {row}: {e}")  # Optional: log or print error details

#     context = {
#         'single_trip_data': single_trip_data,
#         'round_trip_data': round_trip_data,
#     }
#     print(context)
#     return render(request, 'show_csv.html', context)



def show_csv(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'flights_data.csv')  # Update with your CSV file path

    # Prepare data to display
    csv_data = []
    
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Read the header row
        
        for row in csv_reader:
            csv_data.append(row)  # Add each row to the data list

    context = {
        'header': header,
        'csv_data': csv_data,
    }
    
    return render(request, 'show_csv.html', context)

