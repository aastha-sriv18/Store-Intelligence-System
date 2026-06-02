import streamlit as st
import json
import pandas as pd
from PIL import Image
import os

st.title(
    "Store Intelligence Dashboard"
)

# --------------------
# Analytics
# --------------------

with open(
    "outputs/analytics.json"
) as f:

    analytics = json.load(f)

st.header(
    "Store Overview"
)

col1, col2 = st.columns(2)

col1.metric(
    "Total Entries",
    analytics["total_entries"]
)

col2.metric(
    "Unique Visitors",
    analytics["unique_visitors"]
)

# --------------------
# Zone Distribution
# --------------------

st.header(
    "Zone Distribution"
)

zone_df = pd.DataFrame(
    analytics["zone_distribution"].items(),
    columns=[
        "Zone",
        "Count"
    ]
)

st.bar_chart(
    zone_df.set_index("Zone")
)

# --------------------
# Dwell Time
# --------------------

try:

    with open(
        "outputs/dwell_analytics.json"
    ) as f:

        dwell = json.load(f)

    st.header(
        "Average Dwell Time"
    )

    dwell_df = pd.DataFrame(
        dwell.items(),
        columns=[
            "Zone",
            "Seconds"
        ]
    )

    st.bar_chart(
        dwell_df.set_index("Zone")
    )

except:

    st.warning(
        "Run dwell_analytics.py first"
    )

# --------------------
# Customer Journeys
# --------------------

try:

    with open(
        "outputs/journeys.json"
    ) as f:

        journeys = json.load(f)

    st.header(
        "Sample Customer Journeys"
    )

    for visitor in list(
        journeys.keys()
    )[:10]:

        st.write(
            f"Visitor {visitor}: "
            +
            " → ".join(
                journeys[visitor]
            )
        )

except:

    st.warning(
        "Run journeys.py first"
    )
# -------------------------
# Heatmap
# -------------------------

if os.path.exists(
    "outputs/heatmap.png"
):

    st.subheader(
        "Store Heatmap"
    )

    image = Image.open(
        "outputs/heatmap.png"
    )

    st.image(
        image,
        use_container_width=True
    )

