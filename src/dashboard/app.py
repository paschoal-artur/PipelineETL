import pandas as pd 
import streamlit as st
import sqlite3 

conn = sqlite3.connect('data/mercadolivre.db')

df = pd.read_sql_query("SELECT * FROM notebooks", conn)

conn.close()

#Application title
st.title("📊 Market Search - Mercado Livre's Notebooks")

#Better layout with kpi columns

st.subheader('Kpi principals')
col1, col2, col3 = st.columns(3)

#Kpi 1: Total items
total_items = df.shape[0]
col1.metric(label = "🖥️ Total Notebooks", value = total_items)

#Kpi 2: Number of unique brands
unique_brands = df['brand'].nunique()
col2.metric(label = "🏷️ Unique Brands", value = unique_brands)

#Kpi 3: New average price (reais)
average_new_price = df['new_money'].mean()
col3.metric(label="💰 Average Price (R$)", value = f"{average_new_price:.2f}")

#Most frequent brands
st.subheader('🏆 Most found brands till 10th page')
col1, col2 = st.columns([4, 2])
top_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_brands)
col2.write(top_brands)

#Average price by brand
st.subheader('💵 Average Price by Brand')
col1, col2 = st.columns([4, 2])
df_non_zero_prices = df[df['new_money'] > 0]
average_price_by_brand = df_non_zero_prices.groupby('brand')['new_money'].mean().sort_values(ascending = False)
col1.bar_chart(average_price_by_brand)
col2.write(average_price_by_brand)

#Satisfaction by brand
st.subheader('⭐ Average Satisfaction by Brand')
col1, col2 = st.columns([4, 2])
df_non_zero_reviews = df[df['reviews_rating_number'] > 0]
satisfaction_by_brand = df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)