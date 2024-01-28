# GPU Marketplace Scraper

## Overview

This project, named "GPU Marketplace Scraper", is a Python-based web scraping tool designed to extract and organize information about graphics processing units (GPUs) from the "Tori.fi" marketplace, specifically within the Uusimaa region's computer components category. It focuses on gathering detailed information on each GPU listing, including titles, prices, descriptions, dates, and conditions. The collected data is systematically recorded in a CSV file for easy analysis and reference.

## Features

- **Web Scraping**: Utilizes the `requests` and `BeautifulSoup` libraries to scrape GPU listings from the specified URL.
- **Data Extraction**: Extracts key details of each GPU listing, such as title, price, description, link, date of posting, and condition.
- **Data Recording**: Saves the extracted data into a CSV file (`gpu_all_info.csv`) with appropriate headers for each column.
- **Link Tracking**: Maintains a record of processed links in `processed_links.txt` to avoid duplication of data.
- **Robust Error Handling**: The script checks for HTTP request success and handles cases where data might not be found or the request fails.
- **Timestamp Recording**: Each entry includes a timestamp indicating when the data was fetched, ensuring traceability and relevance of the data.

## How it Works

1. **Initialization**: The script initializes by setting the base URL for the "Tori.fi" GPU listings and preparing the CSV file for data storage.
2. **Data Scraping and Extraction**: For each page in the specified range, the script:
   - Fetches the page content.
   - Extracts individual GPU listing links.
   - Visits each GPU listing to gather detailed information.
   - Records the extracted data in the CSV file.
3. **Tracking Processed Links**: To avoid reprocessing, each processed link is recorded. If the script is rerun, it skips the already processed links.
4. **Continuous Operation**: The script processes a predefined range of pages, extracting and saving data continuously until completed.

## Usage

1. **Dependencies Installation**: Before running the script, ensure that `requests`, `bs4` (Beautiful Soup), and `csv` Python packages are installed.
2. **Execution**: Run the script in a Python environment. The script will automatically start scraping data from the specified URL range.
3. **Output**: The output will be a CSV file named `gpu_all_info.csv` containing all the scraped data along with a file `processed_links.txt` for tracking purposes.

## Note

This script is developed for educational purposes and to demonstrate web scraping capabilities. Users are responsible for adhering to "Tori.fi" terms of service and should be aware of the legal and ethical implications of web scraping. 

---

Feel free to explore the code and contact me for any questions or suggestions regarding this project!
"""
