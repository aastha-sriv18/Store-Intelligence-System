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
    
@app.get("/dwell-time")
def get_dwell():
    with open("outputs/dwell_time.json") as f:
        return json.load(f)