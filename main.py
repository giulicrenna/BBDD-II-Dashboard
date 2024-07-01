import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Bases de Datos II - Dashboard", page_icon=":bar_chart:", layout="wide")

fact = pd.read_csv('data/fact_sep.csv', encoding='latin-1', delimiter=';', index_col=False)
customer = pd.read_csv('data/customer.csv', encoding='latin-1', index_col=False)
group = pd.read_csv('data/group.csv', encoding='latin-1', index_col=False)
employee = pd.read_csv('data/employee.csv', encoding='latin-1', delimiter=';', index_col=False)
time = pd.read_csv('data/time.csv', encoding='latin-1', index_col=False)
products = pd.read_csv('data/products.csv', encoding='latin-1', index_col=False)

def convert_to_int(x) -> int:
    try:
        return int(x)
    except:
        return 0
    
fact['CUSTOMER_KEY'] = fact['CUSTOMER_KEY'].apply(convert_to_int)
fact['TIME_KEY'] = fact['TIME_KEY'].apply(convert_to_int)
fact['TIME_KEY'] = pd.to_datetime(fact['TIME_KEY'], format='%Y%m%d', errors='coerce')
fact['TOTAL_LITERS'] = pd.to_numeric(fact['TOTAL_LITERS'].apply(lambda x: x.replace(',', '.')))
fact['QUANTITY'] = fact['QUANTITY'].apply(convert_to_int)

customer_names = customer[['CUSTOMER_KEY', 'FULL_NAME']].drop_duplicates()
fact = fact.merge(customer_names, on='CUSTOMER_KEY', how='left')

employees_birthdate = employee[['EMPLOYEE_KEY', 'BIRTH_DATE']].drop_duplicates()
fact = fact.merge(employees_birthdate, on='EMPLOYEE_KEY', how='left')
fact['BIRTH_DATE'] = pd.to_datetime(fact['BIRTH_DATE'], format='%Y/%m/%d', errors='coerce')

customer['BIRTH_DATE'] = pd.to_datetime(customer['BIRTH_DATE'], format='%d/%m/%Y', errors='coerce')

# Question 1: Liters Consumed and Products Acquired by Customer Over Time
st.header("1. Litros Consumidos y Productos adquiridos por Cliente")
liters_consumed = fact.groupby(['FULL_NAME', 'TIME_KEY'])[['TOTAL_LITERS', 'QUANTITY']].sum().reset_index()
fig1 = px.line(liters_consumed,
               x='TIME_KEY',
               y='TOTAL_LITERS',
               color='FULL_NAME',
               title='Litros Consumidos y Productos adquiridos por Cliente"').update_traces(visible="legendonly", selector=lambda t: not t.name in ["Abel", "Nelsen"])
st.plotly_chart(fig1)

fig2 = px.line(liters_consumed,
               x='TIME_KEY',
               y='QUANTITY',
               color='FULL_NAME',
               title='Productos adquiridos por Cliente').update_traces(visible="legendonly", selector=lambda t: not t.name in ["Abel", "Adina"])
st.plotly_chart(fig2)

# Question 2: Average Purchase in Liters by Customer Over Time
st.header("2. Promedio de Compra en Litros por Cliente")
average_purchase = liters_consumed.groupby(['TIME_KEY', 'FULL_NAME'])[['TOTAL_LITERS']].mean().reset_index()
fig3 = px.line(average_purchase,
               x='TIME_KEY',
               y='TOTAL_LITERS',
               color='FULL_NAME',
               title='Promedio de Compra en Litros por Cliente').update_traces(visible="legendonly", selector=lambda t: not t.name in ["Adams", "Antrim"])
st.plotly_chart(fig3)
