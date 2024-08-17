import csv
import os
from enum import Enum
import unicodedata

class PostalCodeColumns(Enum):
    POSTAL_CODE = 0
    CITY = 1
    PROVINCE = 2
    TIMEZONE = 3
    LATITUDE = 4
    LONGITUDE = 5

class PostalCodeData:
    def __init__(self, postal_code, city, province, timezone, latitude, longitude):
        self.postal_code = postal_code
        self.city = city
        self.province = province
        self.timezone = timezone
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"PostalCodeData(city={self.city}, province={self.province}, timezone={self.timezone}, latitude={self.latitude}, longitude={self.longitude})"

def load_postal_codes_to_dict(input_file, limit=100):
    postal_codes_dict = {}
    count = 0

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        
        # Skip the header row
        next(reader)
        
        for row in reader:
            if len(row) < 6:
                continue  # Skip any malformed rows
            
            postal_code = row[PostalCodeColumns.POSTAL_CODE.value].strip()
            city = row[PostalCodeColumns.CITY.value].strip()
            province = row[PostalCodeColumns.PROVINCE.value].strip()
            timezone = row[PostalCodeColumns.TIMEZONE.value].strip()
            latitude = row[PostalCodeColumns.LATITUDE.value].strip()
            longitude = row[PostalCodeColumns.LONGITUDE.value].strip()
            
            postal_codes_dict[postal_code] = PostalCodeData(postal_code, city, province, timezone, latitude, longitude)
            if(limit != None):
                count += 1
                if count >= limit:
                    break

    return postal_codes_dict

def update_csv_files_with_lat_long(cleaned_folder, postal_codes_dict):
    for filename in os.listdir(cleaned_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(cleaned_folder, filename)
            
            with open(file_path, mode='r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                rows = list(reader)
                
                # Add Latitude and Longitude columns to the header
                if 'Latitude' not in rows[0] and 'Longitude' not in rows[0]:
                    header = rows[0] + ['Latitude', 'Longitude']
                    updated_rows = [header]
                else:
                    updated_rows = [rows[0]]

                lat_index = updated_rows[0].index('Latitude')
                long_index = updated_rows[0].index('Longitude')
                address_index = updated_rows[0].index('Address')
                
                for row in rows[1:]:
                    # check if row Latitude and Longitude are already present
                    if(long_index < len(row) and (row[lat_index] != '' and row[long_index] != '')):
                        updated_rows.append(row)
                        continue

                    address = unicodedata.normalize("NFKD", row[address_index].strip())
                    postal_code = address[-7:]  # Assuming postal code is the last part of the address
                    
                    if postal_code in postal_codes_dict:
                        lat = postal_codes_dict[postal_code].latitude
                        long = postal_codes_dict[postal_code].longitude
                    else:
                        lat = ''
                        long = ''
                    
                    modified_row = row.copy()
                    modified_row[address_index] = address

                    if(long_index < len(row)):
                        modified_row[lat_index] = lat
                        modified_row[long_index] = long
                    else:
                        modified_row += [lat, long]
                    updated_rows.append(modified_row)
            
            # Write the updated rows back to the CSV file
            with open(file_path, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(updated_rows)

# Example usage
input_file = 'CanadianPostalCodes202403.csv'
postal_codes_dict = load_postal_codes_to_dict(input_file, None)

cleaned_folder = os.path.join(os.path.dirname(__file__), '..', 'cleaned')
update_csv_files_with_lat_long(cleaned_folder, postal_codes_dict)