from bs4 import BeautifulSoup
import requests

BASE_URL = "https://en.wikipedia.org"
OUTPUT_FILE = "foods.txt"

def get_data(url):
    return requests.get(BASE_URL + url).text
    
def get_links(start_url):
    soup = BeautifulSoup(get_data(start_url), "html.parser")

    return soup.find_all('a')

# Get all anchor tags
links = get_links("/wiki/Lists_of_foods")

list_urls = []
for link in links:
    if link.get_text()[:7] == "List of":
        list_urls.append(link.get("href"))

f = open(OUTPUT_FILE, "w", encoding="utf-8")

for food_list in list_urls:
    soup = BeautifulSoup(get_data(food_list), "html.parser")
    content = soup.find(id = "bodyContent")
    data = content.find_all('td')
    
    for cell in data:
        for string in cell.stripped_strings:
            f.write(string + "\n")
        
f.close()
