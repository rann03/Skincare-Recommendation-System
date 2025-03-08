import pandas as pd
import sqlite3


df = pd.read_csv('cosmetics.csv')
conn = sqlite3.connect('cosmetic.db')
df.to_sql('cosmetic', conn, if_exists='replace', index=False)
conn.close()