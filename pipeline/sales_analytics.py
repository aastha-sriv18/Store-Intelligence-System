import pandas as pd
import json
import os


SALES_PATH = "data/sales.csv"
ANALYTICS_PATH = "outputs/analytics.json"
OUTPUT_PATH = "outputs/sales_metrics.json"


def compute_sales_metrics():
    df = pd.read_csv(SALES_PATH)

    # basic cleaning safety
    df = df.dropna(subset=["order_id", "GMV"])

    total_orders = df["order_id"].nunique()
    total_revenue = df["GMV"].sum()

    avg_basket = total_revenue / total_orders if total_orders else 0

    # load visitor analytics safely
    if os.path.exists(ANALYTICS_PATH):
        with open(ANALYTICS_PATH) as f:
            analytics = json.load(f)
        visitors = analytics.get("unique_visitors", 0)
    else:
        visitors = 0

    conversion_rate = (
        (total_orders / visitors * 100)
        if visitors else 0
    )

    sales_data = {
        "orders": int(total_orders),
        "revenue": round(float(total_revenue), 2),
        "avg_basket": round(float(avg_basket), 2),
        "conversion_rate": round(float(conversion_rate), 2)
    }

    os.makedirs("outputs", exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(sales_data, f, indent=4)

    return sales_data


if __name__ == "__main__":
    print(compute_sales_metrics())