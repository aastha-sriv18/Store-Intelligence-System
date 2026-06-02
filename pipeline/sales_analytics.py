import pandas as pd
import json

df = pd.read_csv(
    "data/sales.csv"
)

total_orders = df["order_id"].nunique()

total_revenue = df["GMV"].sum()

avg_basket = (
    total_revenue /
    total_orders
)

with open(
    "outputs/analytics.json"
) as f:
    analytics = json.load(f)

visitors = analytics["unique_visitors"]

conversion_rate = (
    total_orders /
    visitors * 100
)

sales_data = {
    "orders": int(total_orders),
    "revenue": round(total_revenue, 2),
    "avg_basket": round(avg_basket, 2),
    "conversion_rate": round(
        conversion_rate, 2
    )
}

with open(
    "outputs/sales_metrics.json",
    "w"
) as f:
    json.dump(
        sales_data,
        f,
        indent=4
    )