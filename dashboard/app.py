import streamlit as st
import json

st.title("Store Intelligence Dashboard")

with open("outputs/analytics.json", "r") as f:
    analytics = json.load(f)

st.metric("Store Entries", analytics["total_entries"])
st.metric("Unique Visitors", analytics["unique_visitors"])

st.subheader("Zone Distribution")

st.bar_chart(analytics["zone_distribution"])

st.subheader("Store Heatmap")

st.image(
    "outputs/heatmap.png"
)