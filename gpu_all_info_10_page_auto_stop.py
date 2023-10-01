from datetime import datetime  # Importing datetime to record when the details were fetched
import requests
from bs4 import BeautifulSoup
import csv
import os
import time

base_url = 'https://www.tori.fi/uusimaa/tietokoneet_ja_lisalaitteet/komponentit?ca=18&cg=5030&c=5038&ps=1&st=s&st=k&st=u&st=h&st=g&com=graphic_card&w=1&o='
filename = 'gpu_all_info.csv'
processed_links_file = 'processed_links.txt'

def get_item_details(link):
    print(f"Fetching details from {link}")
    response = requests.get(link)
    
    # If the HTTP request is successful, the server will respond with HTTP status code 200
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the title of the item
        title_div = soup.find('div', class_='topic')
        title = title_div.find('h1').text.strip() if title_div else 'Title not found'
        
        # Find the price of the item
        price = soup.find(itemprop='price')
        price = price['content'] if price and price.has_attr('content') else 'Price not found'
        
        # Find the description of the item
        description_div = soup.find('div', class_='body', itemprop='description')
        description = description_div.text.strip() if description_div else 'Description not found'
        
        # Attempt to find the tech_data table which might contain date and condition of the item
        tech_data_table = soup.find('table', class_='tech_data')
        
        if tech_data_table:  # If the tech_data table is found
            rows = tech_data_table.find_all('tr')
            
            # Attempt to extract date from the second row, second column of the table if it exists
            date = 'Date not found'
            if len(rows) > 1:
                date_td = rows[1].find_all('td', class_='value')
                if date_td and len(date_td) > 1:
                    date = date_td[1].text.strip()
            
            # Attempt to extract condition from the third row, first column of the table if it exists
            condition = 'Condition not found'
            if len(rows) > 2:
                condition_td = rows[2].find('td', class_='value')
                if condition_td:
                    condition = condition_td.text.strip()
        else:  # If the tech_data table is not found, set date and condition as not found
            date = 'Date not found'
            condition = 'Condition not found'
        
        # Record the date and time when the details were fetched
        fetched_timestamp = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
        
        # Return a dictionary containing all the extracted details
        return {
            'Title': title,
            'Price': price,
            'Description': description,
            'Link': link,
            'Date': date,
            'Condition': condition,
            'Fetched Timestamp': fetched_timestamp
        }
        
    else:  # If the HTTP request is unsuccessful, return a dictionary with 'Failed to retrieve' for every detail
        print(f"Failed to retrieve details from {link}: {response.status_code}")
        return {
            'Title': 'Failed to retrieve',
            'Price': 'Failed to retrieve',
            'Description': 'Failed to retrieve',
            'Link': link,
            'Date': 'Failed to retrieve',
            'Condition': 'Failed to retrieve',
            'Fetched Timestamp': datetime.now().strftime('%H:%M:%S %Y-%m-%d')
        }


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

with open(filename, 'a', newline='', encoding='utf-8') as file:
    fieldnames = ['Title', 'Price', 'Description', 'Link', 'Date', 'Condition', 'Fetched Timestamp']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    if not file_exists:
        writer.writeheader()

# Iterate over the desired range of pages
for page_number in range(2, 5):
    url = base_url + str(page_number)
    print(f"Scraping page {page_number}")
    
    items_details_list = scrape_page(url, processed_links)
    
    if not items_details_list:
        print(f"No links found on page {page_number}. Exiting.")
        break
    
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        for item_details in items_details_list:
            writer.writerow(item_details)
            processed_links.add(item_details.get('Link'))
        
    # Save processed links
    with open(processed_links_file, 'w', encoding='utf-8') as f:
        for link in processed_links:
            f.write(f"{link}\n")

print("Scraping Completed.")