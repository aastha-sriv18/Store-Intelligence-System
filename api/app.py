from fastapi import FastAPI
import json
import subprocess
import os

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Store Intelligence API Running"
    }


@app.get("/analytics")
def analytics():

    with open("outputs/analytics.json") as f:
        data = json.load(f)

    return data


    
@app.get("/events")
def events():

    with open("outputs/events.json") as f:
        data = json.load(f)

    return data

@app.get("/dwell")
def get_dwell():

    with open(
        "outputs/dwell_times.json"
    ) as f:

        return json.load(f)
    
    
@app.get("/funnel")
def get_funnel():

    with open(
        "outputs/funnel.json"
    ) as f:

        return json.load(f)
    
@app.get("/anomalies")
def anomalies():

    with open("outputs/anomalies.json") as f:
        return json.load(f)
    
@app.get("/metrics")
def metrics():

    with open("outputs/analytics.json") as f:
        analytics = json.load(f)

    with open("outputs/funnel.json") as f:
        funnel = json.load(f)

    with open("outputs/anomalies.json") as f:
        anomalies = json.load(f)


    return {
        "analytics": analytics,
        "funnel": funnel,
        "anomalies": anomalies
    }
  
@app.get("/sales-metrics")
def sales_metrics():

    # optional: auto-recompute before serving
    subprocess.run(["python", "pipeline/sales_analytics.py"])

    if not os.path.exists("outputs/sales_metrics.json"):
        return {"error": "sales_metrics.json not found"}

    with open("outputs/sales_metrics.json") as f:
        return json.load(f)
    

@app.post("/recompute-sales-metrics")
def recompute_sales_metrics():
    from pipeline.sales_analytics import compute_sales_metrics
    return compute_sales_metrics()