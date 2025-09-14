import requests
from bs4 import BeautifulSoup
import os

# List of websites to scrape

`websites = [
‘https://www.mingpao.com’,
#‘https://www.hk01.com’,
# Add more websites here]`

# Directory to save the ads.txt files

output_dir = ‘ads_txt_files’

# Create the output directory if it doesn’t exist

if not os.path.exists(output_dir):
os.makedirs(output_dir)

def scrape_ads_txt(url, output_dir):
try:
response = requests.get(f’{url}/ads.txt’)
if response.status_code == 200:
content = response.text
filename = f’{output_dir}/{url.split(“//”)[1].split(“/”)[0]}.txt’
with open(filename, ‘w’) as file:
file.write(content)
print(f’Successfully saved {filename}‘)
else:
print(f’Failed to retrieve ads.txt from {url}’)
except Exception as e:
print(f’Error: {e}’)

# Scrape ads.txt files from the list of websites

for website in websites:
scrape_ads_txt(website, output_dir)
