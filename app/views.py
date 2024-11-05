from django.shortcuts import render,redirect
import os
from django.http import JsonResponse,FileResponse
import json
import fitz 
import requests
import time
import shutil
from .image import vision
import csv
from django.conf import settings
from .json_to_csv import get_csv
from .models import User,Ticket
from .llm import llm_res
import re
from dotenv import load_dotenv 
load_dotenv()

# global variables 
json_data=[]
form_data=[]

def llm_response(airport_code):
    # get the directory of the files where pdfs and images are stored
    directory= str(os.getcwd()).replace('\\','/')+'/app/files'
    directory_path = directory
    
    # List all file paths in the directory
    file_paths = [str(os.path.join(directory_path, f)).replace('\\','/') for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    # this is the global variable that will hold all the json data
    global json_data
    for file in file_paths:
        # time.sleep(10)
        # Read the file one by one
        text=save_chunks(file)
        # get respones from llm in json form 
        response=get_json(text,airport_code)
        try:
            json_data.append(response)
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
def get_json(text,airport_code):
    data=llm_res(text,airport_code)
    
    # Regex pattern to match the JSON data
    pattern = r'\{.*\}'

    # Search for the JSON part
    match = re.search(pattern, data, re.DOTALL)

    # Extract the JSON data if a match is found
    if match:
        json_d = match.group(0)
        json_d=json.loads(json_d)
        return json_d
    else:
        print("No JSON data found.")
        return None


# this function reads the text from a PDF or image file and returns the text content as a string
def save_chunks(file):
    if file.endswith('.pdf'):
        doc = fitz.open(file)
        text = ""
        for page in doc:
            text += page.get_text()
        # if pdf is not selectable
        if len(text)==0:
            print("PDF is not selectable.")
                   
        return text
    elif file.endswith((".png", ".jpg", ".tiff", ".webp", ".jpeg")):
        text = vision(file)  # calling OpenAI Vision API to extract text from images
        return text
    else:
        raise ValueError("Unsupported file format")
   


# show csv file to user
def show_csv(request):
    directory = os.path.join(settings.BASE_DIR, 'csv_data')
    csv_file_path = os.path.join(directory, 'flights_data.csv')
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
    csv_file_path = os.path.join(directory, 'flights_data.csv')
    
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
        airport_code=request.POST['airportCode']
        files = request.FILES.getlist('fileUploads')
        request.session['travel_entry_id'] = travel_entry_id
        f_data={'travel_entry_id': travel_entry_id, 'event_id': event_id, 'planner_id': planner_id, 'user_id': user_id,'airport_code': airport_code}
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
        try:
            llm_response(airport_code)
        except Exception as e:
            print(e)
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
    requests.post(os.getenv('POST_API_URL'),data)
    return render(request,'main.html',context={"data":'pushed to webhook successfully'})



def database(request):
    # data=[{'travel_entry_id': '123', 'event_id': 'ghgh', 'planner_id': 'gg', 'user_id': 'gg'}]
    data=form_data
    print(data)
    try:
        user=User.objects.filter(travel_entry_id=data[0]['travel_entry_id'])
        if not user:
            user=User()
            user.travel_entry_id=data[0]['travel_entry_id']
            user.save()  
        user=User.objects.get(travel_entry_id=data[0]['travel_entry_id'])

        with open('data.json', 'r') as f:
            file_dta = json.load(f)
        for x in file_dta:
            if 'single_trip' in x:
                # t=Ticket.objects.filter(event_id=data[0]['event_id'], ticket_type='single')
                # if not t:
                    ticket=Ticket()
                    ticket.travel_entry_id=user
                    ticket.event_id=data[0]['event_id']
                    ticket.planner_id=data[0]['planner_id']
                    ticket.user_id=data[0]['user_id']
                    ticket.airport_code=data[0]['airport_code']
                    
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
                    ticket.airport_code=data[0]['airport_code']
                    
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
    
    except Exception as e:
        print(e)
        return render(request, 'main.html',context={"data":"error while pushing"})



 





    