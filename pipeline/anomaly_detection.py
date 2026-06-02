import json
from collections import defaultdict

DWELL_THRESHOLD = 10
ZONE_SWITCH_THRESHOLD = 5

anomalies = []

# -------------------------
# Long Dwell Time
# -------------------------

with open(
    "outputs/dwell_times.json"
) as f:

    dwell_data = json.load(f)

for record in dwell_data:

    if (
        record["dwell_seconds"]
        > DWELL_THRESHOLD
    ):

        anomalies.append(
            {
                "visitor_id":
                record["visitor_id"],

                "anomaly":
                "LONG_DWELL_TIME",

                "zone":
                record["zone"],

                "dwell_seconds":
                record["dwell_seconds"]
            }
        )

# -------------------------
# Customer Journeys
# -------------------------

with open(
    "outputs/journeys.json"
) as f:

    journeys = json.load(f)

# -------------------------
# Excessive Zone Switching
# -------------------------

for visitor, path in journeys.items():

    unique_zones = len(path)

    if (
        unique_zones
        > ZONE_SWITCH_THRESHOLD
    ):

        anomalies.append(
            {
                "visitor_id": visitor,
                "anomaly":
                "EXCESSIVE_ZONE_SWITCHING",
                "zones_visited":
                unique_zones
            }
        )

# -------------------------
# Direct Checkout
# -------------------------

for visitor, path in journeys.items():

    if len(path) >= 2:

        if (
            path[0] == "ENTRANCE"
            and path[1] == "CHECKOUT"
        ):

            anomalies.append(
                {
                    "visitor_id": visitor,
                    "anomaly":
                    "DIRECT_CHECKOUT"
                }
            )

# -------------------------
# Save
# -------------------------

with open(
    "outputs/anomalies.json",
    "w"
) as f:

    json.dump(
        anomalies,
        f,
        indent=4
    )

print(
    "\n===== ANOMALIES =====\n"
)

for anomaly in anomalies:

    print(anomaly)

print(
    f"\nTotal Anomalies: "
    f"{len(anomalies)}"
)