from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.track(
    source="data/test_video.mp4",
    tracker="bytetrack.yaml",
    save=True,
    persist=True
)

print("Tracking complete!")