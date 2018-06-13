from bs4 import BeautifulSoup
import requests

BASE_URL = "https://en.wikipedia.org"
PAGE_TO_SCRAPE = "/wiki/Lists_of_foods"
TARGET_ID = "bodyContent"
OUTPUT_FILE = "foods.txt"

def get_data(url):
    return requests.get(BASE_URL + url).text

def get_links(start_url):
    soup = BeautifulSoup(get_data(start_url), "html.parser")

    return soup.find_all('a')

def get_lists(links):
    urls = []
    for link in links:
        if link.get_text()[:7] == "List of":
            urls.append(link.get("href"))

    return urls

def scrape_urls(list_urls, elem_id):
    table_data = []
    
    for list_item in list_urls:
        soup = BeautifulSoup(get_data(list_item), "html.parser")
        content = soup.find(id = elem_id)
        table_data.append(content.find_all('td'))

    return table_data

def remove_duplicates(list_data):
    unique_items = set()
    
    for row in list_data:
        for cell in row:
            for string in cell.stripped_strings:
                unique_items.add(string)

    return unique_items

def write_list_to_file(list_data, file_name):
    f = open(file_name, "wt", encoding="utf-8")

    for string in list_data:
        f.write(string + "\n")

    f.close()

def scraper():
    links = get_links(PAGE_TO_SCRAPE)
    urls = get_lists(links)
    raw_data = scrape_urls(urls, TARGET_ID)
    unique_data = remove_duplicates(raw_data)
    write_list_to_file(unique_data, OUTPUT_FILE)

if __name__ == '__main__':
    scraper()
