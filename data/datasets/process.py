# change encoding format of all csv

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

import os
import chardet

def detect_file_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def remove_empty_lines_from_csv(file_path):
    # encoding = detect_file_encoding(file_path)
    encoding = "utf-8"

    print(f"Processing {file_path}")
    
    with open(file_path, 'r', encoding=encoding) as file:
        lines = file.readlines()
    
    non_empty_lines = [line for line in lines if line.strip() != '']
    
    with open(file_path, 'w', encoding=encoding) as file:
        file.writelines(non_empty_lines)

def process_all_csv_files():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(current_directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(current_directory, filename)
            remove_empty_lines_from_csv(file_path)

# Process all CSV files in the current directory
process_all_csv_files()
