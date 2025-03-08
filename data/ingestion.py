import pandas as pd
import sqlite3
import os

csv_path = os.path.abspath("/Users/amalayrania/Desktop/Skincare/data/cosmetics.csv")
db_path = os.path.abspath("/Users/amalayrania/Desktop/Skincare/data/cosmetic.db")

df = pd.read_csv(csv_path)

conn = sqlite3.connect(db_path)
df.to_sql('cosmetic', conn, if_exists='replace', index=False)
conn.close()

print("Data successfully ingested into the database!")
