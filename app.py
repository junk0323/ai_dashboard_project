import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load mock data
df = pd.read_csv("data/mock_sales.csv")

st.title("📊 AI Alerts + Sales Dashboard")

st.write("## Sales Data")
st.dataframe(df.head())

st.write("## Sales by Region")
region_sales = df.groupby("Region")["Sales"].sum()
fig, ax = plt.subplots()
region_sales.plot(kind="bar", ax=ax)
st.pyplot(fig)

st.write("## AI Alert Simulation")
threshold = st.slider("Set Sales Alert Threshold", 1000, 10000, 5000)
alerts = df[df["Sales"] > threshold]
if not alerts.empty:
    st.warning(f"⚠️ {len(alerts)} transactions exceeded the threshold!")
    st.dataframe(alerts)
else:
    st.success("✅ No alerts triggered.")
