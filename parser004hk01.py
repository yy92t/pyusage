import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote

def fetch_and_parse(url):
response = requests.get(url)
response.raise_for_status() # Check for request errors
soup = BeautifulSoup(response.content, ‘html.parser’)
return soup

def extract_and_decode_links(soup, base_url):
links = []
for a_tag in soup.find_all(‘a’, href=True):
link = urljoin(base_url, a_tag[‘href’])
decoded_link = unquote(link) # Decode the URL
links.append(decoded_link)
return links

def main():
url = ‘https://www.scmp.com’
soup = fetch_and_parse(url)
links = extract_and_decode_links(soup, url)

```
# Display links in chronological order (assuming they are in order of appearance)
for link in links:
    print(link)
```

if **name** == “**main**”:
main()

# Define the content you want to save

`#content = links`

# Open a file in write mode

`#with open(“output.txt”, “w”) as file:
# Write the content to the file
#file.write(content)`

`#print(“File saved successfully!”)`
