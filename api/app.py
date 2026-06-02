from fastapi import FastAPI
import json

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
  