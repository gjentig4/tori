import requests
from bs4 import BeautifulSoup
import csv
import os
import time

base_url = 'https://www.tori.fi/uusimaa/tietokoneet_ja_lisalaitteet/komponentit?ca=18&cg=5030&c=5038&ps=1&st=s&st=k&st=u&st=h&st=g&com=graphic_card&w=1&o='
filename = '123.csv'
processed_links_file = 'processed_links.txt'


def get_item_details(link):
    print(f"Fetching details from {link}")
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title_div = soup.find('div', class_='topic')
        title = title_div.find('h1').text.strip() if title_div else 'Title not found'
        price = soup.find(itemprop='price')
        price = price['content'] if price and price.has_attr('content') else 'Price not found'
        description_div = soup.find('div', class_='body', itemprop='description')
        description = description_div.text.strip() if description_div else 'Description not found'
        print(f"Fetched details: Title - {title}, Price - {price}")
        return {'Title': title, 'Price': price, 'Description': description, 'Link': link}
    else:
        print(f"Failed to retrieve details from {link}: {response.status_code}")
        return {'Title': 'Failed to retrieve', 'Price': 'Failed to retrieve', 'Description': 'Failed to retrieve', 'Link': link}


def scrape_page(url, processed_links):
    print(f"Fetching items from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.select('div.list_mode_thumb a[href]')]
        print(f"Found {len(links)} links")
        items_details = []
        for link in links:
            full_link = 'https://www.tori.fi' + link if not link.startswith('http') else link
            if full_link in processed_links:
                print(f"Skipping already processed link: {full_link}")
                continue
            item_details = get_item_details(full_link)
            items_details.append(item_details)
            processed_links.add(full_link)
            time.sleep(0.5)
        return items_details
    else:
        print(f"Failed to retrieve page {url}: {response.status_code}")
        return []


processed_links = set()
if os.path.exists(processed_links_file):
    with open(processed_links_file, 'r') as f:
        processed_links = set(line.strip() for line in f)

file_exists = os.path.isfile(filename)

with open(filename, 'a', newline='', encoding='utf-8') as file:
    fieldnames = ['Title', 'Price', 'Description', 'Link']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    if not file_exists:
        writer.writeheader()

    # Your other code above ...

# Iterate over the desired range of pages
for page_number in range(2, 5):  # Or any other range you desire
    url = base_url + str(page_number)
    print(f"Scraping page {page_number}")
        
    # Call the function to scrape the page
    items_details_list = scrape_page(url, processed_links)
    
    if not items_details_list:  # Exit the loop if no links are found on the page
        print("No links found on page {page_number}. Exiting.")
        break
    
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['Title', 'Price', 'Description', 'Link']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        for item_details in items_details_list:
            link = item_details.get('Link')
            writer.writerow(item_details)
            processed_links.add(link)
        
    # Save processed links
    with open(processed_links_file, 'w', encoding='utf-8') as f:
        for link in processed_links:
            f.write(f"{link}\n")

print("Scraping Completed.")
