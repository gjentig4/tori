import requests
from bs4 import BeautifulSoup
import csv
import os

url = 'https://www.tori.fi/uusimaa/tietokoneet_ja_lisalaitteet/komponentit?ca=18&cg=5030&c=5038&ps=1&w=1&st=s&st=k&st=u&st=h&st=g&com=graphic_card'

filename = 'tori_fi_GPUs.csv'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
   
    titles = soup.find_all('div', class_='li-title')
    prices = soup.find_all('p', class_='list_price')
    
    # Check if file exists, create or append accordingly
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # If file didn't exist, write header
        if not file_exists:
            writer.writerow(['Title', 'Price'])
        
        for title, price in zip(titles, prices):
            writer.writerow([title.text.strip(), price.text.strip()])

else:
    print(f"Failed to retrieve the page: {response.status_code}")
