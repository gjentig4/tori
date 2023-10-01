import pandas as pd
import re

# Define a list of keywords that you will search for in the title and description.
gpu_keywords = [ '960','970','980','1050','1060', '1070', '1080', '2060', '2070', '2080', '3060', '3070', '3080', '3090', '4090',
                 '470','480', '390', '580 ','570 ', '590', '6700', '6800', '6900', '5500' ,'5700', '5600', 'Vega',
                '4070', '3090', '7900', '4080', '6950', '7800',
                '6750', '4060', '6600', '6650', '7600',
                '6500', '3050', '6400', '1660', '1650']

# Load the CSV file into a pandas DataFrame
filename = '123.csv'
data = pd.read_csv(filename)

# Initialize new columns for the GPU category and VRAM
data['GPU_Category'] = 'Unknown'
data['VRAM'] = 'Unknown'

# Define a function to categorize GPUs and find VRAM based on keywords in title and description
def categorize_gpu_and_find_vram(row):
    # Combine title and description and convert to lower case
    combined_text = (str(row['Title']) + ' ' + str(row['Description'])).lower()
    
    # Categorize GPU
    for keyword in gpu_keywords:
        if keyword.lower() in combined_text:
            row['GPU_Category'] = keyword
            break  # Stop the loop once a keyword is found
    
    # Find VRAM with case insensitive search
    vram_match = re.search(r'(?i)(\d+\s?GB)', combined_text)
    if vram_match:
        row['VRAM'] = vram_match.group(1).strip()
        
    return row

# Apply the function to each row in the DataFrame
data = data.apply(categorize_gpu_and_find_vram, axis=1)

# Reorder the columns list to place 'GPU_Category' as the 3rd column and 'VRAM' as the 4th column
columns_list = data.columns.tolist()
new_columns_list = columns_list[:2] + ['GPU_Category', 'VRAM'] + columns_list[2:-2]
data = data[new_columns_list]

# Save the categorized data and VRAM to a new CSV file with the new column order
data.to_csv('gpu_cleaned_data.csv', index=False)
