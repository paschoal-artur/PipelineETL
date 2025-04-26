import pandas as pd 
from datetime import datetime 
import sqlite3 

# Load the data from the json file
df = pd.read_json('data/data.jsonl', lines=True)

pd.options.display.max_columns = None 

#Create new column for the source, with a fixed value 
df['_source']  = "https://lista.mercadolivre.com.br/notebook"

#Create new column for the datetime
df['datetime'] = datetime.now()

#Making sure that None is 0
df['old_money'] = df['old_money'].fillna('0')
df['new_money'] = df['new_money'].fillna('0')
df['reviews_amount'] = df['reviews_amount'].fillna('0')
df['reviews_rating_number'] = df['reviews_rating_number'].fillna('0')

#Clean the data
df['old_money'] = df['old_money'].astype(str).str.replace('.', '', regex = False)
df['new_money'] = df['new_money'].astype(str).str.replace('.', '', regex = False)
df['reviews_amount'] = df['reviews_amount'].astype(str).str.replace('[\(\)]', '', regex = True)

#Convert the Data 
df['old_money'] = df['old_money'].astype(float).fillna('0')
df['new_money'] = df['new_money'].astype(float).fillna('0')
df['reviews_amount'] = df['reviews_amount'].astype(int).fillna('0')
df['reviews_rating_number'] = df['reviews_rating_number'].astype(float).fillna('0')

#Keep out the outliers, no notebooks are worth less than 1000 reais
df = df [
    (df['old_money'] >= 1000) &
    (df['new_money'] >= 1000) 
]

#print(df)

#Conect to the database

conn = sqlite3.connect('data/mercadolivre.sql')

#Save the dataframe in sqlite database
df.to_sql('mercadolivre', conn, if_exists='replace', index = False)

conn.close()