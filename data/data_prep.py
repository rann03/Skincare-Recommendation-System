import pandas as pd

file_path = '/Users/amalayrania/Desktop/Skincare/data/cosmetics.csv'
df = pd.read_csv(file_path)
df['description'] = df.apply(lambda row: f"Name: {row['Name']}. Brand: {row['Brand']}. Ingredients: {row['Ingredients']}. Price: ${row['Price']}.", axis=1)
df.to_csv('cosmetics_prepared.csv', index=False)
print(df.head())