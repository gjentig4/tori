import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import schedule

base_url = 'https://www.tori.fi/uusimaa/tietokoneet_ja_lisalaitteet/komponentit?ca=18&cg=5030&c=5038&ps=1&st=s&st=k&st=u&st=h&st=g&com=graphic_card&w=1&o=1'
filename = '123.csv'
processed_links_file = 'processed_links.txt'  # Define the processed_links_file

def get_item_details(link):    
    print(f"Fetching details from {link}")
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Finding the title
        title_div = soup.find('div', class_='topic')
        title = title_div.find('h1').text.strip() if title_div else 'Title not found'
        
        # Finding the price
        price = soup.find(itemprop='price')
        price = price['content'] if price and price.has_attr('content') else 'Price not found'
        
        # Finding the description
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
                continue  # Skip the link if it's already processed.
                
            item_details = get_item_details(full_link)  # Fetch details only for unprocessed link.
            items_details.append(item_details)
            processed_links.add(full_link)  # Add the link to processed_links set after processing.
            time.sleep(0.5)
            
        return items_details
    else:
        print(f"Failed to retrieve page {url}: {response.status_code}")
        return []


# Load processed links
processed_links = set()
if os.path.exists(processed_links_file):
    with open(processed_links_file, 'r') as f:
        processed_links = set(line.strip() for line in f)

item_details_list = scrape_page(base_url, processed_links)  # Pass the processed_links set to the scrape_page function.

file_exists = os.path.isfile(filename)

with open(filename, 'a', newline='', encoding='utf-8') as file:
    fieldnames = ['Title', 'Price', 'Description', 'Link']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    if not file_exists:
        writer.writeheader()
    
    for item_details in item_details_list:
        link = item_details.get('Link')
        writer.writerow(item_details)
        processed_links.add(link)

# Save processed links
with open(processed_links_file, 'w') as f:
    for link in processed_links:
        f.write(f"{link}\n")

print("Scraping Completed.")

