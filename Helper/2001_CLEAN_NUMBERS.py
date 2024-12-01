import pandas as pd
import re

# Read the Excel file
df = pd.read_excel('2001.XLS')

# Function to clean and convert numeric strings
def clean_number(x):
    if pd.isna(x):
        return 0
    # If it's already a number, just convert to int
    if isinstance(x, (int, float)):
        return int(x)
    # Otherwise clean string and convert
    cleaned = re.sub(r'\s+', '', str(x))
    try:
        return int(cleaned)
    except ValueError:
        print(f"Warning: Could not convert '{x}' to number")
        return 0

numeric_columns = [col for col in df.columns if col not in ['Nr\npoz.', '%\nw okr.','Kandydat','Mandat']]

# Clean and convert numeric columns
for col in numeric_columns:
    df[col] = df[col].apply(clean_number)

# Group by 'Nr\nokręgu' and sum all numeric columns
#grouped = df.groupby('Nr\nokręgu').sum()

# Save results to CSV
df.to_csv('temp_2001.csv')

print("Results saved to temp_2001.csv")
