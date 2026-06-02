import json
from collections import defaultdict

with open("outputs/events.json", "r") as f:
    events = json.load(f)

journeys = defaultdict(list)

for event in events:

    if event["event_type"] == "ZONE_ENTER":

        visitor_id = event["visitor_id"]
        zone = event["zone"]

        if len(journeys[visitor_id]) == 0:
            journeys[visitor_id].append(zone)

        elif journeys[visitor_id][-1] != zone:
            journeys[visitor_id].append(zone)

print("\n===== CUSTOMER JOURNEYS =====\n")

for visitor_id, path in journeys.items():

    print(
        f"Visitor {visitor_id}: "
        + " -> ".join(path)
    )