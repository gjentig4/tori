import requests
from bs4 import BeautifulSoup

url = 'https://www.tori.fi/uusimaa/Msi_aero_1060_3g_117292860.htm?ca=18&w=3'

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    tech_data_table = soup.find('table', class_='tech_data')
    
    if tech_data_table:
        rows = tech_data_table.find_all('tr')
        
        # Extracting Date
        if len(rows) > 1:
            date_td = rows[1].find_all('td', class_='value')
            if date_td and len(date_td) > 1:
                date = date_td[1].text.strip()
            else:
                date = 'Date not found'
        else:
            date = 'Date not found'
        
        # Extracting Condition
        if len(rows) > 2:
            condition_td = rows[2].find('td', class_='value')
            condition = condition_td.text.strip() if condition_td else 'Condition not found'
        else:
            condition = 'Condition not found'
        
        print(f"Date: {date}, Condition: {condition}")
    else:
        print('tech_data table not found.')
else:
    print(f"Failed to retrieve page {url}: {response.status_code}")
