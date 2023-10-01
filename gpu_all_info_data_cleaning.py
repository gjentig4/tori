import pandas as pd
import re

# Load the CSV file into a pandas DataFrame
filename = 'gpu_all_info.csv'
data = pd.read_csv(filename)

# Define GPU keywords
gpu_keywords = ['960', '970', '980', '1050', '1060', '1070', '1080', '2060', '2070', '2080', '3060', '3070', '3080', '3090', '4090',
                '470', '480', '390', '580', '570', '590', '6700', '6800', '6900', '5500', '5700', '5600', 'Vega',
                '4070', '3090', '7900', '4080', '6950', '7800', '6750', '4060', '6600', '6650', '7600', '6500', '3050', '6400', '1660', '1650']

# Initialize new columns for the GPU category, VRAM, and GPU Variant
data['GPU_Category'] = 'Unknown'
data['VRAM'] = 'Unknown'
data['GPU_Variant'] = 'None'  # New column to store GPU variant information


# Define a function to categorize GPUs, find VRAM, and GPU Variant based on keywords in title and description
def categorize_gpu_and_find_vram(row):
    combined_text = (str(row['Title']) + ' ' + str(row['Description'])).lower()
    
    # Find GPU Category and Variant together
    for keyword in gpu_keywords:
        pattern = rf'(?i)({keyword}\s*(xt|ti|super|oc)?)'
        match = re.search(pattern, combined_text)
        if match:
            row['GPU_Category'] = keyword  # Extracting GPU Category
            variant = match.group(2)  # Extracting GPU Variant if exists
            if variant:
                row['GPU_Variant'] = variant.strip().upper()
            break
    
    # Find VRAM
    vram_match = re.search(r'(?i)(\d+\s?GB)', combined_text)
    if vram_match:
        row['VRAM'] = vram_match.group(1).strip()

    return row


# Apply the function to each row in the DataFrame
data = data.apply(categorize_gpu_and_find_vram, axis=1)

# Reorder the columns list to place 'GPU_Category' as the 3rd column, 'VRAM' as the 4th column, and 'GPU_Variant' as the 5th column
columns_list = data.columns.tolist()
new_columns_list = columns_list[:2] + ['GPU_Category', 'VRAM', 'GPU_Variant'] + columns_list[2:-3]
data = data[new_columns_list]

# Save the resulting DataFrame to a new CSV file
output_filename = 'gpu_cleaned_data.csv'
data.to_csv(output_filename, index=False)

output_filename
