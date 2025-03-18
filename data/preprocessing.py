import pandas as pd
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import os

csv_path = os.path.abspath("/Users/amalayrania/Desktop/Skincare/data/cosmetics.csv")
db_path = os.path.abspath("/Users/amalayrania/Desktop/Skincare/data/cosmetic.db")

df = pd.read_csv(csv_path)

tfidf = TfidfVectorizer(stop_words="english", max_features=100)
ingredient_vectors = tfidf.fit_transform(df["Ingredients"].fillna(""))
ingredient_df = pd.DataFrame(ingredient_vectors.toarray(), columns=tfidf.get_feature_names_out())

label_encoders = {}
for col in ["Brand", "Name"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

df = df.drop(columns=["Ingredients"])
df = pd.concat([df, ingredient_df], axis=1)

numeric_df = df.select_dtypes(include=["number"])
low_variance_cols = numeric_df.columns[numeric_df.var() < 0.01]
df = df.drop(columns=low_variance_cols)

conn = sqlite3.connect(db_path)
df.to_sql("preprocessed_cosmetic", conn, if_exists="replace", index=False)
conn.close()

print("Data preprocessing completed successfully!")






