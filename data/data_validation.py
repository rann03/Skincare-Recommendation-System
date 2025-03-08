import pandas as pd
import os
import sqlite3

db_path = os.path.abspath("/Users/amalayrania/Desktop/Skincare/data/cosmetic.db")

conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM preprocessed_cosmetic", conn)
conn.close()

schema = {
    "Brand": "object",
    "Name": "object",
    "Price": "int64",
    "Rank": "int64"
}

print("Data Statistics:")
print(df.describe(include='all'))

print("\nMissing Values:")
print(df.isnull().sum())

print("\nData Types:")
print(df.dtypes)

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nOutliers in Price:")
print(df["Price"].describe())
print("\nOutliers in Rank:")
print(df["Rank"].describe())

df = df.dropna()  

df = df.astype(schema)

df = df.drop_duplicates()

price_threshold = df["Price"].mean() + 3 * df["Price"].std()
rank_threshold = df["Rank"].mean() + 3 * df["Rank"].std()
df = df[(df["Price"] <= price_threshold) & (df["Rank"] <= rank_threshold)]

conn = sqlite3.connect("cosmetic_cleaned.db")
df.to_sql("preprocessed_cosmetic", conn, if_exists="replace", index=False)
conn.close()

print("\nData validation and cleaning completed.")