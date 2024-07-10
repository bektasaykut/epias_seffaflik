import requests
import json
import pandas as pd
import os
import platform
from datetime import datetime, timedelta

class RealTimeGenerationFetcher:
    def __init__(self):
        # Define the API details
        self.base_url = "https://seffaflik.epias.com.tr/electricity-service"
        self.endpoint = "/v1/generation/data/realtime-generation"
        self.headers = {
            "Content-Type": "application/json"
        }
        self.url = self.base_url + self.endpoint


    def get_realtime_generation(self, start_date, end_date, powerplant_id):
        request_body = {
            "startDate": start_date,
            "endDate": end_date,
            "powerPlantId": powerplant_id
        }
        response = requests.post(self.url, headers=self.headers, json=request_body)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
            print(response.text)
            return []

    def fetch(self,start_date,end_date,powerplant_id):
        current_start = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S%z")
        final_end = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S%z")
        all_data = []

        while current_start < final_end:
            current_end = min(current_start + timedelta(days=365), final_end)
            print(current_start,current_end)
            data = self.get_realtime_generation(current_start.isoformat(), current_end.isoformat(),powerplant_id)
            all_data.extend(data)
            current_start = current_end

        return all_data

    def save_to_excel(self, data, filename):
        if data:
            df = pd.DataFrame(data)
            df.to_excel(filename, index=False)
            print(f"Data has been saved to {filename}")
            self.open_file(filename)
        else:
            print(data)
            print("No data to save.")

    @staticmethod
    def open_file(filename):
        if platform.system() == "Windows":
            os.startfile(filename)
        elif platform.system() == "Darwin":  # macOS
            os.system(f"open {filename}")
        else:  # Linux and other Unix-like systems
            os.system(f"xdg-open {filename}")



# Define the overall period you want to fetch data for
overall_start_date = "2020-01-01T00:00:00+03:00"
overall_end_date = "2024-01-01T00:00:00+03:00"
excel_filename = "realtime_generation_data.xlsx"
powerplant_id = ""#1076
# Create an instance of RealTimeGenerationFetcher
fetcher = RealTimeGenerationFetcher()

# Fetch data over the defined period
all_generation_data = fetcher.fetch(overall_start_date, overall_end_date,"")

# Save the data to an Excel file and open it
fetcher.save_to_excel(all_generation_data, excel_filename)


