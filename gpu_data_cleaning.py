import pandas as pd
import re

# Load the Data
filename = 'tori_fi_GPUs_10pg.csv'
data = pd.read_csv(filename)

# Data Cleaning
data['Title'] = data['Title'].str.lower()  # Convert titles to lowercase
data['Title'] = data['Title'].str.replace('[^a-z0-9\s]', '')  # Remove special characters from titles
data['Price'] = data['Price'].replace('[\€, ]', '', regex=True).astype(float)  # Convert price to numerical

# List of GPU models
nvidia_models = ['960', '970', '980', '1050', '1060', '1070', '1080', '2060', '2070', '2080', '2090', '3060', '3070', '3080', '3090', '4060', '4070', '4080', '4090']
amd_models = ['rx570', 'rx580', 'rx590', 'rx5500xt', 'rx5600xt', 'rx5700', 'rx5700xt', 'rx6600', 'rx6600xt', 'rx6700xt', 'rx6800', 'rx6800xt', 'rx6900xt']
all_models = nvidia_models + amd_models

# Define function to find model
def find_model(title):
    for model in all_models:
        model_with_space = model.replace('rx', 'rx ')
        if model in title or model_with_space in title:
            return model
    return 'Other'

# Define function to find model with VRAM
def find_model_with_vram(title):
    for model in all_models:
        pattern = re.compile(rf'({model}\s*\d+gb)')
        match = pattern.search(title)
        if match:
            return match.group(1).replace(' ', '')
        
        model_with_space = model.replace('rx', 'rx ')
        if model in title or model_with_space in title:
            return model
    return 'Other'

# Data Categorization - Models Only
data['Model'] = data['Title'].apply(find_model)
aggregated_by_model = data.groupby('Model').agg({'Price': ['mean', 'count']}).reset_index()
aggregated_by_model.columns = ['Model', 'Average Price', 'Count']

# Data Categorization - Models + VRAM
data['Model_VRAM'] = data['Title'].apply(find_model_with_vram)
aggregated_by_model_vram = data.groupby('Model_VRAM').agg({'Price': ['mean', 'count']}).reset_index()
aggregated_by_model_vram.columns = ['Model_VRAM', 'Average Price', 'Count']

# Print Results
print("Aggregated by Model")
print(aggregated_by_model)
print("\nAggregated by Model + VRAM")
print(aggregated_by_model_vram)

# Optionally, save the aggregated DataFrames to CSV
aggregated_by_model.to_csv('aggregated_by_model.csv', index=False)
aggregated_by_model_vram.to_csv('aggregated_by_model_vram.csv', index=False)
