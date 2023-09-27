import requests
from bs4 import BeautifulSoup
import csv
import os
import time

base_url = 'https://www.tori.fi/uusimaa/tietokoneet_ja_lisalaitteet/komponentit?ca=18&cg=5030&c=5038&ps=1&st=s&st=k&st=u&st=h&st=g&com=graphic_card&w=1&o=1'
filename = 'tori_fi_GPUs_descriptions.csv'

def get_description(link):
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        description = soup.find('div', class_='body', itemprop='description')
        return description.text.strip() if description else 'Description not found'
    else:
        print(f"Failed to retrieve description from {link}: {response.status_code}")
        return 'Failed to retrieve description'

def scrape_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.select('div.list_mode_thumb a[href]')]
        
        descriptions = []
        for link in links:
            full_link = 'https://www.tori.fi' + link if not link.startswith('http') else link
            descriptions.append(get_description(full_link))
            time.sleep(3)
        return descriptions
    else:
        print(f"Failed to retrieve page {url}: {response.status_code}")
        return []

file_exists = os.path.isfile(filename)

with open(filename, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(['Description'])
    descriptions = scrape_page(base_url)
    for description in descriptions:
        writer.writerow([description])
