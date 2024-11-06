import json
import csv
import os
from django.conf import settings
import shutil

def get_csv():
# Step 1: Load the JSON data from the file
        json_data=os.path.join(settings.BASE_DIR, 'data.json')
        with open(json_data, 'r') as json_file:
            data = json.load(json_file)

        # Step 2: Define the CSV headers (for both single_trip and round_trip)
        csv_headers = [ 
                    'flight_no'
                    ,'passenger name'
                    ,'source_location'
                    ,'departure_date'
                    ,'departure_time'
                    ,'arrival_date'
                    ,'arrival_time'
                    ,'arrival_location'
                    ,'airline_name'
                    ,'return flight_no'
                    ,'return departure_date'
                    , 'return source_location'
                    ,'return departure_time'
                    ,'return arrival_date'
                    ,'return arrival_time'
                    ,'return arrival_location'
                    ,'return airline_name' 
        ]
        csv_directory=os.path.join(settings.BASE_DIR,'csv_data')
        path= csv_directory
        
        # remove the existing files in the directory before uploading new ones
        shutil.rmtree(path) 
        # Create the directory that was deleted before
        if not os.path.exists(csv_directory):
            os.makedirs(csv_directory)
            
        # Create the new file name
        csv_file_name = 'flights_data.csv'
        csv_file_path = os.path.join(csv_directory, csv_file_name)
        
        # Step 3: Create the CSV file and write the data
        with open(os.path.join(csv_directory,csv_file_path), mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
            
            # Write the header
            writer.writeheader()
            
            # Write each JSON object as a row in the CSV
            for flight in data:
                single_trip = flight.get('single_trip', {})
                round_trip = flight.get('round_trip', {})
                
                writer.writerow({
                    'flight_no': single_trip.get('flight_no', ''),
                    'passenger name':single_trip.get('passenger_name', ''),
                    'source_location':single_trip.get('source_location', ''),
                    'departure_date': single_trip.get('departure_date', ''),
                    'departure_time': single_trip.get('departure_time', ''),
                    'arrival_date': single_trip.get('arrival_date', ''),
                    'arrival_time': single_trip.get('arrival_time', ''),
                    'arrival_location': single_trip.get('arrival_location', ''),
                    'airline_name': single_trip.get('airline_name', ''),
                    'return flight_no': round_trip.get('flight_no', ''),
                    'return source_location': round_trip.get('source_location', ''),
                    'return departure_date': round_trip.get('departure_date', ''),
                    'return departure_time': round_trip.get('departure_time', ''),
                    'return arrival_date': round_trip.get('arrival_date', ''),
                    'return arrival_time': round_trip.get('arrival_time', ''),
                    'return arrival_location': round_trip.get('arrival_location', ''),
                    'return airline_name': round_trip.get('airline_name', '')
                })

        # print(f"CSV file {csv_file_name} has been created successfully.")
