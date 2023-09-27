import requests
from bs4 import BeautifulSoup
import csv
import os

base_url = 'https://www.tori.fi/uusimaa/tietokoneet_ja_lisalaitteet/komponentit?ca=18&cg=5030&c=5038&ps=1&st=s&st=k&st=u&st=h&st=g&com=graphic_card&w=1&o='
filename = 'tori_fi_GPUs_10pg.csv'

# Function to scrape a single page
def scrape_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all('div', class_='li-title')  
        prices = soup.find_all('p', class_='list_price') 
        return list(zip(titles, prices))
    else:
        print(f"Failed to retrieve page {url}: {response.status_code}")
        return []

# Main loop to iterate over the pages
file_exists = os.path.isfile(filename)

with open(filename, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write header if file didn't exist
    if not file_exists:
        writer.writerow(['Title', 'Price'])
        
    # Iterate over the desired range of pages
    for page_number in range(2, 11):  # 6 is exclusive, so it will iterate over 2, 3, 4, 5
        url = base_url + str(page_number)
        print(f"Scraping page {page_number}")
        
        # Call the function to scrape the page
        for title, price in scrape_page(url):
            writer.writerow([title.text.strip(), price.text.strip()])
