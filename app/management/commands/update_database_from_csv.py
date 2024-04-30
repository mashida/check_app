import csv
import os

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import DataError
from app.models import NumberRange
from urllib.parse import urlparse

import pandas as pd
import requests
import urllib3
from bs4 import BeautifulSoup
from tqdm import tqdm

# Disable the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = 'https://opendata.digital.gov.ru/registry/numeric/downloads'

def download_csv(url, download_dir):
    """
    Downloads a CSV file from a given URL and saves it to the specified filename.
    """
    response = requests.get(url, verify=False)

    # Assuming the response is HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <a> tags with href attribute containing ".csv"
    csv_links = [a['href'] for a in soup.find_all('a', href=True) if '.csv' in a['href']]

    print("CSV links found:")
    for link in csv_links:
        print(link)

    # Directory to save the downloaded files
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    for link in csv_links:
        # Parse the URL to get the path component
        parsed_url = urlparse(link)
        # Extract the filename from the path
        filename = os.path.basename(parsed_url.path)
        # Construct the full path to save the file
        file_path = os.path.join(download_dir, filename)

        # Download the file
        response = requests.get(link, verify=False)
        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"Downloaded {filename} to {file_path}")

class Command(BaseCommand):
    help = 'Updates the database from multiple CSV files in a specified directory'

    def handle(self, *args, **options):
        csv_directory = 'csv_data'
        download_csv(URL, csv_directory)
        NumberRange.objects.all().delete()
        self.process_csv_files_in_directory(csv_directory)

    def process_csv_files_in_directory(self, directory):
        # Get all CSV files in the directory
        csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
        for file_name in csv_files:
            file_path = os.path.join(directory, file_name)
            self.update_database_from_csv(file_path)

    def update_database_from_csv(self, file_path):
        # Process the CSV file in chunks
        chunk_size = 1000 # Adjust based on your system's capabilities

        # Iterate through the CSV file in chunks
        for chunk in tqdm(pd.read_csv(file_path, delimiter=';', chunksize=chunk_size), desc=f"processing {file_path}"):
            # Convert numeric fields to integers for each chunk
            chunk.iloc[:, 1] = chunk.iloc[:, 1].astype(int)
            chunk.iloc[:, 2] = chunk.iloc[:, 2].astype(int)
            chunk.iloc[:, 3] = chunk.iloc[:, 3].astype(int)
            chunk.iloc[:, 0] = chunk.iloc[:, 0].astype(int)

            records = []
            for index, row in chunk.iterrows():
                code = row.iloc[0]
                from_number = row.iloc[1]
                to_number = row.iloc[2]
                capacity = row.iloc[3]
                operator = row.iloc[4]
                region = row.iloc[5]
                inn = row.iloc[7]
                territory_gar = row.iloc[6]

                # Create a list of dictionaries to be inserted or updated
                records.append(NumberRange(
                    code=code,
                    from_number=from_number,
                    to_number=to_number,
                    capacity=capacity,
                    operator=operator,
                    region=region,
                    inn=inn,
                    territory_gar=territory_gar
                ))

            # Attempt to bulk create or update records
            try:
                with transaction.atomic():
                    NumberRange.objects.bulk_create(records, ignore_conflicts=True)
            except DataError as e:
                # Log the error and the data causing the issue
                self.stdout.write(self.style.ERROR(f"DataError occurred: {e}"))
                for record in records:
                    if len(record.operator) > 255: # Assuming 'operator' is the field causing the issue
                        self.stdout.write(self.style.ERROR(f"Record with operator exceeding 255 characters: {record.operator}"))
                        # Optionally, you can truncate the data or take other actions here

            # self.stdout.write(self.style.SUCCESS(f'Successfully processed {len(records)} records'))
