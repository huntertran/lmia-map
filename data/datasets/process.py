# import os

# # Define the directory to search
# directory = 'downloads'

# # Iterate through the files in the directory
# for filename in os.listdir(directory):
#     if filename.endswith('_fr.csv') or filename.endswith('_fr.xlsx'):
#         file_path = os.path.join(directory, filename)
#         try:
#             os.remove(file_path)
#             print(f"Deleted {file_path}")
#         except Exception as e:
#             print(f"Error deleting {file_path}: {e}")

# print("Deletion process completed.")

import csv
import os

# Define the input file path
input_file = 'downloads/positive_employers_en.csv'
temp_file = 'downloads/temp_positive_employers_en.csv'

# Read the CSV file and filter out empty rows
with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
     open(temp_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    for row in reader:
        if any(field.strip() for field in row):  # Check if the row is not empty
            writer.writerow(row)

# Replace the original file with the cleaned file
os.replace(temp_file, input_file)

print("Empty rows removed and cleaned data saved to", input_file)