import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load custom theme
st.set_page_config(layout="wide")

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
    st.write(df_top10_handsets)

    # Prepare the DataFrame for plotting
    df_top10_handsets['Handset'] = df_top10_handsets['Handset Manufacturer'] + ' ' + df_top10_handsets['Handset Type']

    # Set the size of the figure
    plt.figure(figsize=(12, 8))
    sns.set(style="whitegrid")

    # Create a horizontal bar plot
    plt.barh(df_top10_handsets['Handset'], df_top10_handsets['Count'], color='skyblue')

    # Set the title and axis labels for the plot
    plt.title('Top 10 Handsets Used by Customers', fontsize=18, fontweight='bold')
    plt.xlabel('Count', fontsize=14)
    plt.ylabel('Handset Manufacturer and Type', fontsize=14)

    # Rotate the y-axis labels if needed
    plt.yticks(rotation=0, fontsize=12)

    # Display the plot
    st.pyplot(plt.gcf())

def main():
    # Use Markdown for the title with custom font size
    st.markdown("<h1 style='text-align: center; color: black;'>Telecom Data Dashboard</h1>", unsafe_allow_html=True)
    fetch_data_and_plot()

if __name__ == "__main__":
    main()