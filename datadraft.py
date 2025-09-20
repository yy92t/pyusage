import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website to scrape
url = ‘https://en.wikipedia.org/wiki/List_of_companies_listed_on_the_Hong_Kong_Stock_Exchange’

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
# Parse the HTML content of the page
soup = BeautifulSoup(response.text, ‘html.parser’)

# Example: Extract data from a table
table = soup.find('table')
headers = [header.text for header in table.find_all('th')]
rows = []

for row in table.find_all('tr')[1:]:
    cells = row.find_all('td')
    data = [cell.text.strip() for cell in cells]
    rows.append(data)

# Create a DataFrame and save it to a CSV file
df = pd.DataFrame(rows, columns=headers)
df.to_csv('output.csv', index=False)

print("Data has been scraped and saved to output.csv")

else:
print(f”Failed to retrieve the webpage. Status code: {response.status_code}“)
