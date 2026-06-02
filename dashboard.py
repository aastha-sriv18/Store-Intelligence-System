import streamlit as st
import json
import pandas as pd
from PIL import Image
import os
import plotly.express as px

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="Store Intelligence Dashboard", 
    page_icon="🛍️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS for Professional Styling
st.markdown("""
    <style>
        /* Add padding to the top */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        /* Style the metric containers to look like cards */
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.05);
        }
        /* FIX: Force all text inside the metric cards to be dark */
        div[data-testid="stMetric"] * {
            color: #1E1E1E !important;
        }
        /* Customize headers */
        h1, h2, h3 {
            font-family: 'Helvetica Neue', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------
# Header Section
# --------------------
st.title("📊 Store Intelligence Dashboard")
st.markdown("Monitor real-time retail analytics, customer flow, and zone engagement.")
st.divider()

# --------------------
# Data Loading & KPIs
# --------------------
try:
    with open("outputs/analytics.json") as f:
        analytics = json.load(f)
        
    st.subheader("Key Performance Indicators")
    
    # Use columns for KPIs to save vertical space
    kpi1, kpi2, kpi3 = st.columns(3)
    
    with kpi1:
        st.metric("Total Entries", analytics.get("total_entries", 0))
    with kpi2:
        st.metric("Unique Visitors", analytics.get("unique_visitors", 0))
    with kpi3:
        st.metric("Active Zones", len(analytics.get("zone_distribution", {})))
        
except FileNotFoundError:
    st.error("Analytics data not found. Please ensure the pipeline has generated outputs/analytics.json")
    st.stop()

st.write("") # Spacer

# --------------------
# Main Charts Section
# --------------------
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Zone Distribution")
    zone_data = analytics.get("zone_distribution", {})
    if zone_data:
        df_zones = pd.DataFrame(list(zone_data.items()), columns=["Zone", "Visitor Count"])
        # Upgrade to Plotly for a better look
        fig_zones = px.bar(
            df_zones, 
            x="Zone", 
            y="Visitor Count", 
            color="Visitor Count",
            color_continuous_scale="Blues"
        )
        fig_zones.update_layout(margin=dict(l=0, r=0, t=30, b=0), showlegend=False)
        st.plotly_chart(fig_zones, use_container_width=True)
    else:
        st.info("No zone data available.")

with col_chart2:
    st.subheader("Average Dwell Time")
    try:
        with open("outputs/dwell_analytics.json") as f:
            dwell = json.load(f)
        df_dwell = pd.DataFrame(list(dwell.items()), columns=["Zone", "Seconds"])
        
        fig_dwell = px.bar(
            df_dwell, 
            x="Seconds", 
            y="Zone", 
            orientation='h',
            color="Seconds",
            color_continuous_scale="Teal"
        )
        fig_dwell.update_layout(margin=dict(l=0, r=0, t=30, b=0), showlegend=False)
        st.plotly_chart(fig_dwell, use_container_width=True)
    except FileNotFoundError:
        st.warning("Run dwell_analytics.py first to generate dwell time data.")

st.divider()

# --------------------
# Heatmap & Journeys Section
# --------------------
col_heat, col_journey = st.columns([1.5, 1])

with col_heat:
    st.subheader("Store Heatmap")
    if os.path.exists("outputs/heatmap.png"):
        image = Image.open("outputs/heatmap.png")
        # Use a container to add a border/shadow to the image via markdown if desired
        st.image(image, use_container_width=True, caption="Customer concentration and traffic flow.")
    else:
        st.info("Heatmap not generated yet.")

with col_journey:
    st.subheader("Sample Customer Journeys")
    try:
        with open("outputs/journeys.json") as f:
            journeys = json.load(f)
            
        # Display in a clean, scrollable expander or styled text
        with st.container(height=400):
            for visitor in list(journeys.keys())[:10]:
                path = " ➔ ".join(journeys[visitor])
                st.markdown(f"**Visitor {visitor}:**<br> {path}", unsafe_allow_html=True)
                st.markdown("<hr style='margin: 0.5em 0px; border-top: 1px solid #f0f0f0;'>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Run journeys.py first to see path data.")

# --------------------
# Anomaly Detection
# --------------------
st.divider()
st.subheader("🚨 Anomaly Detection")

try:
    with open("outputs/anomalies.json") as f:
        anomalies = json.load(f)

    if len(anomalies) == 0:
        st.success("System Normal: No anomalies detected.", icon="✅")
    else:
        st.warning(f"{len(anomalies)} Anomaly/Anomalies Detected!", icon="⚠️")
        
        # Display as a clean table if it's a list of dictionaries (standard JSON format)
        if isinstance(anomalies, list) and len(anomalies) > 0 and isinstance(anomalies[0], dict):
            df_anomalies = pd.DataFrame(anomalies)
            st.dataframe(df_anomalies, use_container_width=True, hide_index=True)
        else:
            # Fallback to JSON if the structure is more complex
            with st.expander("View Anomaly Details", expanded=True):
                for anomaly in anomalies:
                    st.json(anomaly)

except FileNotFoundError:
    st.info("Run anomaly_detection.py first to monitor for unusual behavior.", icon="ℹ️")
except json.JSONDecodeError:
    st.error("Error reading anomalies.json. Ensure the file contains valid JSON.", icon="❌")