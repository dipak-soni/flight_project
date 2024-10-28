from django.shortcuts import render,redirect
import os
from django.http import JsonResponse,FileResponse
import json
import fitz 
from langchain_community.llms import OpenAI
import requests
import time
from langchain_openai import OpenAI
import shutil
from .image import vision
import csv
from django.conf import settings
from .json_to_csv import get_csv
from .models import *
import openai
from langchain_anthropic import AnthropicLLM
from dotenv import load_dotenv 
load_dotenv()

# global variables 
json_data=[]
form_data=[]

def llm_response():
    # get the directory of the files where pdfs and images are stored
    directory= str(os.getcwd()).replace('\\','/')+'/app/files'
    directory_path = directory
    
    # List all file paths in the directory
    file_paths = [str(os.path.join(directory_path, f)).replace('\\','/') for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    # this is the global variable that will hold all the json data
    global json_data
    for file in file_paths:
        
        # Read the file one by one
        text=save_chunks(file)
        
        # get respones from llm in json form 
        response=get_json(text)
        try:
            json_data.append(json.loads(response))
        except:
            pass
       
    try:
        # save the json data to a data.json file
        with open('data.json', 'w') as json_file:
             json.dump(json_data, json_file, indent=4)  # 'indent=4' for pretty formatting
        # return json.dumps({"data":json_data})
    except:
        print(json_data)
        print("error occured in assembling json ")


# this function will return the llm response in json format
def get_json(text):
    prompt = f"""
        You are an assistant that returns flight details in JSON format. Based on the document provided below, return the flight details in the following format:
        
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
        1. If you do not get return ticket informations then simply exclude the "round_trip" field from json.
        2. If flight_no in round-trip field and flight_no in single trip field is exact equal then exclude the round_trip field from json.
        3. If the document has multiple flight ticket infomations then use first flight ticket detail to extract single_trip field and the last flight ticket detail to extract round_trip field.
        4. If you do not find any value of a particular filed then you can place N/A in place of empty string. 
        5. If the arrival_time in single_trip field and departure_time in round_trip field is same then exclude the round_trip field from json.
        6. If you do not find flight_no in any field then simply exclude that field from json.
        Document: {text}
        
        Answer:
    """
    data=opanai_answer(prompt)
    # print(data)
    return data



# this function reads the text from a PDF or image file and returns the text content as a string
def save_chunks(file):
    if file.endswith('.pdf'):
        doc = fitz.open(file)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    elif file.endswith((".png", ".jpg", ".tiff", ".webp", ".jpeg")):
        text = vision(file)  # calling OpenAI Vision API to extract text from images
        return text
    else:
        raise ValueError("Unsupported file format")




def opanai_answer(question):
    os.getenv("OPENAI_API_KEY")
    llm=OpenAI()
    # llm = AnthropicLLM()
    try:
        return llm.invoke(question)
    except:
        print("open ai error occurred")
        JsonResponse({"error": "Unable to connect"}, status=500)
   

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


# show csv file to user
def show_csv(request):
    directory = os.path.join(settings.BASE_DIR, 'csv_data','')
      # List all files in the directory
    files = os.listdir(directory)
    
    # Filter files that match the naming pattern
    csv_files = [f for f in files if f.startswith('flights_data_') and f.endswith('.csv')]
    
        # Find the latest number
    if csv_files:
        # Extract the numbers from the file names and find the maximum
        numbers = [int(f.split('_')[2].split('.')[0]) for f in csv_files]
        next_number = max(numbers) 
    else:
        next_number = 1  # If no files, start with 1
        
    # Create the new file name
    csv_file_name = f'flights_data_{next_number}.csv'
    csv_file_path = os.path.join(directory, csv_file_name)
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


def download_csv(request):
    directory = os.path.join(settings.BASE_DIR, 'csv_data','')
      # List all files in the directory
    files = os.listdir(directory)
    
    # Filter files that match the naming pattern
    csv_files = [f for f in files if f.startswith('flights_data_') and f.endswith('.csv')]
    
        # Find the latest number
    if csv_files:
        # Extract the numbers from the file names and find the maximum
        numbers = [int(f.split('_')[2].split('.')[0]) for f in csv_files]
        next_number = max(numbers) 
    else:
        next_number = 1  # If no files, start with 1
        
    # Create the new file name
    csv_file_name = f'flights_data_{next_number}.csv'
    csv_file_path = os.path.join(directory, csv_file_name)
    
    # Serve the file as a download
    response = FileResponse(open(csv_file_path, 'rb'), as_attachment=True, filename='flights_data.csv')
    return response


# login page
def formView(request):
    return render(request, 'form.html')


# get login data from user
def getFormData(request):
    if request.method == 'POST':
        travel_entry_id = request.POST['iTravelEntryID']
        event_id = request.POST['iEventID']
        planner_id = request.POST['iPlannerID']
        user_id = request.POST['iUserID']
        files = request.FILES.getlist('fileUploads')
        request.session['travel_entry_id'] = travel_entry_id
        f_data={'travel_entry_id': travel_entry_id, 'event_id': event_id, 'planner_id': planner_id, 'user_id': user_id}
        form_data.append(f_data)
        # print(form_data)
    
        # get the path of pdf files and images stored
        upload_dir = os.path.join(os.getcwd(), 'app/files')
        path= upload_dir
        
        # remove the existing files in the directory before uploading new ones
        shutil.rmtree(path)
        global json_data
        
        # Create the directory that was deleted before
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        
        # get file from form upload and write to the directory
        for file in files:
            file_path = os.path.join(upload_dir, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
          
        # if file uploaded successfully then call the llm function
        response= llm_response()
        with open('data.json', 'r') as f:
            data = json.load(f)
            data=json.dumps(data)
        try:
            template=render(request,'main.html',context={"data":data})
            # csv_creator(json_data)
            get_csv()
            json_data=[]
            return template
        except:
            print("error occured in data")
            template=render(request,'main.html',context={'data':data} )
            # csv_creator(json_data)
            get_csv()
            json_data=[]
            return template
    elif request.method == 'GET':
        return render(request, 'form.html')
       


# push to webhook api
def push_webhook(request):
    with open('data.json', 'r') as f:
        data = json.load(f)
    data=json.dumps(data)
    requests.post('https://webhook.site/74fe7401-3802-4d5d-aab7-9112add794e7',data)
    return render(request,'main.html',context={"data":'pushed to webhook successfully'})



def database(request):
    # data=[{'travel_entry_id': '123', 'event_id': 'ghgh', 'planner_id': 'gg', 'user_id': 'gg'}]
    data=form_data
    user=User.objects.filter(travel_entry_id=data[0]['travel_entry_id'])
    if not user:
        user=User()
        user.travel_entry_id=data[0]['travel_entry_id']
        user.save()  
    user=User.objects.get(travel_entry_id=data[0]['travel_entry_id'])

    with open('data.json', 'r') as f:
        file_dta = json.load(f)
    print(file_dta)
    for x in file_dta:
        if 'single_trip' in x:
            # t=Ticket.objects.filter(event_id=data[0]['event_id'], ticket_type='single')
            # if not t:
                ticket=Ticket()
                ticket.travel_entry_id=user
                ticket.event_id=data[0]['event_id']
                ticket.planner_id=data[0]['planner_id']
                ticket.user_id=data[0]['user_id']
                
                y=x['single_trip']
                ticket.passenger_name=y['passenger_name']
                ticket.flight_no=y['flight_no']
                ticket.source_location=y['source_location']
                ticket.departure_date=y['departure_date']
                ticket.departure_time=y['departure_time']
                ticket.arrival_date=y['arrival_date']
                ticket.arrival_time=y['arrival_time']
                ticket.arrival_location=y['arrival_location']
                ticket.airline_name=y['airline_name']
                ticket.ticket_type='single'
                ticket.save()
        if 'round_trip' in x:
            # t=Ticket.objects.filter(event_id=data[0]['event_id'], ticket_type='round')
            # if not t:
                ticket=Ticket()
                ticket.travel_entry_id=user
                ticket.event_id=data[0]['event_id']
                ticket.planner_id=data[0]['planner_id']
                ticket.user_id=data[0]['user_id']
                
                y=x['round_trip']
                ticket.passenger_name=y['passenger_name']
                ticket.flight_no=y['flight_no']
                ticket.source_location=y['source_location']
                ticket.departure_date=y['departure_date']
                ticket.departure_time=y['departure_time']
                ticket.arrival_date=y['arrival_date']
                ticket.arrival_time=y['arrival_time']
                ticket.arrival_location=y['arrival_location']
                ticket.airline_name=y['airline_name']
                ticket.ticket_type='round'
                ticket.save()
    return render(request,'main.html',context={"data":'Pushed to database successfully'})



 





    