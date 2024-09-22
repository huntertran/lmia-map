import re
import csv
import os

# build for 2014

# Step 0: Define the path to the "data/database" folder
database_folder = os.path.join(os.path.dirname(__file__), '..', 'database')
cleaned_folder = os.path.join(os.path.dirname(__file__), '..', 'cleaned')
all_employers_file = os.path.join(database_folder, 'all_employers.csv')

# Step 1: Build the hashmap from all_employers.csv
employer_map = {}
with open(all_employers_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        key = (row['Employer'].strip().lower(), row['Postal Code'].strip().lower())
        employer_map[key] = row

# Function to extract postal code from address
def extract_postal_code(address):
    postal_code_pattern = r'\b[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d\b'
    match = re.search(postal_code_pattern, address)
    return match.group(0) if match else ''

def build_modified_rows(file_name, data_map, employer_column_id, address_column_id, position_column_id, latitude_column_id, longitude_column_id):
    with open(os.path.join(cleaned_folder, file_name), mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header

        for row in reader:
            employer = row[employer_column_id].strip().lower()
            postal_code = extract_postal_code(row[address_column_id]).lower()
            key = (employer, postal_code)
            employer_id = employer_map.get(key, None)

            if employer_id:
                modified_row = {
                    'EmployerID': employer_id.get('ID'),
                    'Position': row[position_column_id],
                    'Latitude': row[latitude_column_id],
                    'Longitude': row[longitude_column_id]
                }

                if(not modified_row['Latitude'] and not modified_row['Longitude']):
                    continue

                # get employer id as a key
                employer_id_key = employer_id.get('ID')
                # check if employer is already in the data_map
                if employer_id_key in data_map:
                    existing_row = data_map[employer_id_key]
                    existing_row['Position'] = int(existing_row['Position']) + int(modified_row['Position'])
                else:
                    data_map[employer_id_key] = modified_row

def build_geo_database(file_names, employer_column_id, address_column_id, position_column_id, latitude_column_id, longitude_column_id):
    modified_rows = []
    data_map = {}

    for file_name in file_names:
        build_modified_rows(file_name, data_map, employer_column_id, address_column_id, position_column_id, latitude_column_id, longitude_column_id)

    modified_rows = sorted(data_map.values(), key=lambda x: int(x['EmployerID']))
    combined_file_name = ''
    if '_' in file_names[0]:
        combined_file_name = file_names[0].split('_')[0] + '.csv'
    else:
        combined_file_name = file_names[0]

    # Step 3: Write the modified data to a new CSV file
    with open(os.path.join(database_folder, combined_file_name), mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['EmployerID', 'Position', 'Latitude', 'Longitude']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(modified_rows)

# build_geo_database(['2014.csv'], 0, 1, 2, 4, 5)
# build_geo_database(['2015.csv'], 0, 1, 2, 4, 5)

# Province,Employer,Address,Positions,NOC 2011,NOC Name,Latitude,Longitude
# build_geo_database(['2016.csv'], employer_column_id=1, address_column_id=2, position_column_id=3, latitude_column_id=6, longitude_column_id=7)

# Province,Employer,Address,Positions,Stream,NOC 2011,NOC Name,Latitude,Longitude
build_geo_database(['2017_06.csv', '2017_09.csv', '2017_12.csv'], employer_column_id=1, address_column_id=2, position_column_id=3, latitude_column_id=7, longitude_column_id=8)

# Province,Employer,Address,Positions,Stream,NOC 2011,NOC Name,Latitude,Longitude
build_geo_database(['2018_03.csv', '2018_06.csv', '2018_09.csv', '2018_12.csv'], employer_column_id=1, address_column_id=2, position_column_id=3, latitude_column_id=7, longitude_column_id=8)

# Province,Employer,Address,Positions,Stream,NOC 2011,NOC Name,Latitude,Longitude
build_geo_database(['2019_03.csv', '2019_06.csv', '2019_09.csv', '2019_12.csv'], employer_column_id=1, address_column_id=2, position_column_id=3, latitude_column_id=7, longitude_column_id=8)

# Province,Employer,Address,Positions,Stream,NOC 2011,NOC Name,Latitude,Longitude
build_geo_database(['2020_03.csv', '2020_09.csv'], employer_column_id=1, address_column_id=2, position_column_id=3, latitude_column_id=7, longitude_column_id=8)

# Province,Employer,Address,Positions,Stream,NOC 2011,NOC Name,Latitude,Longitude
build_geo_database(['2021_06.csv', '2021_09.csv'], employer_column_id=1, address_column_id=2, position_column_id=3, latitude_column_id=7, longitude_column_id=8)

# Province,Employer,Address,Positions,Stream,NOC 2011,NOC Name,Incorporated Status,Approved LMIA,Latitude,Longitude
build_geo_database(['2022_03.csv', '2022_06.csv', '2022_09.csv', '2022_12.csv'], employer_column_id=1, address_column_id=2, position_column_id=8, latitude_column_id=9, longitude_column_id=10)

# Province,Employer,Address,Positions,Stream,NOC 2011,NOC Name,Incorporated Status,Approved LMIA,Latitude,Longitude
build_geo_database(['2023_03.csv', '2023_06.csv', '2023_09.csv', '2023_12.csv'], employer_column_id=1, address_column_id=2, position_column_id=8, latitude_column_id=9, longitude_column_id=10)