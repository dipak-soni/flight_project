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
        csv_headers = [
            'single_flight_no', 'single_departure_date', 'single_departure_time', 'single_arrival_date',
            'single_arrival_time', 'single_arrival_location', 'single_airline_name',
            'round_flight_no', 'round_departure_date', 'round_departure_time', 'round_arrival_date',
            'round_arrival_time', 'round_arrival_location', 'round_airline_name'
        ]

        # Step 3: Create the CSV file and write the data
        with open(os.path.join(settings.BASE_DIR,'flights_data.csv'), mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
            
            # Write the header
            writer.writeheader()
            
            # Write each JSON object as a row in the CSV
            for flight in data:
                single_trip = flight.get('single_trip', {})
                round_trip = flight.get('round_trip', {})
                
                writer.writerow({
                    'single_flight_no': single_trip.get('flight_no', ''),
                    'single_departure_date': single_trip.get('departure_date', ''),
                    'single_departure_time': single_trip.get('departure_time', ''),
                    'single_arrival_date': single_trip.get('arrival_date', ''),
                    'single_arrival_time': single_trip.get('arrival_time', ''),
                    'single_arrival_location': single_trip.get('arrival_location', ''),
                    'single_airline_name': single_trip.get('airline_name', ''),
                    'round_flight_no': round_trip.get('flight_no', ''),
                    'round_departure_date': round_trip.get('departure_date', ''),
                    'round_departure_time': round_trip.get('departure_time', ''),
                    'round_arrival_date': round_trip.get('arrival_date', ''),
                    'round_arrival_time': round_trip.get('arrival_time', ''),
                    'round_arrival_location': round_trip.get('arrival_location', ''),
                    'round_airline_name': round_trip.get('airline_name', '')
                })

        print("CSV file 'flights_data.csv' has been created successfully.")
