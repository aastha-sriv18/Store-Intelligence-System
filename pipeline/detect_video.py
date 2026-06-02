from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.predict(
    source="data/test_video.mp4",
    save=True,
    conf=0.4
)

print("Video processing complete!")