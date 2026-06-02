from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.track(
    source="data/test_video.mp4",
    tracker="bytetrack.yaml",
    persist=True,
    stream=True
)

for result in results:

    print("Frame shape:", result.orig_shape)

    if result.boxes.id is not None:

        boxes = result.boxes.xyxy.cpu().numpy()
        ids = result.boxes.id.cpu().numpy()

        for box, track_id in zip(boxes, ids):

            x1, y1, x2, y2 = box

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            print(
                f"ID={int(track_id)} Center=({center_x},{center_y})"
            )

    break