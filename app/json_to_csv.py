import json
import csv
import os
from django.conf import settings

def get_csv():
# Step 1: Load the JSON data from the file
        json_data=os.path.join(settings.BASE_DIR, 'data.json')
        with open(json_data, 'r') as json_file:
            data = json.load(json_file)

        # Step 2: Define the CSV headers (for both single_trip and round_trip)
        csv_headers = [ 'flight_no','passenger name', 'departure_date', 'departure_time' ,'arrival_date'
                    ,'arrival_time'
                    ,'arrival_location'
                    ,'airline_name'
                    ,'return flight_no'
                    ,'return departure_date'
                    ,'return departure_time'
                    ,'return arrival_date'
                    ,'return arrival_time'
                    ,'return arrival_location'
                    ,'return airline_name' 
        ]
        csv_directory=os.path.join(settings.BASE_DIR,'csv_data','')
        
         # List all files in the directory
        files = os.listdir(csv_directory)
        
        # Filter files that match the naming pattern
        csv_files = [f for f in files if f.startswith('flights_data_') and f.endswith('.csv')]
        
         # Find the latest number
        if csv_files:
            # Extract the numbers from the file names and find the maximum
            numbers = [int(f.split('_')[2].split('.')[0]) for f in csv_files]
            next_number = max(numbers) + 1
        else:
            next_number = 1  # If no files, start with 1
            
        # Create the new file name
        csv_file_name = f'flights_data_{next_number}.csv'
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
                    'departure_date': single_trip.get('departure_date', ''),
                    'departure_time': single_trip.get('departure_time', ''),
                    'arrival_date': single_trip.get('arrival_date', ''),
                    'arrival_time': single_trip.get('arrival_time', ''),
                    'arrival_location': single_trip.get('arrival_location', ''),
                    'airline_name': single_trip.get('airline_name', ''),
                    'return flight_no': round_trip.get('flight_no', ''),
                    'return departure_date': round_trip.get('departure_date', ''),
                    'return departure_time': round_trip.get('departure_time', ''),
                    'return arrival_date': round_trip.get('arrival_date', ''),
                    'return arrival_time': round_trip.get('arrival_time', ''),
                    'return arrival_location': round_trip.get('arrival_location', ''),
                    'return airline_name': round_trip.get('airline_name', '')
                })

        # print(f"CSV file {csv_file_name} has been created successfully.")
