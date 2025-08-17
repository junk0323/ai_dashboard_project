import streamlit as st
import pandas as pd
import snowflake.connector
import altair as alt

# -------------------------------
# Snowflake connection function
# -------------------------------
@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database="SNOWFLAKE_SAMPLE_DATA",
        schema="TPCH_SF1"
    )

# -------------------------------
# Query runner
# -------------------------------
@st.cache_data
def run_query(query):
    conn = init_connection()
    cur = conn.cursor()
    cur.execute(query)
    df = cur.fetch_pandas_all()
    cur.close()
    conn.close()
    return df

# -------------------------------
# Streamlit Dashboard
# -------------------------------
st.set_page_config(page_title="Snowflake TPCH Dashboard", layout="wide")
st.title("📊 Snowflake TPCH_SF1 Sample Dashboard")

# Example Query using ORDERS + LINEITEM
query = """
    SELECT 
        o_orderdate AS ORDER_DATE,
        o_orderkey AS ORDER_ID,
        o_custkey AS CUSTOMER_ID,
        SUM(l_extendedprice * (1 - l_discount)) AS SALES_AMOUNT
    FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS o
    JOIN SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.LINEITEM l
        ON o.o_orderkey = l.l_orderkey
    GROUP BY o_orderdate, o_orderkey, o_custkey
    LIMIT 1000
"""
df = run_query(query)

st.subheader("📈 Sales Data (Sample from TPCH_SF1)")
st.dataframe(df.head(20))

# -------------------------------
# Charts
# -------------------------------

# Sales over time
sales_time = (
    alt.Chart(df)
    .mark_line()
    .encode(
        x="ORDER_DATE:T",
        y="sum(SALES_AMOUNT):Q"
    )
    .properties(title="Sales Over Time")
)

# Top Customers
top_customers = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x="CUSTOMER_ID:O",
        y="sum(SALES_AMOUNT):Q"
    )
    .transform_aggregate(
        total_sales="sum(SALES_AMOUNT)",
        groupby=["CUSTOMER_ID"]
    )
    .transform_window(
        rank="rank()",
        sort=[{"field": "total_sales", "order": "descending"}]
    )
    .transform_filter("datum.rank <= 10")
    .properties(title="Top 10 Customers by Sales")
)

# Layout
col1, col2 = st.columns(2)
col1.altair_chart(sales_time, use_container_width=True)
col2.altair_chart(top_customers, use_container_width=True)

st.success("✅ Dashboard connected to Snowflake TPCH sample data")
