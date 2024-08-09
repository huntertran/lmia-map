import json
import requests
import os

# Load JSON data from file
with open('all.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Function to download a file from a URL
def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    local_filename = os.path.join(dest_folder, url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

# Iterate through the JSON objects and download .csv and .xlsx files
for item in data['result']['resources']:
    url = item.get('url')
    if url and (url.endswith('.csv') or url.endswith('.xlsx')):
        print(f"Downloading {url}")
        download_file(url, 'downloads')

print("Download completed.")