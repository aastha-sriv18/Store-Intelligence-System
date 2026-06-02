import json

with open("outputs/events.json", "r") as f:
    events = json.load(f)

# Count store entries
total_entries = sum(
    1 for event in events
    if event["event_type"] == "STORE_ENTRY"
)

all_visitors = set()

for event in events:
    all_visitors.add(
        event["visitor_id"]
    )

unique_visitors = len(all_visitors)

# Zone distribution
zone_distribution = {}

for event in events:

    zone = event["zone"]

    if zone not in zone_distribution:
        zone_distribution[zone] = 0

    zone_distribution[zone] += 1

print("\n===== STORE ANALYTICS =====")
print("Total Entries:", total_entries)
print("Unique Visitors:", unique_visitors)

print("\nZone Distribution:")

for zone, count in zone_distribution.items():
    print(f"{zone}: {count}")

analytics_data = {
    "total_entries": total_entries,
    "unique_visitors": unique_visitors,
    "zone_distribution": zone_distribution
}

with open("outputs/analytics.json", "w") as f:
    json.dump(
        analytics_data,
        f,
        indent=4
    )

print("\nanalytics.json created successfully")