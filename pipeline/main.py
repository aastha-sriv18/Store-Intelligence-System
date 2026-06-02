from ultralytics import YOLO
from pipeline.zones import get_zone, ZONES
from pipeline.event_engine import create_event
import json
ENTRY_LINE_Y = 350

model = YOLO("yolov8n.pt")

previous_positions = {}
entered_ids = set()
visitor_zones = {}

events = []
frame_number = 0
positions = []
results = model.track(
    source="data/test_video.mp4",
    tracker="bytetrack.yaml",
    persist=True,
    stream=True
)

for result in results:
    frame_number += 1
    if frame_number == 1:
        print("\n==============================")
        print("FRAME SHAPE =", result.orig_img.shape)
        print("==============================\n")


    if result.boxes.id is None:
        continue

    boxes = result.boxes.xyxy.cpu().numpy()
    ids = result.boxes.id.cpu().numpy()

    for box, track_id in zip(boxes, ids):

        track_id = int(track_id)

        x1, y1, x2, y2 = box

        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)

        positions.append(
            {
                "visitor_id": track_id,
                "x": center_x,
                "y": center_y,
                "frame": frame_number
            }
        )

        zone = get_zone(
            center_x,
            center_y
        )
        #print(
         #   f"ID={track_id} "
          #  f"Center=({center_x},{center_y}) "
           # f"Zone={zone}"
        #)

        # -------------------------
        # Zone Events
        # -------------------------

        if track_id not in visitor_zones:

            visitor_zones[track_id] = zone

            event = create_event(
                track_id,
                "ZONE_ENTER",
                frame_number,
                zone
            )

            events.append(event)

            print(event)

        else:

            previous_zone = visitor_zones[track_id]

            if previous_zone != zone and zone != "UNKNOWN":

                exit_event = create_event(
                    track_id,
                    "ZONE_EXIT",
                    frame_number,
                    previous_zone
                )

                enter_event = create_event(
                    track_id,
                    "ZONE_ENTER",
                    frame_number,
                    zone
                )

                events.append(exit_event)
                events.append(enter_event)

                print(exit_event)
                print(enter_event)

                visitor_zones[track_id] = zone

        # -------------------------
        # Entry Events
        # -------------------------

        if track_id in previous_positions:

            prev_y = previous_positions[track_id]

            crossed = (
                prev_y < ENTRY_LINE_Y
                and center_y >= ENTRY_LINE_Y
            )

            if crossed and track_id not in entered_ids:

                entered_ids.add(track_id)

                event = create_event(
                    track_id,
                    "STORE_ENTRY",
                    frame_number,
                    zone
                )

                events.append(event)

                print(event)

        previous_positions[track_id] = center_y

# -------------------------
# Save Events
# -------------------------

with open(
    "outputs/events.json",
    "w"
) as f:

    json.dump(
        events,
        f,
        indent=4
    )

print("\n========== SUMMARY ==========")
print("Total Entries:", len(entered_ids))
print("Total Events:", len(events))

with open(
    "outputs/positions.json",
    "w"
) as f:

    json.dump(
        positions,
        f,
        indent=4
    )

