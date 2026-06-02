import json
from collections import defaultdict

with open("outputs/events.json") as f:
    events = json.load(f)

journeys = defaultdict(list)

for event in events:

    if event["event_type"] == "ZONE_ENTER":

        journeys[
            event["visitor_id"]
        ].append(
            event["zone"]
        )

journey_dict = dict(journeys)

with open(
    "outputs/journeys.json",
    "w"
) as f:

    json.dump(
        journey_dict,
        f,
        indent=4
    )

print("Saved journeys.json")