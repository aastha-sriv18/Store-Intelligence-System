from ultralytics import YOLO

# =====================================
# CONFIGURATION
# =====================================

ENTRY_LINE_Y = 1200

ZONES = {
    "SKINCARE": (0, 0, 1920, 1080),
    "MAKEUP": (1920, 0, 3840, 1080),
    "FRAGRANCE": (0, 1080, 1920, 2160),
    "BILLING": (1920, 1080, 3840, 2160)
}


# =====================================
# HELPER FUNCTION
# =====================================

def get_zone(x, y):

    for zone_name, (x1, y1, x2, y2) in ZONES.items():

        if x1 <= x <= x2 and y1 <= y <= y2:
            return zone_name

    return "UNKNOWN"


# =====================================
# LOAD MODEL
# =====================================

model = YOLO("yolov8n.pt")


# =====================================
# STATE STORAGE
# =====================================

previous_positions = {}
entered_ids = set()

# Stores current zone of each visitor
visitor_zones = {}


# =====================================
# PROCESS VIDEO
# =====================================

results = model.track(
    source="data/test_video.mp4",
    tracker="bytetrack.yaml",
    persist=True,
    stream=True
)

for result in results:

    if result.boxes.id is None:
        continue

    boxes = result.boxes.xyxy.cpu().numpy()
    ids = result.boxes.id.cpu().numpy()

    for box, track_id in zip(boxes, ids):

        track_id = int(track_id)

        x1, y1, x2, y2 = box

        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)

        zone = get_zone(center_x, center_y)

        # =====================================
        # ZONE EVENTS
        # =====================================

        if track_id not in visitor_zones:

            visitor_zones[track_id] = zone

            print(
                f"ZONE_ENTER -> Visitor {track_id} entered {zone}"
            )

        else:

            previous_zone = visitor_zones[track_id]

            if previous_zone != zone:

                print(
                    f"ZONE_EXIT -> Visitor {track_id} left {previous_zone}"
                )

                print(
                    f"ZONE_ENTER -> Visitor {track_id} entered {zone}"
                )

                visitor_zones[track_id] = zone

        # =====================================
        # DEBUG INFO
        # =====================================

        print(
            f"ID={track_id} "
            f"Center=({center_x},{center_y}) "
            f"Zone={zone}"
        )

        # =====================================
        # ENTRY DETECTION
        # =====================================

        if track_id in previous_positions:

            prev_y = previous_positions[track_id]

            crossed = (
                prev_y < ENTRY_LINE_Y
                and center_y >= ENTRY_LINE_Y
            )

            if crossed and track_id not in entered_ids:

                entered_ids.add(track_id)

                print(
                    f"ENTRY EVENT -> Visitor {track_id}"
                )

        previous_positions[track_id] = center_y


# =====================================
# SUMMARY
# =====================================

print("\n========== SUMMARY ==========")

print(f"Total Entries: {len(entered_ids)}")

print(f"Unique Visitors Seen: {len(visitor_zones)}")