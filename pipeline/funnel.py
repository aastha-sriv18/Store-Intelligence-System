import json
import pandas as pd

# -------------------------
# Load Analytics
# -------------------------

with open("outputs/analytics.json", "r") as f:
    analytics = json.load(f)

total_visitors = analytics["unique_visitors"]

# -------------------------
# Billing Visitors
# -------------------------

with open("outputs/events.json", "r") as f:
    events = json.load(f)

billing_visitors = set()

for event in events:

    if (
        event["event_type"] == "ZONE_ENTER"
        and event["zone"] == "BILLING"
    ):
        billing_visitors.add(
            event["visitor_id"]
        )

billing_count = len(
    billing_visitors
)

# -------------------------
# Sales Data
# -------------------------

sales_df = pd.read_csv(
    "data/sales.csv"
)

transactions = len(
    sales_df["order_id"].unique()
)

# -------------------------
# Conversion
# -------------------------

conversion_rate = 0

if total_visitors > 0:

    conversion_rate = (
        transactions
        / total_visitors
    ) * 100

# -------------------------
# Save
# -------------------------

funnel_data = {
    "store_visitors": total_visitors,
    "billing_visitors": billing_count,
    "transactions": transactions,
    "conversion_rate": round(
        conversion_rate,
        2
    )
}

with open(
    "outputs/funnel.json",
    "w"
) as f:

    json.dump(
        funnel_data,
        f,
        indent=4
    )

print(
    "\nFunnel saved to outputs/funnel.json"
)