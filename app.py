import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

def connect_to_database():
    database_name = 'telecom'
    connection_params = {
        "host": "localhost",
        "user": "postgres",
        "password": "12345rdx",
        "port": "5432",
        "database": database_name
    }
    engine = create_engine(f"postgresql+psycopg2://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}:{connection_params['port']}/{connection_params['database']}")
    return engine

def fetch_data_and_plot():
    engine = connect_to_database()
    # Fetch data from the database
    df = pd.read_sql_query("SELECT * FROM public.xdr_data LIMIT 3000", engine)
    
    # SQL query to find the top 10 handsets used by customers
    sql_query = """
    SELECT "Handset Manufacturer", "Handset Type", COUNT(*) AS "Count"
    FROM "public"."xdr_data"
    WHERE "Handset Manufacturer" IS NOT NULL
    GROUP BY "Handset Manufacturer", "Handset Type"
    ORDER BY "Count" DESC
    LIMIT 10;
    """
    df_top10_handsets = pd.read_sql(sql_query, con=engine)

    # Prepare the DataFrame for plotting
    df_top10_handsets['Handset'] = df_top10_handsets['Handset Manufacturer'] + ' ' + df_top10_handsets['Handset Type']

    # Display the table in the first row
    st.write(df_top10_handsets)

    # Create a layout with 2 columns for the second row
    col1, col2 = st.columns(2)

    # Create a horizontal bar plot in the first column of the second row
    with col1:
        plt.figure(figsize=(10, 6))
        plt.barh(df_top10_handsets['Handset'], df_top10_handsets['Count'], color='skyblue')
        plt.title('Top 10 Handsets Used by Customers')
        plt.xlabel('Count')
        plt.ylabel('Handset Manufacturer and Type')
        plt.yticks(rotation=0)
        st.pyplot(plt.gcf())

    # Create a pie chart in the second column of the second row
    with col2:
        plt.figure(figsize=(10, 6))
        plt.pie(df_top10_handsets['Count'], labels=df_top10_handsets['Handset'], autopct='%1.1f%%', startangle=140)
        plt.title('Top 10 Handsets Used by Customers (Pie Chart)')
        st.pyplot(plt.gcf())

def main():
    st.title('Telecom Data Dashboard')
    fetch_data_and_plot()

if __name__ == "__main__":
    main()