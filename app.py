import streamlit as st
import pandas as pd
import snowflake.connector
import matplotlib.pyplot as plt

st.set_page_config(page_title="Snowflake Dashboard", layout="wide")

# Initialize connection using Streamlit secrets
@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"],
        role=st.secrets["snowflake"]["role"]
    )

# Query runner
@st.cache_data
def run_query(query):
    conn = init_connection()
    cur = conn.cursor()
    cur.execute(query)
    df = cur.fetch_pandas_all()
    cur.close()
    return df

st.title("📊 Snowflake Live Dashboard")

# Example query (change as needed)
query = "SELECT C_MKTSEGMENT, COUNT(*) AS customer_count FROM CUSTOMER GROUP BY C_MKTSEGMENT"
df = run_query(query)

st.subheader("Customer Count by Market Segment")
st.dataframe(df)

fig, ax = plt.subplots()
ax.bar(df["C_MKTSEGMENT"], df["CUSTOMER_COUNT"])
plt.xticks(rotation=45)
st.pyplot(fig)
