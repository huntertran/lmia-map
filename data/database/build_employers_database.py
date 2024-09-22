import pandas as pd
import os
import re

# Define the path to the "cleaned" folder
cleaned_folder = os.path.join(os.path.dirname(__file__), '..', 'cleaned')

# Define the path to the "data/database" folder
output_folder = os.path.join(os.path.dirname(__file__), '..', 'database')

# Initialize an empty DataFrame to store the results
results_df = pd.DataFrame(columns=['Employer', 'Address', 'Postal Code', 'Province', 'Latitude', 'Longitude'])

# Function to extract postal code from address
def extract_postal_code(address):
    if pd.isna(address):
        return ''
    postal_code_pattern = r'\b[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d\b'
    match = re.search(postal_code_pattern, address)
    return match.group(0) if match else ''

# Loop through each CSV file in the "cleaned" folder
for filename in os.listdir(cleaned_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(cleaned_folder, filename)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Extract the required columns and postal code
        if all(col in df.columns for col in ['Employer', 'Address', 'Province', 'Latitude', 'Longitude']):
            df['Postal Code'] = df['Address'].apply(extract_postal_code)
            extracted_df = df[['Employer', 'Address', 'Postal Code', 'Province', 'Latitude', 'Longitude']]
            
            # Append the extracted data to the results DataFrame
            results_df = pd.concat([results_df, extracted_df], ignore_index=True)

# Exclude all employers without an address
results_df = results_df[results_df['Address'].notna() & (results_df['Address'] != '')]

# Convert 'Employer' and 'Postal Code' to lowercase for duplicate removal
results_df['Employer_lower'] = results_df['Employer'].str.lower()
results_df['Postal Code_lower'] = results_df['Postal Code'].str.lower()

# Remove duplicates based on 'Employer_lower' and 'Postal Code_lower' columns
results_df.drop_duplicates(subset=['Employer_lower', 'Postal Code_lower'], inplace=True)

# Drop the temporary lowercase columns
results_df.drop(columns=['Employer_lower', 'Postal Code_lower'], inplace=True)

# Add an ID column with unique identifiers for each employer
results_df.insert(0, 'ID', range(1, len(results_df) + 1))

# Save the results DataFrame to a new CSV file
output_file_path = os.path.join(output_folder, 'all_employers.csv')
results_df.to_csv(output_file_path, index=False)