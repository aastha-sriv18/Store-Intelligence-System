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
# 3. Floor Plan & Journeys
# --------------------
bottom_col1, bottom_col2 = st.columns([1.5, 1]) 

with bottom_col1:
    st.subheader("Store Heatmap")
    if os.path.exists("outputs/heatmap.png"):
        image = Image.open("outputs/heatmap.png")
        st.image(image, use_container_width=True, caption="Customer concentration and traffic flow.")
    else:
        st.info("Heatmap not generated yet. Run heatmap.py.")

with bottom_col2:
    st.subheader("Sample Customer Journeys")
    try:
        with open("outputs/journeys.json") as f:
            journeys = json.load(f)
        
        
        with st.container(height=520): 
            for visitor in list(journeys.keys())[:15]: 
                
                st.markdown(f"**Visitor {visitor}:**")
                
                st.markdown(f"{' ➔ '.join(journeys[visitor])}")
                
                st.divider()
                
    except FileNotFoundError:
        st.warning("Run journeys.py first.")

# --------------------
# Anomaly Detection
# --------------------
st.divider()
st.subheader("Anomaly Detection")

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


# --------------------
# Conversion Funnel
# --------------------
st.divider()
st.subheader("Conversion Funnel")

try:
    with open("outputs/funnel.json") as f:
        funnel = json.load(f)

    # 1. Display KPIs in a balanced 4-column layout
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)

    with f_col1:
        st.metric("Store Visitors", funnel.get("store_visitors", 0))
    with f_col2:
        st.metric("Billing Visitors", funnel.get("billing_visitors", 0))
    with f_col3:
        st.metric("Transactions", funnel.get("transactions", 0))
    with f_col4:
        st.metric("Conversion Rate", f"{funnel.get('conversion_rate', 0)}%")

    # 2. Generate a visual Plotly Funnel Chart
    st.write("") # Small spacer
    
    # Structure the data for Plotly
    funnel_data = dict(
        number=[
            funnel.get("store_visitors", 0), 
            funnel.get("billing_visitors", 0), 
            funnel.get("transactions", 0)
        ],
        stage=["Store Visitors", "Billing Zone Visitors", "Completed Transactions"]
    )
    df_funnel = pd.DataFrame(funnel_data)
    
    # Create the interactive chart
    fig_funnel = px.funnel(
        df_funnel, 
        x='number', 
        y='stage',
        color_discrete_sequence=['#4C78A8'] # A professional, muted blue
    )
    
    # Clean up the margins so it fits perfectly in the Streamlit container
    fig_funnel.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    
    st.plotly_chart(fig_funnel, use_container_width=True)

except FileNotFoundError:
    st.warning("Run funnel.py first to generate conversion analytics.", icon="⚠️")
except json.JSONDecodeError:
    st.error("Error reading funnel.json. Ensure the file contains valid JSON.", icon="❌")

# --------------------
# Footer
# --------------------
st.write("") # Adds a bit of vertical space
st.markdown("<hr style='border-top: 1px solid #e0e0e0; margin-top: 2rem; margin-bottom: 2rem;'>", unsafe_allow_html=True)

footer_text = "© 2026 Store Intelligence System | Crafted with precision by Aastha Srivastava."

st.markdown(
    f"""
    <div style="text-align: center; color: #888888; font-size: 14px; padding-bottom: 20px;">
        {footer_text}
    </div>
    """, 
    unsafe_allow_html=True
)