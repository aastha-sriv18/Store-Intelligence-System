import json
from collections import defaultdict

with open(
    "outputs/dwell_times.json",
    "r"
) as f:

    dwell_data = json.load(f)

zone_totals = defaultdict(float)
zone_counts = defaultdict(int)

for record in dwell_data:

    zone = record["zone"]

    zone_totals[zone] += record[
        "dwell_seconds"
    ]

    zone_counts[zone] += 1

print(
    "\n===== AVG DWELL TIME =====\n"
)

avg_dwell = {}

for zone in zone_totals:

    avg = (
        zone_totals[zone]
        / zone_counts[zone]
    )

    avg_dwell[zone] = round(
        avg,
        2
    )

    print(
        f"{zone}: "
        f"{avg:.2f} sec"
    )

with open(
    "outputs/dwell_analytics.json",
    "w"
) as f:

    json.dump(
        avg_dwell,
        f,
        indent=4
    )

print(
    "\nSaved dwell_analytics.json"
)