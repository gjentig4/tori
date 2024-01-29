# Tori.fi GPU Data Fetcher, Analyzer, and Cleaner

## Overview

This Python-based project consists of two main scripts:

1. **Data Fetcher and Analyzer (`gpu_all_info_10_page_auto_stop.py`)**: A web scraping tool for extracting GPU listings from "Tori.fi", specifically in the Uusimaa region's computer components category. It captures details like titles, prices, descriptions, and more, saving them to a CSV file.

2. **Data Cleaner (`gpu_all_info_data_cleaning.py`)**: Enhances the data set by categorizing GPUs, identifying VRAM, and extracting GPU variants from the scraped data. It uses the output from the first script and processes it further to add meaningful insights.

3. All other scripts are variations of these two and how I basically came up with these

### Preview

| Title                                 | Price  | GPU Category | VRAM   | GPU Variant | Description                                                                                                                                 | Link                                                                                                      | Date                | Condition   | Timestamp            |
|---------------------------------------|--------|--------------|--------|-------------|---------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|---------------------|-------------|----------------------|
| Rtx 3090 24gb, helsinki               | 1100.00| 3090         | 24gb   | None        | Lisätiedot Hankin tämän tekoälyllä tehtävään kuvanmuokkaukseen, mutta en enää tarvitse sitä. Ei ole louhittu, eikä juurikaan muuten käytetty. | [Link](https://www.tori.fi/uusimaa/Rtx_3090_24gb__helsinki_118762279.htm?ca=18&w=1)                       | 26 syyskuuta 08:43  | Erinomainen | 01:28:26 2023-10-02 |
| GeForce GTX 1050 Ti GAMING X 4G       | 50.00  | 1050         | Unknown| TI          | Lisätiedot Muutaman vuoden käytössä ollut normaali kuntoinen näytönohjain.                                                                  | [Link](https://www.tori.fi/uusimaa/GeForce_GTX_1050_Ti_GAMING_X_4G_118762119.htm?ca=18&w=1)                | 26 syyskuuta 08:38  | Erinomainen | 01:28:27 2023-10-02 |
| Amd Radeon RX 570 Series näytönohjain | 120.00 | 570          | 8 gb   | None        | Lisätiedot Kunto: Hyvä.Käyttöaika: 3 vuotta.Muisti: 8 GB.                                                                                   | [Link](https://www.tori.fi/uusimaa/Amd_Radeon_RX_570_Series_naytonohjain_118751908.htm?ca=18&w=1)           | 25 syyskuuta 19:59  | Hyvä        | 01:28:28 2023-10-02 |

   
## Features

### Data Fetcher and Analyzer

- **Web Scraping**: Uses `requests` and `BeautifulSoup` for scraping GPU listings.
- **Data Extraction**: Captures title, price, description, link, posting date, and condition.
- **Data Recording**: Saves data in `gpu_all_info.csv`.
- **Link Tracking**: Keeps a record of processed links in `processed_links.txt`.
- **Error Handling**: Manages HTTP request failures and missing data.
- **Timestamps**: Includes timestamps for data fetch time.

### Data Cleaner

- **Pandas for Data Manipulation**: Utilizes `pandas` for handling the CSV file.
- **GPU Categorization**: Classifies GPUs based on predefined keywords.
- **VRAM Identification**: Extracts VRAM details from the listings.
- **GPU Variant Extraction**: Identifies specific GPU variants like 'XT', 'TI', or 'Super'.
- **New Columns**: Adds 'GPU_Category', 'VRAM', and 'GPU_Variant' columns to the dataset.
- **Output File**: Generates a cleaned and enhanced CSV file named `gpu_cleaned_data.csv`.

## Usage

### Data Fetcher and Analyzer

1. **Install Dependencies**: Ensure `requests`, `bs4` (Beautiful Soup), and `csv` are installed.
2. **Run the Script**: Execute in a Python environment to start data scraping.
3. **Output**: Check `gpu_all_info.csv` and `processed_links.txt`.

### Data Cleaner

1. **Run the Script**: After the first script, run the data cleaner script.
2. **Output**: Generates `gpu_cleaned_data.csv` with added columns and cleaned data.

## Note

Both scripts are for educational purposes and demonstrate web scraping and data cleaning. Users must adhere to "Tori.fi" terms of service and consider legal and ethical implications of web scraping and data processing.

---

Feel free to explore the code and reach out for any questions or suggestions!
"""
