import pandas as pd

file_path = '/Users/amalayrania/Desktop/Skincare/data/cosmetics.csv'
df = pd.read_csv(file_path)

# Debugging: Print column names to confirm
print(df.columns)

# Strip spaces from column names
df.columns = df.columns.str.strip()


def generate_description(row):
    skin_types = []
    for skin_type in ['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']:
        if row.get(skin_type, 0) == 1:  
            skin_types.append(skin_type)
    
    skin_types_str = f" It is suitable for {' and '.join(skin_types)} skin types." if skin_types else ""
    
    return (f"This product is {row.get('Name', 'Unknown Product')} from the brand {row.get('Brand', 'Unknown Brand')}. "
            f"It is a {row.get('Label', 'Unknown Product Type')}. {skin_types_str} "
            f"It is priced at ${row.get('Price', 'Unknown Price')}.")

df['description'] = df.apply(generate_description, axis=1)

df.to_csv('prepared.csv', index=False)
print(df.head())
