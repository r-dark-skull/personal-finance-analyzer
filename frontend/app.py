import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    return pd.read_csv("expenses.csv")

def save_data(df):
    df.to_csv("expenses.csv", index=False)

st.sidebar.header("Options")
time_period = st.sidebar.selectbox(
    'Select time period:',
    ('Current Month', 'Current Week', 'Current Year', 'Custom')
)

@st.cache_data
def cached_load_data():
    return load_data()

expenses = cached_load_data()

if time_period == 'Current Month':
    filtered_expenses = expenses[pd.to_datetime(expenses['Timestamp']).dt.month == pd.Timestamp.now().month]
elif time_period == 'Current Week':
    filtered_expenses = expenses[(pd.to_datetime(expenses['Timestamp']) >= pd.Timestamp.now() - pd.DateOffset(weeks=1)) & (pd.to_datetime(expenses['Timestamp']) <= pd.Timestamp.now())]
elif time_period == 'Current Year':
    filtered_expenses = expenses[pd.to_datetime(expenses['Timestamp']).dt.year == pd.Timestamp.now().year]
else:
    start_date = st.sidebar.date_input('Start Date', pd.Timestamp.now().replace(day=1, month=1), min_value=pd.Timestamp('2020-01-01'), max_value=pd.Timestamp.now())
    end_date = st.sidebar.date_input('End Date', pd.Timestamp.now(), min_value=pd.Timestamp('2020-01-01'), max_value=pd.Timestamp.now())
    filtered_expenses = expenses[(pd.to_datetime(expenses['Timestamp']) >= start_date) & (pd.to_datetime(expenses['Timestamp']) <= end_date)]

st.title("Expense Tracker")
st.subheader(f"Showing Expenses for {time_period}")
st.write(filtered_expenses)

category_expenses = filtered_expenses.groupby('Category')['Amount'].sum()
fig, ax = plt.subplots()
ax.pie(category_expenses, labels=category_expenses.index, autopct='%1.1f%%')
st.subheader("Expense Distribution by Category")
st.pyplot(fig)

filtered_expenses['Timestamp'] = pd.to_datetime(filtered_expenses['Timestamp'])  # Convert Timestamp column to datetime format
time_expenses = filtered_expenses.groupby(pd.Grouper(key='Timestamp', freq='D')).sum()['Amount']
fig, ax = plt.subplots()
ax.bar(time_expenses.index, time_expenses.values)
plt.xticks(rotation=45)
st.subheader("Total Expenses Over Time")
st.pyplot(fig)

unknown_expenses = filtered_expenses[filtered_expenses['Category'] == 'Unknown']
if not unknown_expenses.empty:
    st.subheader("Unknown Expenses")
    unknown_expenses_table = unknown_expenses[['Timestamp', 'Amount']].copy()
    unknown_expenses_table.index = range(1, len(unknown_expenses_table) + 1)
    row_selected = st.radio("Select a row to update category:", unknown_expenses_table.index)
    selected_row = unknown_expenses_table.loc[row_selected]
    st.write(selected_row)

    selected_category = st.selectbox('Select category:', expenses['Category'].unique())
    if st.button("Assign"):
        if selected_category != 'Unknown':
            expenses.at[row_selected - 1, 'Category'] = selected_category
            save_data(expenses)
            st.success(f'Assigned category "{selected_category}" to Expense {row_selected}!')


st.sidebar.header("Add New Expense")
new_timestamp = st.sidebar.date_input("Date", value=pd.Timestamp.now(), min_value=pd.Timestamp('2020-01-01'), max_value=pd.Timestamp.now())
new_category = st.sidebar.selectbox("Category", expenses['Category'].unique())
new_amount = st.sidebar.number_input("Amount", min_value=0.01, step=0.01)
if st.sidebar.button("Add Expense"):
    new_expense = pd.DataFrame({'Timestamp': [new_timestamp], 'Category': [new_category], 'Amount': [new_amount]})
    expenses = pd.concat([expenses, new_expense], ignore_index=True)
    save_data(expenses)
    st.sidebar.success("Expense added successfully!")
