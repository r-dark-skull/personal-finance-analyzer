import os
import pandas as pd
import streamlit as st
import json
import plotly.express as px
import matplotlib.pyplot as plt

# Fetch data as JSON
fetch_data = """[
    {
        "_id": "txn_001",
        "amount": 150.75,
        "tx_type": "DEBIT",
        "vendor": "Amazon",
        "vendor_id": "vendor_123"
    },
    {
        "_id": "txn_002",
        "amount": 99.99,
        "tx_type": "CREDIT",
        "vendor": "Walmart",
        "vendor_id": "vendor_456"
    },
    {
        "_id": "txn_003",
        "amount": 45.00,
        "tx_type": "DEBIT",
        "vendor": "Starbucks",
        "vendor_id": "null"
    },
    {
        "_id": "txn_004",
        "amount": 200.00,
        "tx_type": "DEBIT",
        "vendor": "Apple Store",
        "vendor_id": "vendor_789"
    },
    {
        "_id": "txn_005",
        "amount": 120.50,
        "tx_type": "CREDIT",
        "vendor": "Best Buy",
        "vendor_id": "vendor_321"
    }
]"""

# Load JSON data into DataFrame
data = json.loads(fetch_data)
df = pd.DataFrame(data)

# Streamlit sidebar for time period selection (removed since not used)
st.sidebar.header("Options")
time_period = st.sidebar.selectbox(
    'Select time period:',
    ('Current Month', 'Current Week', 'Current Year', 'Custom')
)

# Streamlit app title and header
st.title("Expense Tracker")
st.subheader(f"Showing Expenses for {time_period}")

# Display the DataFrame
st.write(df)

# Group by transaction type and sum the amounts
grouped_by_tx_type = df.groupby('tx_type')['amount'].sum().reset_index()

# Create a pie chart for transaction type and amount
fig1 = px.pie(grouped_by_tx_type, names='tx_type', values='amount', title='Transaction Type Distribution by Amount')

# Display the pie chart in Streamlit
st.subheader("Transaction Type Distribution by Amount")
st.plotly_chart(fig1)

# Group by vendor and sum the amounts
grouped_by_vendor = df.groupby('vendor')['amount'].sum().reset_index()

# Create a pie chart for vendor and amount
fig2 = px.pie(grouped_by_vendor, names='vendor', values='amount', title='Vendor Distribution by Amount')

# Display the pie chart in Streamlit
st.subheader("Vendor Distribution by Amount")
st.plotly_chart(fig2)