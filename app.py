import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Customer Marketing Campaign Dashboard")

@st.cache_data
def load_and_clean_data():
    df = pd.read_csv('marketing_campaign.csv')
    
    # 1. Fill missing values
    df['Income'] = df['Income'].fillna(df['Income'].median())
    
    # 2. Filter outliers
    df = df[df['Income'] < 200000]
    df = df[df['Year_Birth'] > 1920]
    
    # 3. Feature Engineering
    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], format='%d/%m/%Y')
    df['Customer_Tenure_Days'] = (df['Dt_Customer'].max() - df['Dt_Customer']).dt.days
    df = df.drop(columns=['Z_CostContact', 'Z_Revenue'], errors='ignore')
    
    spend_cols = ['MntWines','MntFruits','MntMeatProducts','MntFishProducts','MntSweetProducts','MntGoldProds']
    df['Total_Spend'] = df[spend_cols].sum(axis=1)
    df['Age'] = 2026 - df['Year_Birth']
    df['Total_Children'] = df['Kidhome'] + df['Teenhome']
    df['Total_Purchases'] = df['NumWebPurchases'] + df['NumCatalogPurchases'] + df['NumStorePurchases']
    
    # 4. Clean Marital Status
    df['Marital_Status'] = df['Marital_Status'].replace({
        'Alone': 'Single',
        'Absurd': 'Single',
        'YOLO': 'Single'
    })
    return df

df = load_and_clean_data()

st.subheader("Data Overview")
st.dataframe(df.head())

st.subheader("Spending by Family Size")
fig, ax = plt.subplots()
sns.barplot(data=df, x='Total_Children', y='Total_Spend', ax=ax)
st.pyplot(fig)